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
from sqlmodel import select

import requests

# Garante que o módulo backend/ seja encontrado quando executado diretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from database import engine
from models import Proposicao

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

def transform_proposicao(dado_bruto: dict) -> Optional[Proposicao]:
    """
    Converte um dict retornado pela API da Câmara no modelo Proposicao
    do nosso sistema.

    Campos da API utilizados:
        - siglaTipo + numero + ano  →  titulo  (ex: "PL 1234/2025"
        - ementa                    →  descricao

    Args:
        dado_bruto: Dict com os dados brutos de uma proposição.

    Returns:
        Instância de Proposicao pronta para ser salva, ou None se dados
        obrigatórios estiverem ausentes.
    """
    sigla = dado_bruto.get("siglaTipo", "PL")
    numero = dado_bruto.get("numero")
    ano = dado_bruto.get("ano")
    ementa = dado_bruto.get("ementa", "").strip()

    # Valida campos mínimos necessários
    if not numero or not ano or not ementa:
        logger.debug(f"Proposição ignorada por dados incompletos: {dado_bruto.get('id')}")
        return None

    titulo = f"{sigla} {numero}/{ano}"
    descricao = ementa or "Sem descrição disponível."

    return Proposicao(
        id_externo=dado_bruto.get("id"),
        titulo=titulo,
        descricao=descricao,
        tema="Proteção Infantil Digital",
    )


# ---------------------------------------------------------------------------
# CAMADA DE SAVE — persiste no PostgreSQL via SQLModel
# ---------------------------------------------------------------------------

def save_proposicoes(proposicoes: list[Proposicao]) -> int:
    """
    Insere uma lista de Proposicao no banco de dados.
    Usa uma única sessão/transação para eficiência.

    Args:
        proposicoes: Lista de instâncias de Proposicao a salvar.

    Returns:
        Número de registros efetivamente inseridos.
    """
    if not proposicoes:
        logger.info("Nenhuma proposição para salvar.")
        return 0

    inseridos = 0

    with Session(engine) as session:
        for prop in proposicoes:
            try:
                existente = session.exec(
                    select(Proposicao).where(
                        Proposicao.id_externo == prop.id_externo
                )
                ).first()

                if existente:
                    continue

                session.add(prop)
                session.flush()
                inseridos += 1
            except Exception as exc:
                logger.warning(f"Erro ao adicionar '{prop.titulo}': {exc}. Pulando.")
                session.rollback()
                # Reabre a sessão implicitamente para continuar os próximos
                continue

        session.commit()
        logger.info(f"{inseridos} proposições salvas com sucesso no banco de dados.")

    return inseridos


# ---------------------------------------------------------------------------
# PIPELINE PRINCIPAL
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    """
    Orquestra as três etapas do ETL:
        1. Extract  — busca dados na API da Câmara
        2. Transform — converte para o modelo interno
        3. Load      — salva no PostgreSQL
    """
    logger.info("=== Iniciando pipeline ETL — Câmara dos Deputados ===")

    # 1. EXTRACT
    dados_brutos = fetch_todas_proposicoes()

    if not dados_brutos:
        logger.warning("Nenhum dado retornado pela API. Encerrando pipeline.")
        return

    # 2. TRANSFORM
    proposicoes: list[Proposicao] = []
    for dado in dados_brutos:
        prop = transform_proposicao(dado)
        if prop:
            proposicoes.append(prop)

    logger.info(f"{len(proposicoes)} proposições válidas após transformação.")

    # 3. LOAD
    total_salvo = save_proposicoes(proposicoes)

    logger.info(f"=== Pipeline concluído. {total_salvo} registros inseridos. ===")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_pipeline()