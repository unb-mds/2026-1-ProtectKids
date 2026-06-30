"""
crawler/tramitacoes_senado_api.py

Pipeline ETL — Tramitações do Senado Federal → PostgreSQL.

Busca o histórico de movimentações/tramitações das matérias do Senado já
existentes no banco de dados e atualiza a tabela de tramitações.

Endpoint validado por teste manual:
https://legis.senado.leg.br/dadosabertos/materia/movimentacoes/{codigo}.json

Observação:
- O código salvo como id_externo="senado-169929" é o CodigoMateria.
- Não é o IdentificacaoProcesso/idProcesso da API nova /processo/{idProcesso}.
"""

import concurrent.futures
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Any

from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Proposicao, Tramitacao
from crawler.camara_api import fazer_requisicao_com_retry
from crawler.senado_api import find_value


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


BASE_URL_MOVIMENTACOES_SENADO = (
    "https://legis.senado.leg.br/dadosabertos/materia/movimentacoes"
)

MAX_WORKERS_TRAMITACOES_SENADO = int(
    os.getenv("MAX_WORKERS_TRAMITACOES_SENADO", "5")
)


def buscar_ids_senado_no_banco() -> list[str]:
    """
    Busca no banco apenas os IDs externos das matérias do Senado.

    Exemplo:
    - senado-169929
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(
            Proposicao.origem == "Senado"
        )

        resultados = session.exec(statement).all()

    return list(resultados)


def extrair_codigo_senado(id_externo: str) -> Optional[str]:
    """
    Extrai o CodigoMateria de um id_externo no formato senado-123456.
    """
    if not id_externo or not id_externo.startswith("senado-"):
        return None

    partes = id_externo.split("-", maxsplit=1)

    if len(partes) != 2:
        return None

    codigo = partes[1].strip()

    if not codigo.isdigit():
        return None

    return codigo


def parse_data_senado(valor: Optional[str]) -> datetime:
    """
    Converte datas retornadas pela API do Senado.

    Exemplos reais:
    - 2026-03-17 11:58:13
    - 2026-03-17
    - 17/03/2026
    - 2026-03-17T11:58:13
    """
    if not valor:
        return datetime.now()

    texto = str(valor).strip()

    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
    ]

    for formato in formatos:
        try:
            return datetime.strptime(texto[:19], formato)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(texto[:19])
    except ValueError:
        logger.warning("Data de movimentação inválida no Senado: %s", valor)
        return datetime.now()


def coletar_valores_por_chave(obj: Any, chave_alvo: str) -> list[Any]:
    """
    Coleta recursivamente todos os valores associados a uma chave.

    Diferente de find_value, não para no primeiro resultado.
    """
    encontrados: list[Any] = []

    if isinstance(obj, dict):
        for chave, valor in obj.items():
            if str(chave).lower() == chave_alvo.lower():
                encontrados.append(valor)

            encontrados.extend(
                coletar_valores_por_chave(valor, chave_alvo)
            )

    elif isinstance(obj, list):
        for item in obj:
            encontrados.extend(
                coletar_valores_por_chave(item, chave_alvo)
            )

    return encontrados


def normalizar_para_lista_dict(valores: list[Any]) -> list[dict]:
    """
    Normaliza dict/list recebidos da API para list[dict].
    """
    itens: list[dict] = []

    for valor in valores:
        if isinstance(valor, dict):
            itens.append(valor)

        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, dict):
                    itens.append(item)

    return itens


def normalizar_lista_movimentacoes(dados: dict) -> list[dict]:
    """
    Normaliza a estrutura de movimentações do Senado.

    A resposta validada vem em:
    MovimentacaoMateria/Materia/Autuacoes/Autuacao/
    InformesLegislativos/InformeLegislativo

    Também coletamos Despacho e OrdemDoDia, quando existirem, porque o dataset
    do Senado inclui despachos, prazos e ordens do dia no mesmo serviço.
    """
    itens: list[dict] = []

    # Principal para histórico legislativo.
    informes = coletar_valores_por_chave(dados, "InformeLegislativo")
    itens.extend(normalizar_para_lista_dict(informes))

    # Fallbacks úteis quando uma matéria tem pouca tramitação formal.
    movimentacoes = coletar_valores_por_chave(dados, "Movimentacao")
    itens.extend(normalizar_para_lista_dict(movimentacoes))

    tramitacoes = coletar_valores_por_chave(dados, "Tramitacao")
    itens.extend(normalizar_para_lista_dict(tramitacoes))

    despachos = coletar_valores_por_chave(dados, "Despacho")
    itens.extend(normalizar_para_lista_dict(despachos))

    ordens_do_dia = coletar_valores_por_chave(dados, "OrdemDoDia")
    itens.extend(normalizar_para_lista_dict(ordens_do_dia))

    return remover_movimentacoes_duplicadas(itens)


def valor_texto(valor: Any) -> Optional[str]:
    """
    Retorna uma string simples somente quando o valor é útil para exibição.
    """
    if valor is None or isinstance(valor, (dict, list)):
        return None

    texto = str(valor).strip()

    if not texto:
        return None

    return texto


def extrair_orgao_movimentacao(mov: dict) -> str:
    """
    Extrai o órgão/local/colegiado da movimentação.
    """
    local = find_value(mov, "Local")
    colegiado = find_value(mov, "Colegiado")
    sessao = find_value(mov, "SessaoPlenaria")

    if isinstance(local, dict):
        sigla = (
            find_value(local, "SiglaLocal")
            or find_value(local, "SiglaCasaLocal")
        )
        nome = find_value(local, "NomeLocal")
        return valor_texto(sigla) or valor_texto(nome) or "Senado"

    if isinstance(colegiado, dict):
        sigla = (
            find_value(colegiado, "SiglaColegiado")
            or find_value(colegiado, "SiglaCompleta")
            or find_value(colegiado, "SiglaCasaColegiado")
        )
        nome = find_value(colegiado, "NomeColegiado")
        return valor_texto(sigla) or valor_texto(nome) or "Senado"

    if isinstance(sessao, dict):
        casa = find_value(sessao, "SiglaCasaSessao")
        return valor_texto(casa) or "Senado"

    orgao = (
        find_value(mov, "SiglaLocal")
        or find_value(mov, "NomeLocal")
        or find_value(mov, "SiglaColegiado")
        or find_value(mov, "SiglaCompleta")
        or find_value(mov, "NomeColegiado")
        or find_value(mov, "SiglaCasaLocal")
        or find_value(mov, "SiglaCasaColegiado")
        or find_value(mov, "SiglaCasaSessao")
        or find_value(mov, "Orgao")
        or find_value(mov, "Órgão")
        or find_value(mov, "Casa")
    )

    return valor_texto(orgao) or "Senado"


def extrair_data_movimentacao(mov: dict) -> datetime:
    """
    Extrai a data da movimentação usando os nomes reais vistos na API.
    """
    data = (
        find_value(mov, "Data")
        or find_value(mov, "DataMovimentacao")
        or find_value(mov, "DataTramitacao")
        or find_value(mov, "DataSituacao")
        or find_value(mov, "DataDespacho")
        or find_value(mov, "DataOrdemDoDia")
        or find_value(mov, "DataSessao")
        or find_value(mov, "DataEnvio")
        or find_value(mov, "DataUltimaAtualizacao")
    )

    hora = find_value(mov, "HoraInicioSessao")

    if data and hora and len(str(data).strip()) == 10:
        return parse_data_senado(f"{data} {hora}")

    return parse_data_senado(data)


def montar_descricao_movimentacao(mov: dict) -> str:
    """
    Monta uma descrição legível para informes, despachos e ordens do dia.
    """
    descricao = (
        find_value(mov, "Descricao")
        or find_value(mov, "DescricaoTramitacao")
        or find_value(mov, "DescricaoMovimentacao")
        or find_value(mov, "DescricaoInforme")
        or find_value(mov, "Texto")
        or find_value(mov, "Informacao")
        or find_value(mov, "Identificacao")
        or find_value(mov, "Observacao1Despacho")
        or find_value(mov, "Observacao2Despacho")
        or find_value(mov, "DescricaoTipoApreciacao")
        or find_value(mov, "DescricaoResultado")
        or "Sem descrição"
    )

    partes = [valor_texto(descricao) or "Sem descrição"]

    resultado = valor_texto(find_value(mov, "DescricaoResultado"))
    if resultado and resultado not in partes[0]:
        partes.append(f"Resultado: {resultado}")

    motivacao = find_value(mov, "Motivacao")
    if isinstance(motivacao, dict):
        tipo_motivacao = valor_texto(find_value(motivacao, "TipoMotivacao"))
        if tipo_motivacao:
            partes.append(f"Motivação: {tipo_motivacao}")

    situacao = find_value(mov, "SituacaoIniciada") or find_value(mov, "Situacao")
    if isinstance(situacao, dict):
        sigla = valor_texto(find_value(situacao, "SiglaSituacao"))
        descricao_situacao = valor_texto(find_value(situacao, "DescricaoSituacao"))
        situacao_texto = sigla or descricao_situacao

        if situacao_texto:
            partes.append(f"Situação: {situacao_texto}")

    elif valor_texto(situacao):
        partes.append(f"Situação: {valor_texto(situacao)}")

    return " | ".join(partes)


def chave_deduplicacao_movimentacao(mov: dict) -> tuple[str, str, str]:
    """
    Gera chave estável para remover duplicatas que a API pode retornar.
    """
    data = str(
        find_value(mov, "Data")
        or find_value(mov, "DataDespacho")
        or find_value(mov, "DataOrdemDoDia")
        or find_value(mov, "DataTramitacao")
        or ""
    ).strip()

    descricao = valor_texto(
        find_value(mov, "Descricao")
        or find_value(mov, "Observacao1Despacho")
        or find_value(mov, "DescricaoTipoApreciacao")
        or find_value(mov, "DescricaoResultado")
    ) or ""

    orgao = extrair_orgao_movimentacao(mov)

    return (data, descricao[:300], orgao)


def remover_movimentacoes_duplicadas(itens: list[dict]) -> list[dict]:
    """
    Remove duplicatas mantendo a ordem original.
    """
    vistos: set[tuple[str, str, str]] = set()
    unicos: list[dict] = []

    for item in itens:
        chave = chave_deduplicacao_movimentacao(item)

        if chave in vistos:
            continue

        vistos.add(chave)
        unicos.append(item)

    return unicos


def fetch_movimentacoes_senado(codigo_materia: str) -> Optional[list[dict]]:
    """
    Busca movimentações de uma matéria do Senado.

    O endpoint que respondeu 200 nos testes foi:
    /dadosabertos/materia/movimentacoes/{codigo}.json

    Sem o sufixo .json, a API pode retornar 400.
    """
    url = f"{BASE_URL_MOVIMENTACOES_SENADO}/{codigo_materia}.json"

    resp = fazer_requisicao_com_retry(
        url,
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if resp is None:
        logger.warning(
            "Não foi possível buscar movimentações do Senado para matéria %s.",
            codigo_materia,
        )
        return None

    resp.encoding = "utf-8"

    try:
        dados = resp.json()
    except ValueError:
        logger.warning(
            "Resposta inválida nas movimentações do Senado para matéria %s.",
            codigo_materia,
        )
        return None

    movimentacoes = normalizar_lista_movimentacoes(dados)

    if not movimentacoes:
        logger.info(
            "Matéria Senado %s consultada, mas nenhuma movimentação foi encontrada.",
            codigo_materia,
        )

    return movimentacoes


def processar_tramitacoes_senado_individuais(
    id_externo: str,
) -> tuple[str, Optional[list[Tramitacao]]]:
    """
    Processa as movimentações de uma matéria do Senado.
    """
    codigo_materia = extrair_codigo_senado(id_externo)

    if not codigo_materia:
        logger.warning("ID externo inválido para matéria do Senado: %s", id_externo)
        return id_externo, None

    movimentacoes = fetch_movimentacoes_senado(codigo_materia)

    if movimentacoes is None:
        return id_externo, None

    tramitacoes_processadas: list[Tramitacao] = []

    for mov in movimentacoes:
        descricao = montar_descricao_movimentacao(mov)

        if not descricao or descricao == "Sem descrição":
            continue

        nova_tramitacao = Tramitacao(
            id_proposicao_externo=id_externo,
            data_hora=extrair_data_movimentacao(mov),
            orgao=extrair_orgao_movimentacao(mov),
            descricao=descricao,
        )

        tramitacoes_processadas.append(nova_tramitacao)

    return id_externo, tramitacoes_processadas


def substituir_tramitacoes_senado_no_banco(
    tramitacoes_por_id: dict[str, list[Tramitacao]],
) -> int:
    """
    Substitui tramitações antigas apenas das matérias consultadas com sucesso.
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


