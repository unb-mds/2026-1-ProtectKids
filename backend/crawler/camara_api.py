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
import time
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

        logger.info(
            "Buscando keyword='%s' | página %s/%s",
            keyword,
            pagina,
            LIMITE_PAGINAS,
        )

        response = fazer_requisicao_com_retry(
            ENDPOINT_PROPOSICOES,
            params=params,
            headers={"Accept": "application/json"},
            timeout=60,
        )

        if response is None:
            logger.error(
                "Falha ao buscar proposições para keyword '%s' na página %s.",
                keyword,
                pagina,
            )
            break

        try:
            dados = response.json().get("dados", [])
        except ValueError:
            logger.error(
                "Resposta inválida da API da Câmara para keyword '%s' na página %s.",
                keyword,
                pagina,
            )
            break

        if not dados:
            logger.info("Sem mais resultados para '%s' na página %s.", keyword, pagina)
            break

        for dado in dados:
            dado["_keyword_origem"] = keyword

        resultados.extend(dados)

        logger.info("%s proposições encontradas nesta página.", len(dados))

    return resultados

def fetch_proposicoes_amplas_por_ano(ano: int) -> list[dict]:
    """
    Busca proposições da Câmara por ano, sem depender de palavra-chave.

    Essa coleta existe para atender ao critério de aceitação da ETL:
    proposições com ementa genérica também devem ser capturadas,
    ter o inteiro teor baixado e ser classificadas pelo conteúdo completo.
    """
    resultados: list[dict] = []

    for pagina in range(1, LIMITE_PAGINAS + 1):
        params = {
            **PARAMS_BASE,
            "ano": ano,
            "pagina": pagina,
        }

        logger.info(
            "Buscando proposições amplas do ano %s | página %s/%s",
            ano,
            pagina,
            LIMITE_PAGINAS,
        )

        response = fazer_requisicao_com_retry(
            ENDPOINT_PROPOSICOES,
            params=params,
            headers={"Accept": "application/json"},
            timeout=60,
        )

        if response is None:
            logger.error(
                "Falha ao buscar proposições amplas do ano %s na página %s.",
                ano,
                pagina,
            )
            break

        try:
            dados = response.json().get("dados", [])
        except ValueError:
            logger.error(
                "Resposta inválida da API da Câmara na coleta ampla do ano %s.",
                ano,
            )
            break

        if not dados:
            logger.info(
                "Sem mais resultados na coleta ampla do ano %s, página %s.",
                ano,
                pagina,
            )
            break

        for dado in dados:
            dado["_keyword_origem"] = "Coleta ampla por ano"

        resultados.extend(dados)

        logger.info(
            "%s proposições encontradas na coleta ampla desta página.",
            len(dados),
        )

    return resultados

def fetch_todas_proposicoes() -> list[dict]:
    """
    Executa duas estratégias de extração:

    1. Busca por palavras-chave:
       rápida e direcionada ao tema do projeto.

    2. Busca ampla por ano:
       permite capturar proposições com ementa genérica, mas cujo texto
       integral contenha temas relevantes para proteção infantil.

    As duas listas são consolidadas removendo duplicatas pelo campo 'id'
    da API da Câmara.
    """
    todas: dict[int, dict] = {}

    for keyword in KEYWORDS:
        proposicoes = fetch_proposicoes_por_keyword(keyword)

        for prop in proposicoes:
            api_id = prop.get("id")

            if api_id and api_id not in todas:
                todas[api_id] = prop

    ano_coleta = int(os.getenv("ANO_COLETA_AMPLA", datetime.now().year))
    proposicoes_amplas = fetch_proposicoes_amplas_por_ano(ano_coleta)

    for prop in proposicoes_amplas:
        api_id = prop.get("id")

        if api_id and api_id not in todas:
            todas[api_id] = prop

    logger.info(
        "Total de proposições únicas encontradas após keyword + coleta ampla: %s",
        len(todas),
    )

    return list(todas.values())
