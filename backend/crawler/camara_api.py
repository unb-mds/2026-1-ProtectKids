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
from typing import Optional
from sqlmodel import select, Session, SQLModel
from datetime import datetime
import requests
import pdfplumber
import spacy

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
    "infância", 
    "ECA", 
    "menor", 
    "proteção infantil",
    "cyberbullying",
    "adoção",
    "trabalho infantil"
]

# Parâmetros fixos da busca
PARAMS_BASE = {
    "siglaTipo": "PL",          # Somente Projetos de Lei
    "itens": 20,                 # Resultados por página
    "ordem": "DESC",
    "ordenarPor": "id",
}

# Número máximo de páginas a buscar por palavra-chave (evita explosão de dados)
MAX_PAGES = 3

# ---------------------------------------------------------------------------
# CAMADA DE FETCH — busca dados na API externa e extrai documentos
# ---------------------------------------------------------------------------

def fetch_proposicoes_por_keyword(keyword: str) -> list[dict]:
    """
    Consulta a API da Câmara buscando proposições que contenham `keyword`
    na ementa. Pagina automaticamente até MAX_PAGES.
    Injeta a palavra-chave usada dentro do dicionário para rastreamento posterior.
    """
    resultados: list[dict] = []

    for pagina in range(1, MAX_PAGES + 1):
        params = {
            **PARAMS_BASE,
            "keywords": keyword,
            "pagina": pagina,
        }

        logger.info(f"Buscando keyword='{keyword}' | página {pagina}/{MAX_PAGES}")

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
    Faz o download do PDF do inteiro teor de forma temporária,
    extrai todo o conteúdo de texto e deleta o arquivo local de cache.
    """
    if not url_pdf:
        return None
    
    try:
        logger.info(f"Baixando PDF para extração: {url_pdf}")
        resposta = requests.get(url_pdf, timeout=30)
        resposta.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(resposta.content)
            temp_pdf_path = temp_pdf.name
            
        texto_extraido = ""
        with pdfplumber.open(temp_pdf_path) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
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

def classificar_com_ia(texto: Optional[str], ementa: str) -> str:
    """
    Utiliza o spaCy para mapear semanticamente o contexto léxico da lei.
    Caso o PDF falhe, analisa o texto estruturado da ementa.
    """
    texto_analise = texto if texto else ementa
    if not texto_analise:
        return "Proteção Geral"
        
    doc = nlp(texto_analise.lower())
    
    # Mapeamento taxonômico semântico do ProtectKids
    categorias = {
        "Cyberbullying e Crimes Virtuais": ["internet", "cyberbullying", "ofensa", "rede", "digital", "computador", "virtual", "crimes"],
        "Adoção e Orfanatos": ["adoção", "adotar", "órfão", "abrigo", "família", "destituição"],
        "Violência e Abuso": ["violência", "abuso", "exploração", "maus-tratos", "agressão", "sexual", "física"],
        "Educação e Cultura": ["escola", "ensino", "professor", "merenda", "didático", "creche", "colégio"]
    }
    
    contagem_pesos = {cat: 0 for cat in categorias}
    
    # Varre os lemas (raízes linguísticas) identificados pela IA
    for token in doc:
        lema = token.lemma_
        for categoria, termos in categorias.items():
            if lema in termos:
                contagem_pesos[categoria] += 1
                
    # Retorna a categoria com maior relevância textual identificada
    categoria_vencedora = max(contagem_pesos, key=contagem_pesos.get)
    if contagem_pesos[categoria_vencedora] > 0:
        return categoria_vencedora
        
    return "Proteção Geral"


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
        
    id_externo = dado_bruto.get("id")
    
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
        id_externo=id_externo,
        id_autor=id_autor,
        tipo=sigla,
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf,
        subtema=subtema_origem,
        texto_integral=texto_pdf,
        classificacao_nlp=classificacao_ia
    )
    
    return (proposicao, parlamentar)


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


def run_pipeline() -> None:
    logger.info("=== Iniciando pipeline ETL Inteligente (PDF + NLP) ===")
    logger.info("Verificando/Criando tabelas no banco de dados...")
    SQLModel.metadata.create_all(engine)

    # 1. EXTRACT
    dados_brutos = fetch_todas_proposicoes()
    if not dados_brutos:
        logger.warning("Nenhuma proposição capturada na extração externa.")
        return

# 2. TRANSFORM
    tuplas: list[tuple] = []
    for dado in dados_brutos:
        id_prop = dado.get("id")
        
        # Faz as chamadas extras necessárias
        autor_bruto = fetch_autor_da_proposicao(id_prop)
        detalhes_brutos = fetch_detalhes_proposicao(id_prop)
        
        # Injeta o link do PDF no dado antes de transformar
        dado["urlInteiroTeor"] = detalhes_brutos.get("urlInteiroTeor")
        
        resultado = transform_proposicao(dado, autor_bruto)
        if resultado:
            tuplas.append(resultado)
            
    # 3. LOAD
    total_salvo = save_proposicoes(tuplas)
    logger.info(f"=== Pipeline concluído. {total_salvo} novos registros inseridos com NLP. ===")


if __name__ == "__main__":
    run_pipeline()