from fastapi.testclient import TestClient
# Importa o 'app' do seu arquivo principal. 
# Se o seu arquivo principal se chamar 'api.py', mude para: from api import app
from main import app 

# Cria o cliente de teste que vai simular as requisições HTTP
client = TestClient(app)

def test_read_root_route():
    """
    Este teste simula uma requisição GET na rota '/' 
    e verifica se o servidor responde com o status 200 (OK).
    """
    # 1. Faz a requisição simulada
    response = client.get("/")
    
    # 2. Verifica se o status retornado é 200 (Sucesso)
    assert response.status_code == 200