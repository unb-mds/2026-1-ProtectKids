"""
crawler/tramitacoes_api.py

Pipeline ETL — Tramitações da Câmara dos Deputados → PostgreSQL

Busca o histórico de tramitações das proposições da Câmara já existentes
no banco de dados e atualiza a tabela de tramitações.

Uso:
    # A partir da pasta backend/
    python -m crawler.tramitacoes_api
"""

import sys
import os
import logging
from datetime import datetime
from typing import Optional
import concurrent.futures

from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Proposicao, Tramitacao
from crawler.camara_api import fazer_requisicao_com_retry


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

BASE_URL_CAMARA = "https://dadosabertos.camara.leg.br/api/v2"
MAX_WORKERS_TRAMITACOES = int(os.getenv("MAX_WORKERS_TRAMITACOES", 5))


def buscar_ids_camara_no_banco() -> list[str]:
    """
    Busca no banco apenas os IDs externos das proposições da Câmara.

    Exemplos de retorno:
    - camara-2634854
    - camara-1234567
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(
            Proposicao.origem.in_(["Camara", "Câmara"])
        )

        resultados = session.exec(statement).all()

        return list(resultados)


def extrair_id_numerico_camara(id_externo: str) -> Optional[str]:
    """
    Extrai o ID numérico de um id_externo no formato camara-123456.

    Retorna None se o formato estiver inválido.
    """
    if not id_externo or not id_externo.startswith("camara-"):
        return None

    partes = id_externo.split("-", maxsplit=1)

    if len(partes) != 2 or not partes[1]:
        return None

    return partes[1]


def parse_data_hora_tramitacao(data_str: Optional[str]) -> datetime:
    """
    Converte a data/hora retornada pela API da Câmara em datetime.

    Se a data vier inválida ou vazia, usa datetime.now() como fallback.
    """
    if not data_str:
        return datetime.now()

    try:
        data_normalizada = str(data_str).replace("Z", "+00:00")
        data_hora = datetime.fromisoformat(data_normalizada)

        if data_hora.tzinfo is not None:
            data_hora = data_hora.replace(tzinfo=None)

        return data_hora

    except ValueError:
        logger.warning("Data de tramitação inválida: %s", data_str)
        return datetime.now()


def fetch_tramitacoes_brutas(id_camara_numerico: str) -> Optional[list[dict]]:
    """
    Busca na API da Câmara a linha do tempo bruta de tramitações.

    Retorno:
    - list[dict]: requisição bem-sucedida, com ou sem tramitações;
    - None: falha de rede, erro HTTP ou resposta inválida.

    Essa diferença é importante para evitar apagar dados antigos quando
    a API falhar temporariamente.
    """
    url = f"{BASE_URL_CAMARA}/proposicoes/{id_camara_numerico}/tramitacoes"

    resp = fazer_requisicao_com_retry(
        url,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if resp is None:
        logger.warning(
            "Não foi possível buscar tramitações para %s.",
            id_camara_numerico,
        )
        return None

    try:
        dados = resp.json().get("dados", [])
    except ValueError:
        logger.warning(
            "Resposta inválida ao buscar tramitações para %s.",
            id_camara_numerico,
        )
        return None

    if not isinstance(dados, list):
        logger.warning(
            "Formato inesperado de tramitações para %s.",
            id_camara_numerico,
        )
        return None

    return dados


def processar_tramitacoes_individuais(
    id_externo: str,
) -> tuple[str, Optional[list[Tramitacao]]]:
    """
    Processa as tramitações de uma proposição da Câmara.

    Retorno:
    - (id_externo, list[Tramitacao]): busca bem-sucedida;
    - (id_externo, None): falha na busca/processamento.
    """
    id_numerico = extrair_id_numerico_camara(id_externo)

    if not id_numerico:
        logger.warning("ID externo inválido para tramitação: %s", id_externo)
        return id_externo, None

def processar_tramitacoes_individuais(
    id_externo: str,
) -> tuple[str, list[Tramitacao] | None]:
    id_numerico = id_externo.split("-")[1]
    dados_brutos = fetch_tramitacoes_brutas(id_numerico)

    if dados_brutos is None:
        return id_externo, None

    tramitacoes_processadas: list[Tramitacao] = []

    for dado in dados_brutos:
        data_hora_formatada = parse_data_hora_tramitacao(
            dado.get("dataHora")
        )

        nova_tramitacao = Tramitacao(
            id_proposicao_externo=id_externo,
            data_hora=data_hora_formatada,
            orgao=dado.get("siglaOrgao") or "Não Identificado",
            descricao=dado.get("descricaoTramitacao") or "Sem descrição",
        )

        tramitacoes_processadas.append(nova_tramitacao)

    return id_externo, tramitacoes_processadas

def substituir_tramitacoes_no_banco(
    tramitacoes_por_id: dict[str, list[Tramitacao]],
) -> int:
    """
    Substitui as tramitações antigas apenas das proposições que foram
    consultadas com sucesso.

    Isso evita apagar histórico antigo de proposições cuja consulta falhou.
    """
    total_salvo = 0

    with Session(engine) as session:
        for id_externo, novas_tramitacoes in tramitacoes_por_id.items():
            statement = select(Tramitacao).where(
                Tramitacao.id_proposicao_externo == id_externo
            )

            tramitacoes_antigas = session.exec(statement).all()

            for tramitacao_antiga in tramitacoes_antigas:
                session.delete(tramitacao_antiga)

            if novas_tramitacoes:
                session.add_all(novas_tramitacoes)
                total_salvo += len(novas_tramitacoes)

        session.commit()

    return total_salvo


def run_pipeline_tramitacoes() -> None:
    logger.info("=== Iniciando crawler de tramitações da Câmara ===")

    ids_banco = buscar_ids_camara_no_banco()

    if not ids_banco:
        logger.warning(
            "Nenhuma proposição da Câmara encontrada no banco. "
            "Rode o camara_api.py primeiro."
        )
        return

    logger.info(
        "Buscando histórico de tramitações para %s proposições da Câmara.",
        len(ids_banco),
    )

    tramitacoes_por_id: dict[str, list[Tramitacao]] = {}

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS_TRAMITACOES
    ) as executor:
        futuros = {
            executor.submit(processar_tramitacoes_individuais, id_externo): id_externo
            for id_externo in ids_banco
        }

        for futuro in concurrent.futures.as_completed(futuros):
            id_externo = futuros[futuro]

            try:
                id_processado, resultado = futuro.result()
            except Exception:
                logger.exception(
                    "Erro inesperado ao processar tramitações de %s.",
                    id_externo,
                )
                continue

            if resultado is None:
                logger.warning(
                    "Tramitações de %s não foram atualizadas por falha na consulta.",
                    id_processado,
                )
                continue

            tramitacoes_por_id[id_processado] = resultado

    if not tramitacoes_por_id:
        logger.warning(
            "Nenhuma tramitação foi atualizada. "
            "Possível falha geral na API da Câmara."
        )
        return

    total_salvo = substituir_tramitacoes_no_banco(tramitacoes_por_id)

    logger.info(
        "=== Crawler de tramitações concluído. "
        "%s proposições atualizadas; %s passos de tramitação salvos. ===",
        len(tramitacoes_por_id),
        total_salvo,
    )


if __name__ == "__main__":
    run_pipeline_tramitacoes()