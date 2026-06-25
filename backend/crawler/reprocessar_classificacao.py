"""
Reprocessa a classificação NLP das proposições já existentes no banco.

Uso dentro do container:
    python -m crawler.reprocessar_classificacao
"""

import logging
import os
import sys

from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Proposicao
from crawler.camara_api import TEMA_PADRAO, classificar_com_ia

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def reprocessar_classificacoes() -> None:
    with Session(engine) as session:
        proposicoes = session.exec(select(Proposicao)).all()

        if not proposicoes:
            logger.info("Nenhuma proposição encontrada no banco.")
            return

        total_atualizadas = 0

        for prop in proposicoes:
            classificacao_antiga = prop.classificacao_nlp
            tema_antigo = prop.tema

            nova_classificacao = classificar_com_ia(
                texto=prop.texto_integral,
                ementa=prop.ementa,
            )

            prop.classificacao_nlp = nova_classificacao
            prop.tema = TEMA_PADRAO

            if (
                classificacao_antiga != nova_classificacao
                or tema_antigo != TEMA_PADRAO
            ):
                total_atualizadas += 1
                logger.info(
                    "Atualizada %s: '%s' -> '%s'",
                    prop.id_externo,
                    classificacao_antiga,
                    nova_classificacao,
                )

            session.add(prop)

        session.commit()

        logger.info(
            "Reprocessamento concluído. %s proposições atualizadas de um total de %s.",
            total_atualizadas,
            len(proposicoes),
        )


if __name__ == "__main__":
    reprocessar_classificacoes()