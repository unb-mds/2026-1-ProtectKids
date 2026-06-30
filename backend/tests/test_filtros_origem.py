"""
Issue 2: Testes de filtros de origem (Câmara/Senado)

Valida o comportamento do filtro `origem` no endpoint GET /proposicoes,
garantindo que origens válidas retornem 200 e origens inválidas retornem 400.
"""


# ==========================================
# ISSUE 2 — Filtros de origem (Câmara/Senado/inválido)
# ==========================================

def test_listagem_filtra_origem_camara_retorna_200(client, dados_basicos):
    """Valida que origem=Camara retorna status 200."""
    response = client.get("/proposicoes?origem=Camara")
    assert response.status_code == 200


def test_listagem_filtra_origem_camara_retorna_apenas_camara(client, dados_basicos):
    """Valida que origem=Camara retorna apenas proposições da Câmara."""
    response = client.get("/proposicoes?origem=Camara")
    dados = response.json()

    assert len(dados) > 0
    for item in dados:
        assert item["origem"] == "Camara"


def test_listagem_filtra_origem_senado_retorna_200(client, dados_basicos):
    """Valida que origem=Senado retorna status 200."""
    response = client.get("/proposicoes?origem=Senado")
    assert response.status_code == 200


def test_listagem_filtra_origem_senado_retorna_apenas_senado(client, dados_basicos):
    """Valida que origem=Senado retorna apenas proposições do Senado."""
    response = client.get("/proposicoes?origem=Senado")
    dados = response.json()

    assert len(dados) > 0
    for item in dados:
        assert item["origem"] == "Senado"


def test_listagem_rejeita_origem_invalida_retorna_400(client, dados_basicos):
    """Valida que origem=Assembleia retorna 400 Bad Request."""
    response = client.get("/proposicoes?origem=Assembleia")
    assert response.status_code == 400


def test_listagem_rejeita_origem_invalida_retorna_mensagem_de_erro(client, dados_basicos):
    """Valida que o corpo do erro 400 contém uma mensagem explicativa."""
    response = client.get("/proposicoes?origem=Assembleia")
    dados = response.json()

    assert "detail" in dados
    assert len(dados["detail"]) > 0