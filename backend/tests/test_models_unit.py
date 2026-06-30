from datetime import date, datetime

from models import Parlamentar, Proposicao, Tramitacao


def test_cria_parlamentar_com_campos_obrigatorios():
    parlamentar = Parlamentar(
        id_parlamentar=123,
        nome="Maria Silva",
    )

    assert parlamentar.id_parlamentar == 123
    assert parlamentar.nome == "Maria Silva"
    assert parlamentar.partido == "ND"
    assert parlamentar.uf == "ND"


def test_cria_parlamentar_com_partido_e_uf():
    parlamentar = Parlamentar(
        id_parlamentar=456,
        nome="João Souza",
        partido="ABC",
        uf="DF",
    )

    assert parlamentar.id_parlamentar == 456
    assert parlamentar.nome == "João Souza"
    assert parlamentar.partido == "ABC"
    assert parlamentar.uf == "DF"


def test_cria_proposicao_com_campos_obrigatorios_e_defaults():
    proposicao = Proposicao(
        id_externo="camara-123",
        tipo="PL",
        numero=123,
        ano=2026,
        ementa="Projeto de lei sobre proteção de crianças e adolescentes no ambiente digital.",
    )

    assert proposicao.id_externo == "camara-123"
    assert proposicao.tipo == "PL"
    assert proposicao.numero == 123
    assert proposicao.ano == 2026
    assert proposicao.origem == "Camara"
    assert proposicao.tema == "Protecao Infantil"
    assert proposicao.ementa == (
        "Projeto de lei sobre proteção de crianças e adolescentes no ambiente digital."
    )
    assert proposicao.id_autor is None
    assert proposicao.data_apresentacao is None
    assert proposicao.url_inteiro_teor is None
    assert proposicao.subtema is None
    assert proposicao.texto_integral is None
    assert proposicao.classificacao_nlp is None
    assert proposicao.fonte_classificacao is None
    assert proposicao.trecho_classificacao is None


def test_cria_proposicao_com_campos_opcionais():
    data_apresentacao = date(2026, 6, 30)

    proposicao = Proposicao(
        id_proposicao=1,
        id_externo="senado-456",
        id_autor=789,
        origem="Senado",
        tipo="PL",
        numero=456,
        ano=2026,
        ementa="Proposição sobre segurança online de crianças.",
        tema="Protecao Infantil",
        data_apresentacao=data_apresentacao,
        url_inteiro_teor="https://example.com/proposicao.pdf",
        subtema="Segurança Online",
        texto_integral="Texto integral da proposição.",
        classificacao_nlp="Cyberbullying e Crimes Virtuais",
        fonte_classificacao="nlp",
        trecho_classificacao="segurança online de crianças",
    )

    assert proposicao.id_proposicao == 1
    assert proposicao.id_externo == "senado-456"
    assert proposicao.id_autor == 789
    assert proposicao.origem == "Senado"
    assert proposicao.tipo == "PL"
    assert proposicao.numero == 456
    assert proposicao.ano == 2026
    assert proposicao.data_apresentacao == data_apresentacao
    assert proposicao.url_inteiro_teor == "https://example.com/proposicao.pdf"
    assert proposicao.subtema == "Segurança Online"
    assert proposicao.texto_integral == "Texto integral da proposição."
    assert proposicao.classificacao_nlp == "Cyberbullying e Crimes Virtuais"
    assert proposicao.fonte_classificacao == "nlp"
    assert proposicao.trecho_classificacao == "segurança online de crianças"


def test_cria_tramitacao_com_campos_obrigatorios():
    data_hora = datetime(2026, 6, 30, 14, 30, 0)

    tramitacao = Tramitacao(
        id_proposicao_externo="camara-123",
        data_hora=data_hora,
        orgao="MESA",
        descricao="Apresentação da proposição.",
    )

    assert tramitacao.id is None
    assert tramitacao.id_proposicao_externo == "camara-123"
    assert tramitacao.data_hora == data_hora
    assert tramitacao.orgao == "MESA"
    assert tramitacao.descricao == "Apresentação da proposição."


def test_nomes_das_tabelas_dos_modelos():
    assert Parlamentar.__tablename__ == "parlamentares"
    assert Proposicao.__tablename__ == "proposicoes"
    assert Tramitacao.__tablename__ == "tramitacoes"