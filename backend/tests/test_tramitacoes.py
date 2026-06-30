"""
Issue 4: Testes de tramitações de proposições

Valida o endpoint GET /proposicoes/{id_externo}/tramitacoes,
garantindo que a API recupera corretamente o histórico de tramitações
vinculado a uma proposição específica.
"""


# ==========================================
# ISSUE 4 — Tramitações de proposições
# ==========================================

def test_tramitacoes_retorna_200(client, dados_basicos):
    """Valida que o endpoint de tramitações retorna status 200."""
    response = client.get("/proposicoes/camara-1/tramitacoes")
    assert response.status_code == 200


def test_tramitacoes_retorna_lista(client, dados_basicos):
    """Valida que o retorno do endpoint de tramitações é uma lista."""
    response = client.get("/proposicoes/camara-1/tramitacoes")
    dados = response.json()
    assert isinstance(dados, list)


def test_tramitacoes_lista_nao_esta_vazia(client, dados_basicos):
    """
    Valida que proposições com histórico retornam lista não vazia.
    O conftest.py insere uma tramitação vinculada a camara-1.
    """
    response = client.get("/proposicoes/camara-1/tramitacoes")
    dados = response.json()
    assert len(dados) > 0


def test_tramitacoes_estrutura_dos_campos(client, dados_basicos):
    """Valida que cada tramitação contém os campos esperados."""
    response = client.get("/proposicoes/camara-1/tramitacoes")
    dados = response.json()

    tramitacao = dados[0]
    campos_esperados = {"data_hora", "orgao", "descricao"}
    assert campos_esperados.issubset(tramitacao.keys())


def test_tramitacoes_retorna_dados_corretos(client, dados_basicos):
    """Valida que os dados da tramitação batem com o inserido no conftest."""
    response = client.get("/proposicoes/camara-1/tramitacoes")
    dados = response.json()

    tramitacao = dados[0]
    assert tramitacao["orgao"] == "MESA"
    assert tramitacao["descricao"] == "Apresentação do projeto."


def test_tramitacoes_ordenadas_da_mais_recente(client, dados_basicos):
    """
    Valida que as tramitações vêm ordenadas da mais recente para
    a mais antiga, conforme implementado na rota.
    """
    response = client.get("/proposicoes/camara-1/tramitacoes")
    dados = response.json()

    if len(dados) > 1:
        datas = [item["data_hora"] for item in dados]
        assert datas == sorted(datas, reverse=True)


def test_tramitacoes_proposicao_inexistente_retorna_404(client, dados_basicos):
    """Valida que buscar tramitações de proposição inexistente retorna 404."""
    response = client.get("/proposicoes/camara-999999/tramitacoes")
    assert response.status_code == 404


def test_tramitacoes_proposicao_sem_historico_retorna_lista_vazia(client, dados_basicos):
    """
    Valida que uma proposição existente mas sem tramitações
    retorna 200 com lista vazia, não um erro.
    O conftest.py insere senado-2 sem tramitações vinculadas.
    """
    response = client.get("/proposicoes/senado-2/tramitacoes")
    assert response.status_code == 200
    assert response.json() == []