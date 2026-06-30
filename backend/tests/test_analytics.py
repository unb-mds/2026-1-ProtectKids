"""
Issue 5: Testes para endpoints de Analytics

Valida os endpoints de análise de dados:
- GET /analytics/parlamentares/ranking
- GET /analytics/partidos/ranking
- GET /analytics/nuvem-palavras
"""

import time


# ==========================================
# ISSUE 5 — Analytics: Ranking de Parlamentares
# ==========================================

def test_ranking_parlamentares_retorna_200(client, dados_basicos):
    """Valida que o endpoint de ranking de parlamentares retorna status 200."""
    response = client.get("/analytics/parlamentares/ranking")
    assert response.status_code == 200


def test_ranking_parlamentares_retorna_lista(client, dados_basicos):
    """Valida que o retorno do ranking de parlamentares é uma lista."""
    response = client.get("/analytics/parlamentares/ranking")
    assert isinstance(response.json(), list)


def test_ranking_parlamentares_estrutura_dos_campos(client, dados_basicos):
    """Valida que cada item do ranking contém os campos esperados."""
    response = client.get("/analytics/parlamentares/ranking")
    dados = response.json()

    assert len(dados) > 0
    item = dados[0]
    campos_esperados = {"nome", "partido", "uf", "total_proposicoes"}
    assert campos_esperados.issubset(item.keys())


def test_ranking_parlamentares_ordenado_por_total_decrescente(client, dados_basicos):
    """Valida que o ranking vem ordenado do maior para o menor total de projetos."""
    response = client.get("/analytics/parlamentares/ranking")
    dados = response.json()

    if len(dados) > 1:
        totais = [item["total_proposicoes"] for item in dados]
        assert totais == sorted(totais, reverse=True)


def test_ranking_parlamentares_dados_corretos(client, dados_basicos):
    """
    Valida que o parlamentar com mais projetos aparece no topo.
    O conftest insere 1 proposição para Deputada Teste (DF/ABC)
    e 1 proposição para Senador Exemplo (SP/XYZ).
    """
    response = client.get("/analytics/parlamentares/ranking")
    dados = response.json()

    nomes = [item["nome"] for item in dados]
    assert "Deputada Teste" in nomes
    assert "Senador Exemplo" in nomes


def test_ranking_parlamentares_tempo_de_resposta(client, dados_basicos):
    """Valida que o endpoint responde em menos de 2 segundos."""
    inicio = time.time()
    client.get("/analytics/parlamentares/ranking")
    duracao = time.time() - inicio
    assert duracao < 2.0


# ==========================================
# ISSUE 5 — Analytics: Ranking de Partidos
# ==========================================

def test_ranking_partidos_retorna_200(client, dados_basicos):
    """Valida que o endpoint de ranking de partidos retorna status 200."""
    response = client.get("/analytics/partidos/ranking")
    assert response.status_code == 200


def test_ranking_partidos_retorna_lista(client, dados_basicos):
    """Valida que o retorno do ranking de partidos é uma lista."""
    response = client.get("/analytics/partidos/ranking")
    assert isinstance(response.json(), list)


def test_ranking_partidos_estrutura_dos_campos(client, dados_basicos):
    """Valida que cada item do ranking contém os campos esperados."""
    response = client.get("/analytics/partidos/ranking")
    dados = response.json()

    assert len(dados) > 0
    item = dados[0]
    campos_esperados = {"partido", "total_proposicoes"}
    assert campos_esperados.issubset(item.keys())


def test_ranking_partidos_ordenado_por_total_decrescente(client, dados_basicos):
    """Valida que o ranking de partidos vem ordenado do maior para o menor."""
    response = client.get("/analytics/partidos/ranking")
    dados = response.json()

    if len(dados) > 1:
        totais = [item["total_proposicoes"] for item in dados]
        assert totais == sorted(totais, reverse=True)


def test_ranking_partidos_dados_corretos(client, dados_basicos):
    """Valida que os partidos inseridos no conftest aparecem no ranking."""
    response = client.get("/analytics/partidos/ranking")
    dados = response.json()

    partidos = [item["partido"] for item in dados]
    assert "ABC" in partidos
    assert "XYZ" in partidos


def test_ranking_partidos_tempo_de_resposta(client, dados_basicos):
    """Valida que o endpoint responde em menos de 2 segundos."""
    inicio = time.time()
    client.get("/analytics/partidos/ranking")
    duracao = time.time() - inicio
    assert duracao < 2.0


# ==========================================
# ISSUE 5 — Analytics: Nuvem de Palavras
# ==========================================

def test_nuvem_palavras_retorna_200(client, dados_basicos):
    """Valida que o endpoint de nuvem de palavras retorna status 200."""
    response = client.get("/analytics/nuvem-palavras")
    assert response.status_code == 200


def test_nuvem_palavras_retorna_lista(client, dados_basicos):
    """Valida que o retorno da nuvem de palavras é uma lista."""
    response = client.get("/analytics/nuvem-palavras")
    assert isinstance(response.json(), list)


def test_nuvem_palavras_estrutura_dos_campos(client, dados_basicos):
    """
    Valida que cada item da nuvem contém os campos `text` e `value`,
    conforme esperado pelo frontend.
    """
    response = client.get("/analytics/nuvem-palavras")
    dados = response.json()

    if dados:
        item = dados[0]
        assert "text" in item
        assert "value" in item


def test_nuvem_palavras_value_e_inteiro_positivo(client, dados_basicos):
    """Valida que o campo value é um número inteiro positivo."""
    response = client.get("/analytics/nuvem-palavras")
    dados = response.json()

    for item in dados:
        assert isinstance(item["value"], int)
        assert item["value"] > 0


def test_nuvem_palavras_tempo_de_resposta(client, dados_basicos):
    """Valida que o endpoint responde em menos de 2 segundos."""
    inicio = time.time()
    client.get("/analytics/nuvem-palavras")
    duracao = time.time() - inicio
    assert duracao < 2.0