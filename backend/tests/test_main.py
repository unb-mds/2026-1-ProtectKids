from fastapi.testclient import TestClient
from main import app  # ajuste o import conforme o nome real do seu módulo principal

client = TestClient(app)

def test_read_root_route():
    response = client.get("/")
    assert response.status_code == 200