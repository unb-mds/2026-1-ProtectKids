"""
crawler/camara_api.py

Pipeline ETL — Câmara dos Deputados → PostgreSQL
Busca proposições legislativas relacionadas à proteção infantil,
baixa os PDFs, extrai o texto integral, classifica via NLP (spaCy)
e salva as informações enriquecidas no banco.

Uso:
    # A partir da raiz do projeto (backend/)
    python -m crawler.camara_api

    # Ou diretamente, com o PYTHONPATH configurado:
    PYTHONPATH=.. python crawler/camara_api.py
"""

import sys
import os
import logging
import tempfile
import re
import unicodedata
from typing import Optional
from sqlmodel import select, Session, SQLModel
from datetime import datetime
import requests
import fitz
import spacy
import concurrent.futures

# Garante que o módulo backend/ seja encontrado quando executado diretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Inicializa o modelo de NLP do spaCy em Português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    logger.error("Modelo 'pt_core_news_sm' do spaCy não encontrado. Execute o download no Docker antes.")
    raise

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
ENDPOINT_PROPOSICOES = f"{BASE_URL}/proposicoes"

# Palavras-chave relacionadas à proteção infantil
KEYWORDS = [
    "criança",
    "adolescente",
    "infância",
    "ECA",
    "proteção infantil",
    "direitos da criança",
    "conselho tutelar",
    "cyberbullying",
    "internet",
    "proteção de dados",
    "adoção",
    "acolhimento institucional",
    "violência infantil",
    "abuso sexual",
    "exploração sexual",
    "trabalho infantil",
    "educação infantil",
    "creche",
]
TEMA_PADRAO = "Protecao Infantil"

# ---------------------------------------------------------------------------
# DICIONÁRIO DE FILTRAGEM (NLP FAST-PATH)
# ---------------------------------------------------------------------------

TERMOS_SIMBOLICOS = [
    "voto de aplauso",
    "voto de louvor",
    "voto de congratulação",
    "voto de congratulações",
    "voto de pesar",
    "título de cidadão",
    "homenagem",
    "sessão solene",
    "data comemorativa",
    "dia nacional"
]

TERMOS_ESTRATEGICOS = [
    "audiência pública",
    "regime de urgência",
    "convocação",
    "pedido de informação",
    "comissão parlamentar",
    "ministério",
    "recursos financeiros"
]

# Parâmetros fixos da busca
PARAMS_BASE = {
    "siglaTipo": "PL",          # Somente Projetos de Lei
    "itens": 20,                 # Resultados por página
    "ordem": "DESC",
    "ordenarPor": "id",
}

# Número máximo de páginas a buscar por palavra-chave (evita explosão de dados)
LIMITE_PAGINAS = int(os.getenv("MAX_PAGES", 3))

# ---------------------------------------------------------------------------
# CAMADA DE FETCH — busca dados na API externa e extrai documentos
# ---------------------------------------------------------------------------

