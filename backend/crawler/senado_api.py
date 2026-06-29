"""
crawler/senado_api.py

Pipeline ETL — Senado Federal → PostgreSQL
"""
import sys
import os
import logging
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, SQLModel
import concurrent.futures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar
import hashlib

from crawler.camara_api import (
    KEYWORDS,
    TEMA_PADRAO,
    CATEGORIA_PADRAO,
    classificar_com_ia,
    save_proposicoes,
    extrair_texto_pdf,
    fazer_requisicao_com_retry,
    contem_indicador_protecao_infantil,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL_SENADO = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"
SIGLAS_SENADO_COLETA = ["PL", "PLS", "PLC", "PEC"]
ANO_COLETA_AMPLA_SENADO = int(
    os.getenv("ANO_COLETA_AMPLA_SENADO", datetime.now().year)
)

def find_value(obj, target_key: str):
    """Busca recursivamente por uma chave no JSON, ignorando maiúsculas/minúsculas e aninhamentos."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == target_key.lower():
                return v
            res = find_value(v, target_key)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_value(item, target_key)
            if res is not None:
                return res
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
    Consulta a API do Senado buscando matérias pela palavra-chave informada.
    """
    params = {"palavraChave": keyword}
    headers = {"Accept": "application/json"}

    logger.info("Buscando no Senado pela keyword: '%s'", keyword)

    resp = fazer_requisicao_com_retry(
        BASE_URL_SENADO,
        params=params,
        headers=headers,
        timeout=30,
    )

    if resp is None:
        logger.error("Falha ao buscar matérias no Senado para '%s'.", keyword)
        return []

    try:
        dados = resp.json()
    except ValueError:
        logger.error("Resposta inválida da API do Senado para '%s'.", keyword)
        return []

    materias = extrair_materias_resposta_senado(dados)

    if not materias:
        logger.info("Nenhuma matéria encontrada no Senado para '%s'.", keyword)
        return []

    for materia in materias:
        materia["_keyword_origem"] = keyword

    logger.info(
        "Encontradas %s matérias no Senado para '%s'.",
        len(materias),
        keyword,
    )

    return materias

def fetch_proposicoes_senado_por_ano(ano: int) -> list[dict]:
    """
    Busca matérias do Senado por ano e sigla, sem depender de palavra-chave.

    Essa coleta ampla atende ao critério de aceitação da ETL:
    matérias com ementa genérica também devem ser capturadas,
    ter o texto integral baixado e ser classificadas pelo conteúdo completo.
    """
    resultados: list[dict] = []
    headers = {"Accept": "application/json"}

    for sigla in SIGLAS_SENADO_COLETA:
        params = {
            "sigla": sigla,
            "ano": ano,
        }

        logger.info(
            "Buscando matérias amplas no Senado | sigla=%s | ano=%s",
            sigla,
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
                "Falha na coleta ampla do Senado para sigla=%s, ano=%s.",
                sigla,
                ano,
            )
            continue

        try:
            dados = resp.json()
        except ValueError:
            logger.warning(
                "Resposta inválida na coleta ampla do Senado para sigla=%s, ano=%s.",
                sigla,
                ano,
            )
            continue

        materias = extrair_materias_resposta_senado(dados)

        if not materias:
            logger.info(
                "Nenhuma matéria ampla encontrada no Senado para sigla=%s, ano=%s.",
                sigla,
                ano,
            )
            continue

        for materia in materias:
            materia["_keyword_origem"] = "Coleta ampla por ano"

        resultados.extend(materias)

        logger.info(
            "%s matérias encontradas na coleta ampla do Senado para sigla=%s, ano=%s.",
            len(materias),
            sigla,
            ano,
        )

    return resultados

def fetch_todas_materias_senado() -> list[dict]:
    """
    Executa duas estratégias de extração no Senado:

    1. Busca por palavras-chave;
    2. Busca ampla por ano e sigla.

    Remove duplicatas pelo Código da matéria.
    """
    todas: dict[str, dict] = {}

    # Estratégia 1: busca por keywords
    for keyword in KEYWORDS:
        materias = fetch_proposicoes_senado(keyword)

        for materia in materias:
            codigo = find_value(materia, "Codigo")

            if codigo and str(codigo) not in todas:
                todas[str(codigo)] = materia

    # Estratégia 2: coleta ampla
    materias_amplas = fetch_proposicoes_senado_por_ano(ANO_COLETA_AMPLA_SENADO)

    for materia in materias_amplas:
        codigo = find_value(materia, "Codigo")

        if codigo and str(codigo) not in todas:
            todas[str(codigo)] = materia

    logger.info(
        "Total de matérias únicas do Senado após keyword + coleta ampla: %s",
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
    """O Adaptador resiliente atualizado com as chaves reais do Senado."""
    codigo_materia = find_value(materia_bruta, "Codigo")
    if not codigo_materia:
        return None
        
    id_externo_formatado = f"senado-{codigo_materia}"
    
    sigla = find_value(materia_bruta, "Sigla") or "PL"
    numero = find_value(materia_bruta, "Numero") or 0
    ano = find_value(materia_bruta, "Ano") or 2026
    
    ementa = find_value(materia_bruta, "Ementa") or "Sem ementa disponível"
    ementa = str(ementa).strip()

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
        uf=uf
    )
        
    data_apres = None
    data_str = find_value(materia_bruta, "Data")
    if data_str:
        try:
            data_apres = datetime.fromisoformat(str(data_str)[:10]).date()
        except ValueError:
            logger.warning("Data de apresentação inválida no Senado: %s", data_str)
        
    subtema_origem = materia_bruta.get("_keyword_origem", "Geral")
    url_pdf_real = f"https://legis.senado.leg.br/sdleg-getter/documento/download/materia/{codigo_materia}"
    
    texto_pdf = extrair_texto_pdf(url_pdf_real)

    if not texto_pdf:
        texto_pdf = (
            "O texto integral desta matéria está indisponível para extração digital.\n\n"
            f"Ementa Original: {ementa}"
        )
    classificacao_ia = classificar_com_ia(texto=texto_pdf, ementa=ementa)
    foi_coleta_ampla = subtema_origem == "Coleta ampla por ano"

    if (
        foi_coleta_ampla
        and classificacao_ia == CATEGORIA_PADRAO
        and not contem_indicador_protecao_infantil(texto_pdf, ementa)
    ):
        logger.info(
            "Matéria Senado %s descartada: coleta ampla sem indício de proteção infantil.",
            id_externo_formatado,
        )
        return None
    
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
    o reprocessamento de NLP.
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(Proposicao.origem == origem_alvo)
        resultados = session.exec(statement).all()
        return set(resultados)

def run_pipeline_senado():
    logger.info("=== Iniciando pipeline ETL do Senado Inteligente ===")
    SQLModel.metadata.create_all(engine)

    ids_existentes = obter_ids_existentes(origem_alvo="Senado")
    logger.info(
        "Cache local: %s proposições do Senado já existem no banco.",
        len(ids_existentes),
    )

    tuplas = []
    ids_processados_nesta_run = set()
    materias_ineditas = []

        # 1. EXTRACT: coleta por keyword + coleta ampla por ano
    materias_brutas = fetch_todas_materias_senado()

    for mat in materias_brutas:
        codigo = find_value(mat, "Codigo")

        if not codigo:
            continue

        id_externo_formatado = f"senado-{codigo}"

        if (
            id_externo_formatado in ids_existentes
            or id_externo_formatado in ids_processados_nesta_run
        ):
            continue

        ids_processados_nesta_run.add(id_externo_formatado)
        materias_ineditas.append(mat)

    if not materias_ineditas:
        logger.info(
            "=== Pipeline do Senado concluído. Nenhuma matéria inédita para processar hoje. ==="
        )
        return

    logger.info(
        "Iniciando download paralelo de %s PDFs do Senado...",
        len(materias_ineditas),
    )

    # Dispara downloads e processamento em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {
            executor.submit(transform_materia_senado, mat): mat
            for mat in materias_ineditas
        }

        for futuro in concurrent.futures.as_completed(futuros):
            materia = futuros[futuro]
            codigo = find_value(materia, "Codigo") or "desconhecido"

            try:
                resultado = futuro.result()
            except Exception as exc:
                logger.error(
                    "Erro ao processar matéria do Senado %s em paralelo: %s",
                    codigo,
                    exc,
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