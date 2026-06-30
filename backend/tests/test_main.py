import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session
from models import Parlamentar, Proposicao


# ==========================================
# CONFIGURAÇÃO DO BANCO DE TESTES (SQLite em memória)
# ==========================================

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_session_teste():
    with Session(engine_teste) as session:
        yield session


@pytest.fixture(name="session")
def session_fixture():
    """Cria as tabelas antes de cada teste e derruba depois."""
    SQLModel.metadata.create_all(engine_teste)
    with Session(engine_teste) as session:
        yield session
    SQLModel.metadata.drop_all(engine_teste)


@pytest.fixture(name="client")
def client_fixture(session):
    """
    Sobrescreve get_session do FastAPI para usar o banco de testes
    em vez do Postgres real, garantindo isolamento total.
    """
    app.dependency_overrides[get_session] = get_session_teste
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# ==========================================
# ISSUE 1 — Rota raiz e listagem geral de proposições
# ==========================================

def test_get_root(client):
    """Valida que a API está no ar e respondendo na rota raiz."""
    response = client.get("/")

    assert response.status_code == 200

    dados = response.json()
    assert "status" in dados
    assert "message" in dados
    assert dados["status"] == "ProtectKids Online"


def test_get_proposicoes_geral_retorna_200(client):
    """Valida que o endpoint /proposicoes retorna status 200."""
    response = client.get("/proposicoes")
    assert response.status_code == 200


def test_get_proposicoes_geral_retorna_lista(client):
    """Valida que o retorno de /proposicoes é sempre uma lista."""
    response = client.get("/proposicoes")
    assert isinstance(response.json(), list)


def test_get_proposicoes_geral_estrutura_de_metadados(client, session):
    """
    Valida que cada item da listagem contém os campos esperados
    e que texto_integral NÃO é exposto na listagem geral.
    """
    # Arrange: insere um parlamentar e uma proposição no banco de testes
    parlamentar = Parlamentar(
        id_parlamentar=1,
        nome="Deputado Teste",
        partido="PT",
        uf="DF",
    )
    session.add(parlamentar)

    proposicao = Proposicao(
        id_externo="camara-999999",
        id_autor=1,
        origem="Camara",
        tipo="PL",
        numero=1,
        ano=2024,
        ementa="Dispõe sobre proteção de crianças na internet.",
        tema="Protecao Infantil",
        classificacao_nlp="Cyberbullying",
    )
    session.add(proposicao)
    session.commit()

    # Act
    response = client.get("/proposicoes")
    dados = response.json()

    # Assert: lista não está vazia
    assert len(dados) > 0

    item = dados[0]

    # Assert: todos os campos esperados estão presentes
    campos_esperados = {
        "id_proposicao",
        "id_externo",
        "titulo",
        "origem",
        "tipo",
        "numero",
        "ano",
        "ementa",
        "tema",
        "subtema",
        "classificacao_nlp",
        "data_apresentacao",
        "url_inteiro_teor",
        "id_autor",
        "nome_autor",
        "partido_autor",
        "uf_autor",
    }
    assert campos_esperados.issubset(item.keys())

    # Assert: texto_integral NÃO deve aparecer na listagem geral
    assert "texto_integral" not in item