def fetch_proposicoes_por_keyword(keyword: str) -> list[dict]:
    """
    Consulta a API da Câmara buscando proposições que contenham `keyword`
    na ementa. Pagina automaticamente até LIMITE_PAGINAS.
    Injeta a palavra-chave usada dentro do dicionário para rastreamento posterior.
    """
    resultados: list[dict] = []

    for pagina in range(1, LIMITE_PAGINAS + 1):
        params = {
            **PARAMS_BASE,
            "keywords": keyword,
            "pagina": pagina,
        }

        logger.info(f"Buscando keyword='{keyword}' | página {pagina}/{LIMITE_PAGINAS}")

        try:
            response = requests.get(
                ENDPOINT_PROPOSICOES,
                params=params,
                timeout=60,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout na página {pagina} para keyword '{keyword}'. Pulando.")
            break
        except requests.exceptions.HTTPError as exc:
            logger.error(f"Erro HTTP {exc.response.status_code} para keyword '{keyword}': {exc}")
            break
        except requests.exceptions.RequestException as exc:
            logger.error(f"Erro de rede para keyword '{keyword}': {exc}")
            break

        dados = response.json().get("dados", [])

        if not dados:
            logger.info(f"Sem mais resultados para '{keyword}' na página {pagina}.")
            break

        # Injeta qual keyword trouxe essa proposição para usarmos como subtema inicial
        for d in dados:
            d["_keyword_origem"] = keyword

        resultados.extend(dados)
        logger.info(f"{len(dados)} proposições encontradas nesta página.")

    return resultados


def fetch_todas_proposicoes() -> list[dict]:
    """
    Executa a busca para todas as KEYWORDS e retorna uma lista consolidada,
    removendo duplicatas pelo campo 'id' da API.
    """
    todas: dict[int, dict] = {}

    for keyword in KEYWORDS:
        proposicoes = fetch_proposicoes_por_keyword(keyword)
        for prop in proposicoes:
            api_id = prop.get("id")
            if api_id and api_id not in todas:
                todas[api_id] = prop

    logger.info(f"Total de proposições únicas encontradas: {len(todas)}")
    return list(todas.values())


def fetch_autor_da_proposicao(id_proposicao_api: int) -> dict:
    url_autores = f"{BASE_URL}/proposicoes/{id_proposicao_api}/autores"
    try:
        resp_autores = requests.get(url_autores, timeout=30, headers={"Accept": "application/json"})
        resp_autores.raise_for_status()
        dados_autores = resp_autores.json().get("dados", [])
        
        if not dados_autores:
            return {}
            
        autor = dados_autores[0]
        uri_autor = autor.get("uri", "")
        
        if "deputados" in uri_autor:
            resp_perfil = requests.get(uri_autor, timeout=30, headers={"Accept": "application/json"})
            resp_perfil.raise_for_status()
            perfil = resp_perfil.json().get("dados", {})
            status = perfil.get("ultimoStatus", {})
            
            autor["siglaPartido"] = status.get("siglaPartido", "ND")
            autor["siglaUf"] = status.get("siglaUf", "ND")
            
        return autor
        
    except Exception as exc:
        logger.warning(f"Erro ao buscar autor da proposicao {id_proposicao_api}: {exc}")
        return {}

def fetch_detalhes_proposicao(id_proposicao_api: int) -> dict:
    url_detalhes = f"{BASE_URL}/proposicoes/{id_proposicao_api}"
    try:
        resp = requests.get(url_detalhes, timeout=30, headers={"Accept": "application/json"})
        resp.raise_for_status()
        return resp.json().get("dados", {})
    except Exception as exc:
        logger.warning(f"Erro ao buscar detalhes da proposição {id_proposicao_api}: {exc}")
        return {}
    
def extrair_texto_pdf(url_pdf: Optional[str]) -> Optional[str]:
    """
    Faz o descarregamento do PDF de forma temporária e extrai 
    todo o texto utilizando o PyMuPDF (fitz) para máxima velocidade.
    """
    if not url_pdf:
        return None
    
    try:
        logger.info(f"Descarregando PDF para extração rápida: {url_pdf}")
        resposta = requests.get(url_pdf, timeout=30)
        resposta.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(resposta.content)
            temp_pdf_path = temp_pdf.name
            
        texto_extraido = ""
        # A nova lógica de leitura ultrarrápida com PyMuPDF
        with fitz.open(temp_pdf_path) as pdf:
            for pagina in pdf:
                texto = pagina.get_text()
                if texto:
                    texto_extraido += texto + "\n"
                    
        os.remove(temp_pdf_path)
        return texto_extraido.strip() if texto_extraido else None
        
    except Exception as e:
        logger.warning(f"Não foi possível processar o PDF da URL {url_pdf}: {e}")
        return None
# ---------------------------------------------------------------------------
# CAMADA DE NLP — Processamento de Linguagem Natural
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# CAMADA DE NLP — Processamento de Linguagem Natural
# ---------------------------------------------------------------------------

CATEGORIA_PADRAO = "Proteção Geral"

TERMOS_SIMBOLICOS = [
    "voto de aplauso",
    "voto de louvor",
    "voto de congratulação",
    "voto de congratulações",
    "voto de pesar",
    "título de cidadão",
    "titulo de cidadao",
    "homenagem",
    "sessão solene",
    "sessao solene",
    "data comemorativa",
    "dia nacional",
]

TERMOS_ESTRATEGICOS = [
    "audiência pública",
    "audiencia publica",
    "regime de urgência",
    "regime de urgencia",
    "convocação",
    "convocacao",
    "pedido de informação",
    "pedido de informacao",
    "comissão parlamentar",
    "comissao parlamentar",
    "requerimento",
]

CATEGORIAS_NLP = {
    "Cyberbullying e Crimes Virtuais": {
        "frases": [
            "cyberbullying",
            "intimidação sistemática virtual",
            "intimidacao sistematica virtual",
            "crime virtual",
            "crime cibernético",
            "crime cibernetico",
            "ambiente digital",
            "rede social",
            "redes sociais",
            "plataforma digital",
            "plataformas digitais",
            "proteção de dados",
            "protecao de dados",
            "dados pessoais",
            "controle parental",
            "conteúdo nocivo",
            "conteudo nocivo",
            "exploração sexual online",
            "exploracao sexual online",
        ],
        "termos": [
            "cyberbullying",
            "internet",
            "digital",
            "virtual",
            "cibernético",
            "cibernetico",
            "computador",
            "aplicativo",
            "algoritmo",
            "plataforma",
        ],
    },
    "Adoção e Orfanatos": {
        "frases": [
            "adoção",
            "adocao",
            "acolhimento institucional",
            "família substituta",
            "familia substituta",
            "destituição do poder familiar",
            "destituicao do poder familiar",
            "guarda provisória",
            "guarda provisoria",
            "abrigo institucional",
        ],
        "termos": [
            "adoção",
            "adocao",
            "adotar",
            "adotivo",
            "adotante",
            "adotado",
            "órfão",
            "orfao",
            "orfanato",
            "abrigamento",
        ],
    },
    "Violência e Abuso": {
        "frases": [
            "abuso sexual",
            "exploração sexual",
            "exploracao sexual",
            "violência doméstica",
            "violencia domestica",
            "violência contra criança",
            "violencia contra crianca",
            "violência contra adolescente",
            "violencia contra adolescente",
            "maus-tratos",
            "trabalho infantil",
            "pedofilia",
        ],
        "termos": [
            "violência",
            "violencia",
            "abuso",
            "exploração",
            "exploracao",
            "agressão",
            "agressao",
            "estupro",
            "aliciamento",
            "pedofilia",
            "pornografia",
            "maus-tratos",
        ],
    },
    "Educação e Cultura": {
        "frases": [
            "educação infantil",
            "educacao infantil",
            "primeira infância",
            "primeira infancia",
            "ensino fundamental",
            "alimentação escolar",
            "alimentacao escolar",
            "merenda escolar",
            "material didático",
            "material didatico",
        ],
        "termos": [
            "escola",
            "ensino",
            "professor",
            "merenda",
            "didático",
            "didatico",
            "creche",
            "colégio",
            "colegio",
            "alfabetização",
            "alfabetizacao",
        ],
    },
}

MAX_CARACTERES_NLP = 80000
PONTUACAO_MINIMA = 2


def normalizar_texto(valor: Optional[str]) -> str:
    """
    Normaliza texto para comparação:
    - minúsculas;
    - sem acentos;
    - espaços normalizados.
    """
    if not valor:
        return ""

    texto = str(valor).lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def gerar_lemas(texto: Optional[str]) -> list[str]:
    """
    Gera lemas normalizados usando spaCy.
    O texto é limitado para evitar estouro de memória com PDFs muito grandes.
    """
    if not texto:
        return []

    texto_limitado = str(texto)[:MAX_CARACTERES_NLP]
    doc = nlp(texto_limitado.lower())

    return [
        normalizar_texto(token.lemma_)
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.like_num
        and len(token.text) > 2
    ]


def calcular_pontuacao_categoria(
    categoria: str,
    regras: dict,
    ementa_normalizada: str,
    texto_normalizado: str,
    lemas_ementa: list[str],
    lemas_texto: list[str],
) -> int:
    """
    Calcula pontuação ponderada de uma categoria.

    A ementa tem peso maior porque costuma resumir melhor a proposição.
    O texto integral entra como reforço, não como decisão absoluta.
    """
    pontuacao = 0

    frases = regras.get("frases", [])
    termos = {normalizar_texto(termo) for termo in regras.get("termos", [])}

    for frase in frases:
        frase_normalizada = normalizar_texto(frase)

        if frase_normalizada and frase_normalizada in ementa_normalizada:
            pontuacao += 6

        if frase_normalizada and frase_normalizada in texto_normalizado:
            pontuacao += 2

    for lema in lemas_ementa:
        if lema in termos:
            pontuacao += 3

    for lema in lemas_texto:
        if lema in termos:
            pontuacao += 1

    return pontuacao


def classificar_com_ia(texto: Optional[str], ementa: str) -> str:
    """
    Classifica a proposição usando:
    - filtros rápidos para ruído legislativo;
    - spaCy para lematização;
    - pontuação ponderada por categoria.

    Observação:
    esta abordagem é NLP heurístico, não modelo supervisionado treinado.
    """
    ementa_normalizada = normalizar_texto(ementa)
    texto_normalizado = normalizar_texto(texto)

    if not ementa_normalizada and not texto_normalizado:
        return CATEGORIA_PADRAO

    is_simbolico = any(
        normalizar_texto(termo) in ementa_normalizada
        for termo in TERMOS_SIMBOLICOS
    )

    is_estrategico = any(
        normalizar_texto(termo) in ementa_normalizada
        for termo in TERMOS_ESTRATEGICOS
    )

    if is_simbolico and not is_estrategico:
        return "Simbólico/Ruído"

    if is_estrategico:
        return "Articulação Estratégica"

    try:
        lemas_ementa = gerar_lemas(ementa)
        lemas_texto = gerar_lemas(texto)

        pontuacoes = {
            categoria: calcular_pontuacao_categoria(
                categoria=categoria,
                regras=regras,
                ementa_normalizada=ementa_normalizada,
                texto_normalizado=texto_normalizado,
                lemas_ementa=lemas_ementa,
                lemas_texto=lemas_texto,
            )
            for categoria, regras in CATEGORIAS_NLP.items()
        }

        categoria_vencedora = max(pontuacoes, key=pontuacoes.get)

        if pontuacoes[categoria_vencedora] >= PONTUACAO_MINIMA:
            return categoria_vencedora

        return CATEGORIA_PADRAO

    except Exception as exc:
        logger.error(f"Erro no processamento NLP: {exc}")
        return CATEGORIA_PADRAO

# ---------------------------------------------------------------------------
# CAMADA DE TRANSFORM — mapeia dados da API para o modelo do sistema
# ---------------------------------------------------------------------------

def transform_proposicao(dado_bruto: dict, autor_bruto: dict) -> Optional[tuple]:
    sigla = dado_bruto.get("siglaTipo", "PL")
    numero = dado_bruto.get("numero")
    ano = dado_bruto.get("ano")
    ementa = dado_bruto.get("ementa", "").strip()
    
    if not numero or not ano or not ementa:
        return None
        
    id_bruto = dado_bruto.get("id")
    id_externo_formatado = f"camara-{id_bruto}"

    # 1. Monta o Parlamentar
    parlamentar = None
    id_autor = None
    if autor_bruto:
        uri = autor_bruto.get("uri", "")
        try:
            id_autor = int(uri.split("/")[-1])
        except:
            id_autor = 999999
            
        parlamentar = Parlamentar(
            id_parlamentar=id_autor,
            nome=autor_bruto.get("nome", "Desconhecido"),
            partido=autor_bruto.get("siglaPartido", "ND"),
            uf=autor_bruto.get("siglaUf", "ND")
        )
        
    # 2. Formata a Data
    data_apres = None
    data_str = dado_bruto.get("dataApresentacao")
    if data_str:
        try:
            data_apres = datetime.fromisoformat(data_str).date()
        except:
            pass

    # --- PROCESSAMENTO ENRIQUECIDO (PASSO 2) ---
    url_pdf = dado_bruto.get("urlInteiroTeor")
    
    # Executa o pipeline de PDF e IA
    texto_pdf = extrair_texto_pdf(url_pdf)
    classificacao_ia = classificar_com_ia(texto_pdf, ementa)
    subtema_origem = dado_bruto.get("_keyword_origem", "Geral")

    # 3. Monta a Proposicao com os novos campos populados
    proposicao = Proposicao(
        id_externo=id_externo_formatado,
        id_autor=id_autor,
        origem="Camara",
        tipo=sigla,
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        tema=TEMA_PADRAO,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf,
        subtema=subtema_origem,
        texto_integral=texto_pdf,
        classificacao_nlp=classificacao_ia,
)
    
    return (proposicao, parlamentar)

# ---------------------------------------------------------------------------
# CAMADA DE OTIMIZAÇÃO (NOVO)
# ---------------------------------------------------------------------------

def obter_ids_existentes(origem_alvo: str) -> set:
    """
    Busca no banco todos os IDs externos já cadastrados para evitar 
    o download repetido de PDFs e reprocessamento de NLP.
    """
    with Session(engine) as session:
        # Selecionamos apenas a coluna id_externo para não sobrecarregar a memória
        statement = select(Proposicao.id_externo).where(Proposicao.origem == origem_alvo)
        resultados = session.exec(statement).all()
        return set(resultados)

# ---------------------------------------------------------------------------
# CAMADA DE SAVE & RUN PIPELINE
# ---------------------------------------------------------------------------

def save_proposicoes(tuplas_prop_autor: list[tuple]) -> int:
    inseridos = 0
    with Session(engine) as session:
        for prop, autor in tuplas_prop_autor:
            try:
                if autor:
                    existente_autor = session.exec(
                        select(Parlamentar).where(Parlamentar.id_parlamentar == autor.id_parlamentar)
                    ).first()
                    if not existente_autor:
                        session.add(autor)
                        session.flush()

                existente_prop = session.exec(
                    select(Proposicao).where(Proposicao.id_externo == prop.id_externo)
                ).first()
                
                if not existente_prop:
                    session.add(prop)
                    session.flush()
                    inseridos += 1
                    
            except Exception as exc:
                logger.warning(f"Erro ao adicionar proposicao {prop.numero}: {exc}")
                session.rollback()
                continue
                
        session.commit()
    return inseridos

def processar_materia_individual(dado: dict, ids_existentes: set) -> Optional[tuple]:
    """
    Função isolada para ser executada em paralelo (Thread).
    Faz o download do PDF e passa pela IA de forma independente.
    """
    id_bruto = dado.get("id")
    id_externo_formatado = f"camara-{id_bruto}"

    try:
        # Puxa os dados adicionais da API
        autor_bruto = fetch_autor_da_proposicao(id_bruto)
        detalhes_brutos = fetch_detalhes_proposicao(id_bruto)
        
        # Injeta o link do PDF
        dado["urlInteiroTeor"] = detalhes_brutos.get("urlInteiroTeor")
        
        # processamento pesado (PDF + NLP)
        resultado = transform_proposicao(dado, autor_bruto)
        if resultado:
            logger.info(f"Nova matéria processada: {id_externo_formatado}")
        return resultado
    except Exception as exc:
        logger.error(f"Erro na thread ao processar {id_externo_formatado}: {exc}")
        return None
def run_pipeline() -> None:
    logger.info("=== Iniciando pipeline ETL Inteligente (PDF + NLP) ===")
    SQLModel.metadata.create_all(engine)

    ids_existentes = obter_ids_existentes(origem_alvo="Camara")
    logger.info(f"Cache local: {len(ids_existentes)} proposições da Câmara já existem.")

    # 1. EXTRACT
    dados_brutos = fetch_todas_proposicoes()
    if not dados_brutos:
        logger.warning("Nenhuma proposição capturada na extração externa.")
        return

    # 2. TRANSFORM OTIMIZADO (MULTITHREADING)
    tuplas: list[tuple] = []
    ids_processados_nesta_run = set()
    dados_ineditos = []

    # Filtra rapidamente tudo o que é novo e precisa ser processado
    for dado in dados_brutos:
        id_bruto = dado.get("id")
        id_externo_formatado = f"camara-{id_bruto}"
        
        if id_externo_formatado not in ids_existentes and id_externo_formatado not in ids_processados_nesta_run:
            dados_ineditos.append(dado)
            ids_processados_nesta_run.add(id_externo_formatado)

    if not dados_ineditos:
        logger.info("=== Pipeline concluído. Nenhuma matéria inédita para processar hoje. ===")
        return

    logger.info(f"Iniciando download paralelo de {len(dados_ineditos)} PDFs. Isso será rápido...")

    # A MÁGICA: Abre 10 linhas de execução simultâneas
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Envia todas as matérias inéditas para as threads trabalharem
        futuros = {
            executor.submit(processar_materia_individual, d, ids_existentes): d 
            for d in dados_ineditos
        }
        
        # Conforme as threads vão terminando o download e o NLP, vamos guardando o resultado
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                tuplas.append(resultado)

    # 3. LOAD
    if tuplas:
        total_salvo = save_proposicoes(tuplas)
        logger.info(f"=== Pipeline concluído. {total_salvo} novos registros inseridos com NLP. ===")

if __name__ == "__main__":
    run_pipeline()