def run_pipeline_tramitacoes_senado() -> None:
    logger.info("=== Iniciando crawler de tramitações do Senado ===")

    ids_banco = buscar_ids_senado_no_banco()

    if not ids_banco:
        logger.warning(
            "Nenhuma matéria do Senado encontrada no banco. "
            "Rode o senado_api.py primeiro."
        )
        return

    logger.info(
        "Buscando histórico de movimentações para %s matérias do Senado.",
        len(ids_banco),
    )

    tramitacoes_por_id: dict[str, list[Tramitacao]] = {}

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS_TRAMITACOES_SENADO
    ) as executor:
        futuros = {
            executor.submit(
                processar_tramitacoes_senado_individuais,
                id_externo,
            ): id_externo
            for id_externo in ids_banco
        }

        for futuro in concurrent.futures.as_completed(futuros):
            id_externo = futuros[futuro]

            try:
                id_processado, resultado = futuro.result()
            except Exception:
                logger.exception(
                    "Erro inesperado ao processar movimentações de %s.",
                    id_externo,
                )
                continue

            if resultado is None:
                logger.warning(
                    "Movimentações de %s não foram atualizadas por falha.",
                    id_processado,
                )
                continue

            tramitacoes_por_id[id_processado] = resultado

    if not tramitacoes_por_id:
        logger.warning(
            "Nenhuma movimentação do Senado foi atualizada. "
            "Possível falha geral na API."
        )
        return

    total_salvo = substituir_tramitacoes_senado_no_banco(tramitacoes_por_id)

    logger.info(
        "=== Crawler de tramitações do Senado concluído. "
        "%s matérias atualizadas; %s movimentações salvas. ===",
        len(tramitacoes_por_id),
        total_salvo,
    )

if __name__ == "__main__":
    run_pipeline_tramitacoes_senado()
