def test_rota_raiz_retorna_status_online(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ProtectKids Online"