def fetch_autor_da_proposicao(id_proposicao_api: int) -> dict:
    """
    Busca o autor principal de uma proposição da Câmara.

    Primeiro consulta /proposicoes/{id}/autores.
    Se o autor for deputado, consulta também o perfil do parlamentar
    para obter partido e UF atualizados.
    """
    url_autores = f"{BASE_URL}/proposicoes/{id_proposicao_api}/autores"

    resp_autores = fazer_requisicao_com_retry(
        url_autores,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if resp_autores is None:
        logger.warning(
            "Não foi possível buscar autores da proposição %s.",
            id_proposicao_api,
        )
        return {}

    try:
        dados_autores = resp_autores.json().get("dados", [])
    except ValueError:
        logger.warning(
            "Resposta inválida ao buscar autores da proposição %s.",
            id_proposicao_api,
        )
        return {}

    if not dados_autores:
        return {}

    autor = dados_autores[0]
    uri_autor = autor.get("uri", "")

    if "deputados" not in uri_autor:
        return autor

    resp_perfil = fazer_requisicao_com_retry(
        uri_autor,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if resp_perfil is None:
        logger.warning(
            "Não foi possível buscar perfil do autor da proposição %s.",
            id_proposicao_api,
        )
        return autor

    try:
        perfil = resp_perfil.json().get("dados", {})
    except ValueError:
        logger.warning(
            "Resposta inválida ao buscar perfil do autor da proposição %s.",
            id_proposicao_api,
        )
        return autor

    status = perfil.get("ultimoStatus", {})

    autor["siglaPartido"] = status.get("siglaPartido", "ND")
    autor["siglaUf"] = status.get("siglaUf", "ND")

    return autor

def fetch_detalhes_proposicao(id_proposicao_api: int) -> dict:
    url_detalhes = f"{BASE_URL}/proposicoes/{id_proposicao_api}"

    resp = fazer_requisicao_com_retry(
        url_detalhes,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if resp is None:
        logger.warning("Não foi possível buscar detalhes da proposição %s.", id_proposicao_api)
        return {}

    try:
        return resp.json().get("dados", {})
    except ValueError:
        logger.warning("Resposta inválida ao buscar detalhes da proposição %s.", id_proposicao_api)
        return {}
    
def fazer_requisicao_com_retry(
    url: str,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: int = 30,
    max_tentativas: int = 3,
    espera_inicial: int = 2,
) -> Optional[requests.Response]:
    """
    Executa uma requisição HTTP GET com retry simples.

    Retorna:
    - Response em caso de sucesso;
    - None em caso de falha definitiva.
    """
    for tentativa in range(1, max_tentativas + 1):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            if 400 <= response.status_code < 500:
                logger.warning(
                    "Erro cliente %s ao acessar %s. Sem retry.",
                    response.status_code,
                    url,
                )
                return None

            response.raise_for_status()
            return response

        except requests.Timeout:
            logger.warning(
                "Timeout ao acessar %s. Tentativa %s/%s.",
                url,
                tentativa,
                max_tentativas,
            )

        except requests.RequestException as exc:
            logger.warning(
                "Erro HTTP ao acessar %s. Tentativa %s/%s. Erro: %s",
                url,
                tentativa,
                max_tentativas,
                exc,
            )

        if tentativa < max_tentativas:
            espera = espera_inicial * tentativa
            logger.info("Aguardando %s segundos antes de tentar novamente.", espera)
            time.sleep(espera)

    logger.error("Falha definitiva ao acessar %s.", url)
    return None

def extrair_texto_pdf(url_pdf: Optional[str]) -> str:
    """
    Baixa um PDF e extrai seu texto usando PyMuPDF.

    A função usa arquivo temporário e garante limpeza com finally,
    evitando que arquivos fiquem acumulados em caso de erro.
    """
    if not url_pdf:
        return ""

    temp_pdf_path = None

    try:
        response = fazer_requisicao_com_retry(url_pdf, timeout=30)

        if response is None:
            return ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        texto = ""

        with fitz.open(temp_pdf_path) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()

        return texto.strip()

    except Exception as exc:
        logger.error("Erro ao extrair texto do PDF %s: %s", url_pdf, exc)
        return ""

    finally:
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except OSError as exc:
                logger.warning(
                    "Não foi possível remover arquivo temporário %s: %s",
                    temp_pdf_path,
                    exc,
                )

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

def contem_indicador_protecao_infantil(
    texto: Optional[str],
    ementa: Optional[str],
) -> bool:
    """
    Verifica se a proposição possui algum indício mínimo de relação
    com proteção infantil.

    Esse filtro é usado principalmente para a coleta ampla, evitando que
    proposições sem relação com o tema sejam salvas apenas porque foram
    capturadas por ano.
    """
    conteudo = normalizar_texto(f"{ementa or ''} {texto or ''}")

    if not conteudo:
        return False

    termos_chave = [normalizar_texto(termo) for termo in KEYWORDS]

    return any(termo and termo in conteudo for termo in termos_chave)

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
            id_autor = int(uri.rstrip("/").split("/")[-1])
        except (ValueError, IndexError):
            logger.warning("Não foi possível extrair ID do autor pela URI: %s", uri)
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
        except ValueError:
            logger.warning("Data de apresentação inválida: %s", data_str)

    url_pdf = dado_bruto.get("urlInteiroTeor")
    texto_pdf = extrair_texto_pdf(url_pdf)
    classificacao_ia = classificar_com_ia(texto_pdf, ementa)
    subtema_origem = dado_bruto.get("_keyword_origem", "Geral")

    foi_coleta_ampla = subtema_origem == "Coleta ampla por ano"

    if (
        foi_coleta_ampla
        and classificacao_ia == CATEGORIA_PADRAO
        and not contem_indicador_protecao_infantil(texto_pdf, ementa)
    ):
        logger.info(
            "Proposição Câmara %s descartada: coleta ampla sem indício de proteção infantil.",
            id_externo_formatado,
        )
        return None

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