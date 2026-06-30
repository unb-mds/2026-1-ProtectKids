def test_rota_raiz_retorna_status_online(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ProtectKids Online"


def test_listagem_nao_retorna_texto_integral(client, dados_basicos):
    response = client.get("/proposicoes")

    assert response.status_code == 200

    dados = response.json()

    assert len(dados) == 2
    assert "texto_integral" not in dados[0]


def test_listagem_filtra_por_origem(client, dados_basicos):
    response = client.get("/proposicoes", params={"origem": "Senado"})

    assert response.status_code == 200

    dados = response.json()

    assert len(dados) == 1
    assert dados[0]["id_externo"] == "senado-2"


def test_listagem_rejeita_origem_invalida(client, dados_basicos):
    response = client.get("/proposicoes", params={"origem": "Assembleia"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Origem inválida. Use 'Camara' ou 'Senado'."


def test_detalhe_por_id_interno_retorna_texto_integral(client, dados_basicos):
    id_interno = dados_basicos["camara"].id_proposicao

    response = client.get(f"/proposicoes/{id_interno}")

    assert response.status_code == 200

    dados = response.json()

    assert dados["id_externo"] == "camara-1"
    assert dados["texto_integral"] == "Texto completo da proposição da Câmara."
    assert dados["fonte_classificacao"] == "texto_integral"


def test_detalhe_por_id_externo(client, dados_basicos):
    response = client.get("/proposicoes/camara-1")

    assert response.status_code == 200
    assert response.json()["titulo"] == "PL 10/2026"


def test_detalhe_retorna_404_quando_nao_existe(client):
    response = client.get("/proposicoes/camara-inexistente")

    assert response.status_code == 404


def test_tramitacoes_da_proposicao(client, dados_basicos):
    response = client.get("/proposicoes/camara-1/tramitacoes")

    assert response.status_code == 200

    dados = response.json()

    assert len(dados) == 1
    assert dados[0]["orgao"] == "MESA"
    assert dados[0]["descricao"] == "Apresentação do projeto."


def test_ranking_parlamentares(client, dados_basicos):
    response = client.get("/analytics/parlamentares/ranking")

    assert response.status_code == 200

    dados = response.json()
    nomes = {item["nome"] for item in dados}

    assert "Deputada Teste" in nomes
    assert "Senador Exemplo" in nomes


def test_ranking_partidos(client, dados_basicos):
    response = client.get("/analytics/partidos/ranking")

    assert response.status_code == 200

    partidos = {item["partido"] for item in response.json()}

    assert partidos == {"ABC", "XYZ"}


def test_analytics_subtemas(client, dados_basicos):
    response = client.get("/analytics/subtemas")

    assert response.status_code == 200

    nomes = {item["nome"] for item in response.json()}

    assert "Cyberbullying e Crimes Virtuais" in nomes
    assert "Privacidade e Dados de Menores" in nomes