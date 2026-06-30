"""
crawler/tramitacoes_api.py

Script assíncrono para buscar o histórico de tramitações das proposições
já existentes no banco de dados.
"""

import sys
import os
import logging
from datetime import datetime
from sqlmodel import Session, select
import concurrent.futures
from crawler.camara_api import fazer_requisicao_com_retry
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Tramitacao

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL_CAMARA = "https://dadosabertos.camara.leg.br/api/v2"

def buscar_ids_camara_no_banco() -> list[str]:
    """Puxa do banco apenas os IDs de matérias da Câmara."""
    with Session(engine) as session:
        # Pega os IDs externos (ex: 'camara-12345')
        statement = select(Proposicao.id_externo).where(
    Proposicao.origem.in_(["Camara", "Câmara"])
)
        return session.exec(statement).all()

def fetch_tramitacoes_brutas(id_camara_numerico: str) -> list[dict]:
    """
    Busca na API da Câmara a linha do tempo bruta de tramitações
    de uma proposição.

    Usa fazer_requisicao_com_retry para tratar timeout,
    falhas temporárias de rede e erros HTTP de forma padronizada.
    """
    url = f"{BASE_URL_CAMARA}/proposicoes/{id_camara_numerico}/tramitacoes"

    try:
        resp = fazer_requisicao_com_retry(
            url,
            headers={"Accept": "application/json"},
            timeout=30,
        )

        if resp is None:
            logger.warning(
                "Não foi possível buscar tramitações para %s na URL %s.",
                id_camara_numerico,
                url,
            )
            return []

        if 400 <= resp.status_code < 500:
            logger.warning(
                "Erro cliente %s ao buscar tramitações para %s.",
                resp.status_code,
                id_camara_numerico,
            )
            return []

        try:
            return resp.json().get("dados", [])
        except ValueError:
            logger.warning(
                "Resposta inválida ao buscar tramitações para %s.",
                id_camara_numerico,
            )
            return []

    except Exception as exc:
        logger.warning(
            "Falha inesperada ao buscar tramitações para %s: %s",
            id_camara_numerico,
            exc,
        )
        return []

def processar_tramitacoes_individuais(id_externo: str) -> list[Tramitacao]:
    id_numerico = id_externo.split("-")[1]
    dados_brutos = fetch_tramitacoes_brutas(id_numerico)
    tramitacoes_processadas = []

    for dado in dados_brutos:
        data_str = dado.get("dataHora")
        data_hora_formatada = datetime.now()

        if data_str:
            try:
                data_hora_formatada = datetime.fromisoformat(str(data_str))
            except ValueError:
                logger.warning(
                    "Data de tramitação inválida para %s: %s",
                    id_externo,
                    data_str,
                )

        nova_tramitacao = Tramitacao(
            id_proposicao_externo=id_externo,
            data_hora=data_hora_formatada,
            orgao=dado.get("siglaOrgao", "Não Identificado"),
            descricao=dado.get("descricaoTramitacao", "Sem descrição"),
        )

        tramitacoes_processadas.append(nova_tramitacao)

    return tramitacoes_processadas

def run_pipeline_tramitacoes():
    logger.info("=== Iniciando Crawler de Tramitações ===")
    
    ids_banco = buscar_ids_camara_no_banco()
    if not ids_banco:
        logger.warning("Nenhuma proposição da Câmara encontrada no banco. Rode o camara_api.py primeiro.")
        return
        
    logger.info(f"Buscando histórico para {len(ids_banco)} proposições...")
    
    todas_novas_tramitacoes = []
    
    # Multithreading para não demorar horas baixando o histórico
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futuros = {executor.submit(processar_tramitacoes_individuais, id_ext): id_ext for id_ext in ids_banco}
        
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                todas_novas_tramitacoes.extend(resultado)
                
    if todas_novas_tramitacoes:
        with Session(engine) as session:
            # Estratégia de limpeza: apaga o histórico antigo e salva o novo completo
            # Isso evita duplicação de dados sem precisar checar linha por linha
            for id_ext in ids_banco:
                statement = select(Tramitacao).where(Tramitacao.id_proposicao_externo == id_ext)
                tramitacoes_antigas = session.exec(statement).all()
                for t in tramitacoes_antigas:
                    session.delete(t)
            
            session.add_all(todas_novas_tramitacoes)
            session.commit()
            
        logger.info(f"=== Concluído! {len(todas_novas_tramitacoes)} passos de tramitação salvos no banco. ===")

if __name__ == "__main__":
    run_pipeline_tramitacoes()