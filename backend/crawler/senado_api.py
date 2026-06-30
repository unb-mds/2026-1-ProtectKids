"""
crawler/senado_api.py

Pipeline ETL — Senado Federal → PostgreSQL
Busca matérias legislativas relacionadas à proteção infantil no ambiente digital,
baixa os PDFs, extrai o texto integral, classifica via NLP e salva no banco.
"""

import sys
import os
import logging
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, SQLModel
import concurrent.futures
import hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Proposicao, Parlamentar

from crawler.camara_api import (
    KEYWORDS,
    TEMA_PADRAO,
    esta_no_escopo_protectkids,
    classificar_com_ia,
    save_proposicoes,
    extrair_texto_pdf,
    fazer_requisicao_com_retry,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

BASE_URL_SENADO = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"

ANO_INICIO_COLETA = int(os.getenv("ANO_INICIO_COLETA", 2015))
ANO_FIM_COLETA = int(os.getenv("ANO_FIM_COLETA", datetime.now().year))


def find_value(obj, target_key: str):
    """
    Busca recursivamente por uma chave no JSON,
    ignorando maiúsculas/minúsculas e estruturas aninhadas.
    """
    if isinstance(obj, dict):
        for chave, valor in obj.items():
            if chave.lower() == target_key.lower():
                return valor

            resultado = find_value(valor, target_key)

            if resultado is not None:
                return resultado

    elif isinstance(obj, list):
        for item in obj:
            resultado = find_value(item, target_key)

            if resultado is not None:
                return resultado

    return None


def extrair_materias_resposta_senado(dados: dict) -> list[dict]:
    """
    Extrai a lista de matérias da resposta da API do Senado.

    A API pode retornar uma única matéria como dict ou várias matérias como list.
    Esta função normaliza sempre para list[dict].
    """
    materias = (
        dados
        .get("PesquisaBasicaMateria", {})
        .get("Materias", {})
        .get("Materia", [])
    )

    if isinstance(materias, dict):
        materias = [materias]

    if not isinstance(materias, list):
        return []

    return materias


def fetch_proposicoes_senado(keyword: str) -> list[dict]:
    """
    Consulta a API do Senado por palavra-chave, varrendo ano a ano.

    Essa estratégia evita a coleta ampla por ano, que gerava falsos positivos,
    mas mantém cobertura histórica desde ANO_INICIO_COLETA.
    """
    resultados: list[dict] = []
    headers = {"Accept": "application/json"}

    for ano in range(ANO_FIM_COLETA, ANO_INICIO_COLETA - 1, -1):
        params = {
            "palavraChave": keyword,
            "ano": ano,
        }

        logger.info(
            "Buscando Senado | keyword='%s' | ano=%s",
            keyword,
            ano,
        )

        resp = fazer_requisicao_com_retry(
            BASE_URL_SENADO,
            params=params,
            headers=headers,
            timeout=30,
        )

        if resp is None:
            logger.warning(
                "Falha ao buscar Senado para keyword='%s', ano=%s.",
                keyword,
                ano,
            )
            continue

        try:
            dados = resp.json()
        except ValueError:
            logger.warning(
                "Resposta inválida do Senado para keyword='%s', ano=%s.",
                keyword,
                ano,
            )
            continue

        materias = extrair_materias_resposta_senado(dados)

        if not materias:
            continue

        for materia in materias:
            materia["_keyword_origem"] = keyword

        resultados.extend(materias)

        logger.info(
            "%s matérias encontradas no Senado | keyword='%s' | ano=%s.",
            len(materias),
            keyword,
            ano,
        )

    return resultados


def fetch_todas_materias_senado() -> list[dict]:
    """
    Executa a extração principal do Senado usando apenas palavras-chave + ano.

    A coleta ampla por ano foi removida porque trazia matérias fora do escopo
    do ProtectKids, como temas digitais genéricos sem relação com crianças
    ou adolescentes.
    """
    todas: dict[str, dict] = {}

    for keyword in KEYWORDS:
        materias = fetch_proposicoes_senado(keyword)

        for materia in materias:
            codigo = find_value(materia, "Codigo")

            if codigo and str(codigo) not in todas:
                todas[str(codigo)] = materia

    logger.info(
        "Total de matérias únicas do Senado encontradas por palavras-chave: %s",
        len(todas),
    )

    return list(todas.values())


def gerar_id_autor_senado(nome_autor: str) -> int:
    """
    Gera um identificador estável para autores do Senado quando a API
    não fornece um ID numérico confiável.

    Usa uma faixa alta para reduzir conflito com IDs reais da Câmara,
    mas sem ultrapassar o limite de INTEGER do PostgreSQL.
    """
    nome_normalizado = nome_autor.strip().lower()

    if not nome_normalizado:
        nome_normalizado = "autor-desconhecido-senado"

    digest = hashlib.sha256(nome_normalizado.encode("utf-8")).hexdigest()
    valor_hash = int(digest[:8], 16)

    return 1_000_000_000 + (valor_hash % 900_000_000)


def transform_materia_senado(materia_bruta: dict) -> Optional[tuple]:
    """
    Transforma uma matéria bruta do Senado em Proposicao + Parlamentar.
    """
    codigo_materia = find_value(materia_bruta, "Codigo")

    if not codigo_materia:
        return None

    id_externo_formatado = f"senado-{codigo_materia}"

    sigla = find_value(materia_bruta, "Sigla") or "PL"
    numero = find_value(materia_bruta, "Numero") or 0
    ano = find_value(materia_bruta, "Ano") or ANO_FIM_COLETA

    ementa = find_value(materia_bruta, "Ementa") or "Sem ementa disponível"
    ementa = str(ementa).strip()

    if not ementa or ementa == "Sem ementa disponível":
        logger.info(
            "Matéria Senado %s descartada: sem ementa disponível.",
            id_externo_formatado,
        )
        return None

    autor_string = find_value(materia_bruta, "Autor") or "Desconhecido"
    nome_autor = autor_string
    partido = "ND"
    uf = "ND"

    if "(" in autor_string and ")" in autor_string:
        partes = autor_string.split("(")
        nome_autor = partes[0].strip()

        partido_uf = partes[1].replace(")", "").split("/")

        if len(partido_uf) == 2:
            partido = partido_uf[0].strip()
            uf = partido_uf[1].strip()

    id_autor = gerar_id_autor_senado(nome_autor)

    parlamentar = Parlamentar(
        id_parlamentar=id_autor,
        nome=nome_autor,
        partido=partido,
        uf=uf,
    )

    data_apres = None
    data_str = find_value(materia_bruta, "Data")

    if data_str:
        try:
            data_apres = datetime.fromisoformat(str(data_str)[:10]).date()
        except ValueError:
            logger.warning(
                "Data de apresentação inválida no Senado: %s",
                data_str,
            )

    subtema_origem = materia_bruta.get("_keyword_origem", "Geral")

    url_pdf_real = (
        "https://legis.senado.leg.br/sdleg-getter/documento/download/materia/"
        f"{codigo_materia}"
    )

    texto_pdf = extrair_texto_pdf(url_pdf_real) or ""

    if not texto_pdf:
        texto_pdf = (
            "O texto integral desta matéria está indisponível para extração digital.\n\n"
            f"Ementa Original: {ementa}"
        )

    if not esta_no_escopo_protectkids(
        texto=texto_pdf,
        ementa=ementa,
    ):
        logger.info(
            "Matéria Senado %s descartada: fora do escopo ProtectKids. Ementa: %s",
            id_externo_formatado,
            ementa[:180],
        )
        return None

    classificacao_ia = classificar_com_ia(
        texto=texto_pdf,
        ementa=ementa,
    )

    proposicao = Proposicao(
        id_externo=id_externo_formatado,
        origem="Senado",
        id_autor=id_autor,
        tipo=str(sigla),
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        tema=TEMA_PADRAO,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf_real,
        subtema=subtema_origem,
        texto_integral=texto_pdf,
        classificacao_nlp=classificacao_ia,
    )

    return (proposicao, parlamentar)


def obter_ids_existentes(origem_alvo: str) -> set:
    """
    Busca no banco todos os IDs externos já cadastrados para evitar
    reprocessamento de NLP.
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(
            Proposicao.origem == origem_alvo
        )
        resultados = session.exec(statement).all()

        return set(resultados)


def run_pipeline_senado() -> None:
    logger.info("=== Iniciando pipeline ETL do Senado Inteligente ===")
    SQLModel.metadata.create_all(engine)

    ids_existentes = obter_ids_existentes(origem_alvo="Senado")
    logger.info(
        "Cache local: %s proposições do Senado já existem no banco.",
        len(ids_existentes),
    )

    tuplas: list[tuple] = []
    ids_processados_nesta_run = set()
    materias_ineditas = []

    materias_brutas = fetch_todas_materias_senado()

    for materia in materias_brutas:
        codigo = find_value(materia, "Codigo")

        if not codigo:
            continue

        id_externo_formatado = f"senado-{codigo}"

        if (
            id_externo_formatado in ids_existentes
            or id_externo_formatado in ids_processados_nesta_run
        ):
            continue

        ids_processados_nesta_run.add(id_externo_formatado)
        materias_ineditas.append(materia)

    if not materias_ineditas:
        logger.info(
            "=== Pipeline do Senado concluído. Nenhuma matéria inédita para processar hoje. ==="
        )
        return

    logger.info(
        "Iniciando download paralelo de %s PDFs do Senado...",
        len(materias_ineditas),
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {
            executor.submit(transform_materia_senado, materia): materia
            for materia in materias_ineditas
        }

        for futuro in concurrent.futures.as_completed(futuros):
            materia = futuros[futuro]
            codigo = find_value(materia, "Codigo") or "desconhecido"

            try:
                resultado = futuro.result()
            except Exception:
                logger.exception(
                    "Erro ao processar matéria do Senado %s em paralelo.",
                    codigo,
                )
                continue

            if resultado:
                tuplas.append(resultado)

    if tuplas:
        total_salvo = save_proposicoes(tuplas)

        logger.info(
            "=== Pipeline do Senado concluído. %s registros normalizados salvos. ===",
            total_salvo,
        )
    else:
        logger.info(
            "=== Pipeline do Senado concluído. Nenhuma matéria nova processada. ==="
        )


if __name__ == "__main__":
    run_pipeline_senado()