"""
crawler/camara_api.py

Pipeline ETL — Câmara dos Deputados → PostgreSQL
Busca proposições legislativas relacionadas à proteção infantil e salva no banco.

Uso:
    # A partir da raiz do projeto (backend/)
    python -m crawler.camara_api

    # Ou diretamente, com o PYTHONPATH configurado:
    PYTHONPATH=.. python crawler/camara_api.py
"""

import sys
import os
import logging
from typing import Optional
from sqlmodel import select, Session, SQLModel
from datetime import datetime
import requests

# Garante que o módulo backend/ seja encontrado quando executado diretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar

# ---------------------------------------------------------------------------
# Configuração de logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
ENDPOINT_PROPOSICOES = f"{BASE_URL}/proposicoes"

# Palavras-chave relacionadas à proteção infantil
KEYWORDS = ["criança", "infância", "ECA", "menor", "proteção infantil"]

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
# CAMADA DE FETCH — busca dados na API externa
# ---------------------------------------------------------------------------

def fetch_proposicoes_por_keyword(keyword: str) -> list[dict]:
    """
    Consulta a API da Câmara buscando proposições que contenham `keyword`
    na ementa. Pagina automaticamente até MAX_PAGES.

    Args:
        keyword: Termo de busca (ex: "criança", "ECA").

    Returns:
        Lista de dicts com os dados brutos retornados pela API.
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

        resultados.extend(dados)
        logger.info(f"{len(dados)} proposições encontradas nesta página.")

    return resultados


def fetch_todas_proposicoes() -> list[dict]:
    """
    Executa a busca para todas as KEYWORDS e retorna uma lista consolidada,
    removendo duplicatas pelo campo 'id' da API.

    Returns:
        Lista deduplicada de proposições brutas.
    """
    todas: dict[int, dict] = {}  # id_api → dado, para deduplicação

    for keyword in KEYWORDS:
        proposicoes = fetch_proposicoes_por_keyword(keyword)
        for prop in proposicoes:
            api_id = prop.get("id")
            if api_id and api_id not in todas:
                todas[api_id] = prop

    logger.info(f"Total de proposições únicas encontradas: {len(todas)}")
    return list(todas.values())


# ---------------------------------------------------------------------------
# CAMADA DE TRANSFORM — mapeia dados da API para o modelo do sistema
# ---------------------------------------------------------------------------
def fetch_autor_da_proposicao(id_proposicao_api: int) -> dict:
    url_autores = f"{BASE_URL}/proposicoes/{id_proposicao_api}/autores"
    try:
        # 1. Descobre quem é o autor da lei
        resp_autores = requests.get(url_autores, timeout=30, headers={"Accept": "application/json"})
        resp_autores.raise_for_status()
        dados_autores = resp_autores.json().get("dados", [])
        
        if not dados_autores:
            return {}
            
        autor = dados_autores[0]
        uri_autor = autor.get("uri", "")
        
        # 2. Faz uma requisição extra no perfil do deputado para descobrir o partido
        if "deputados" in uri_autor:
            resp_perfil = requests.get(uri_autor, timeout=30, headers={"Accept": "application/json"})
            resp_perfil.raise_for_status()
            perfil = resp_perfil.json().get("dados", {})
            status = perfil.get("ultimoStatus", {})
            
            # Injeta o partido e a UF no dicionário para a função de transformação usar
            autor["siglaPartido"] = status.get("siglaPartido", "ND")
            autor["siglaUf"] = status.get("siglaUf", "ND")
            
        return autor
        
    except Exception as exc:
        logger.warning(f"Erro ao buscar autor da proposicao {id_proposicao_api}: {exc}")
        return {}

# --- Atualize a Camada de Transform ---

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
            # A API da Camara esconde o ID do deputado no final da URI
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

    # 3. Monta a Proposicao
    proposicao = Proposicao(
        id_externo=id_externo,
        id_autor=id_autor,
        tipo=sigla,
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        data_apresentacao=data_apres
    )
    
    return (proposicao, parlamentar)

# --- Atualize a Camada de Save ---
def save_proposicoes(tuplas_prop_autor: list[tuple]) -> int:
    inseridos = 0
    with Session(engine) as session:
        for prop, autor in tuplas_prop_autor:
            try:
                # 1. Salva o Autor PRIMEIRO (para respeitar a chave estrangeira)
                if autor:
                    existente_autor = session.exec(
                        select(Parlamentar).where(Parlamentar.id_parlamentar == autor.id_parlamentar)
                    ).first()
                    if not existente_autor:
                        session.add(autor)
                        session.flush() # Salva rapido para gerar o ID pro banco

                # 2. Salva a Proposicao DEPOIS
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

# --- Atualize o Pipeline Principal ---
def run_pipeline() -> None:
    logger.info("=== Iniciando pipeline ETL ===")
    logger.info("Verificando/Criando tabelas no banco de dados...")
    SQLModel.metadata.create_all(engine)

    # 1. EXTRACT
    dados_brutos = fetch_todas_proposicoes()
    if not dados_brutos:
        return

    # 2. TRANSFORM
    tuplas: list[tuple] = []
    for dado in dados_brutos:
        # ATENCAO: Nova chamada extra na API para cada lei encontrada
        autor_bruto = fetch_autor_da_proposicao(dado.get("id"))
        resultado = transform_proposicao(dado, autor_bruto)
        if resultado:
            tuplas.append(resultado)

    logger.info(f"{len(tuplas)} proposicoes prontas.")

    # 3. LOAD
    total_salvo = save_proposicoes(tuplas)
    logger.info(f"=== Pipeline concluido. {total_salvo} registros inseridos. ===")

if __name__ == "__main__":
    run_pipeline()