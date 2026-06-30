"""
Issue 3: Testes de busca por ID e validação de existência

Valida os endpoints GET /proposicoes/{id} e GET /proposicoes/{id_externo},
garantindo a recuperação correta de uma proposição única e o retorno 404
para registros inexistentes.
"""


# ==========================================
# ISSUE 3 — Busca por ID e validação de existência
# ==========================================

def test_busca_por_id_interno_retorna_200(client, dados_basicos):
    """Valida que buscar por id_proposicao interno retorna status 200."""
    id_interno = dados_basicos["camara"].id_proposicao
    response = client.get(f"/proposicoes/{id_interno}")
    assert response.status_code == 200


def test_busca_por_id_interno_retorna_proposicao_correta(client, dados_basicos):
    """Valida que a proposição retornada pelo id interno é a correta."""
    proposicao = dados_basicos["camara"]
    response = client.get(f"/proposicoes/{proposicao.id_proposicao}")
    dados = response.json()

    assert dados["id_externo"] == proposicao.id_externo
    assert dados["tipo"] == proposicao.tipo
    assert dados["numero"] == proposicao.numero
    assert dados["ano"] == proposicao.ano


def test_busca_por_id_interno_expoe_texto_integral(client, dados_basicos):
    """
    Valida que a rota de detalhe expõe texto_integral,
    diferente da listagem geral que omite esse campo.
    """
    id_interno = dados_basicos["camara"].id_proposicao
    response = client.get(f"/proposicoes/{id_interno}")
    dados = response.json()

    assert "texto_integral" in dados
    assert dados["texto_integral"] == "Texto completo da proposição da Câmara."


def test_busca_por_id_externo_retorna_200(client, dados_basicos):
    """Valida que buscar por id_externo retorna status 200."""
    response = client.get("/proposicoes/camara-1")
    assert response.status_code == 200


def test_busca_por_id_externo_retorna_proposicao_correta(client, dados_basicos):
    """Valida que a proposição retornada pelo id externo é a correta."""
    response = client.get("/proposicoes/senado-2")
    dados = response.json()

    assert dados["id_externo"] == "senado-2"
    assert dados["origem"] == "Senado"
    assert dados["numero"] == 20
    assert dados["ano"] == 2025


def test_busca_por_id_inexistente_retorna_404(client, dados_basicos):
    """Valida que buscar por ID numérico inexistente retorna 404."""
    response = client.get("/proposicoes/999999")
    assert response.status_code == 404


def test_busca_por_id_externo_inexistente_retorna_404(client, dados_basicos):
    """Valida que buscar por id_externo inexistente retorna 404."""
    response = client.get("/proposicoes/camara-999999")
    assert response.status_code == 404


def test_busca_por_id_inexistente_retorna_mensagem_de_erro(client, dados_basicos):
    """Valida que o corpo do 404 contém mensagem explicativa no campo detail."""
    response = client.get("/proposicoes/999999")
    dados = response.json()

    assert "detail" in dados
    assert len(dados["detail"]) > 0