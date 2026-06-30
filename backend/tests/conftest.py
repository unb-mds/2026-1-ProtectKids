import os
from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///./test_protectkids.db"
os.environ["DEBUG_SQL"] = "false"

from database import get_session  # noqa: E402
from main import app  # noqa: E402
from models import Parlamentar, Proposicao, Tramitacao  # noqa: E402


@pytest.fixture(name="session")
def session_fixture():
    engine_teste = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine_teste)

    with Session(engine_teste, expire_on_commit=False) as session:
        yield session

    SQLModel.metadata.drop_all(engine_teste)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="dados_basicos")
def dados_basicos_fixture(session: Session):
    parlamentar_df = Parlamentar(
        id_parlamentar=1,
        nome="Deputada Teste",
        partido="ABC",
        uf="DF",
    )

    parlamentar_sp = Parlamentar(
        id_parlamentar=2,
        nome="Senador Exemplo",
        partido="XYZ",
        uf="SP",
    )

    proposicao_camara = Proposicao(
        id_externo="camara-1",
        id_autor=1,
        origem="Camara",
        tipo="PL",
        numero=10,
        ano=2026,
        ementa="Projeto sobre proteção de crianças no ambiente digital.",
        tema="Proteção Infantil",
        subtema="Cyberbullying",
        classificacao_nlp="Cyberbullying e Crimes Virtuais",
        data_apresentacao=date(2026, 6, 1),
        url_inteiro_teor="https://exemplo.com/camara.pdf",
        texto_integral="Texto completo da proposição da Câmara.",
        fonte_classificacao="texto_integral",
        trecho_classificacao="proteção de crianças no ambiente digital",
    )

    proposicao_senado = Proposicao(
        id_externo="senado-2",
        id_autor=2,
        origem="Senado",
        tipo="PL",
        numero=20,
        ano=2025,
        ementa="Projeto sobre dados pessoais de adolescentes.",
        tema="Proteção Infantil",
        subtema="Privacidade",
        classificacao_nlp="Privacidade e Dados de Menores",
        data_apresentacao=date(2025, 5, 10),
        texto_integral="Texto completo da proposição do Senado.",
    )

    tramitacao = Tramitacao(
        id_proposicao_externo="camara-1",
        data_hora=datetime(2026, 6, 2, 10, 30),
        orgao="MESA",
        descricao="Apresentação do projeto.",
    )

    session.add(parlamentar_df)
    session.add(parlamentar_sp)
    session.add(proposicao_camara)
    session.add(proposicao_senado)
    session.add(tramitacao)

    session.commit()

    session.refresh(proposicao_camara)
    session.refresh(proposicao_senado)

    return {
        "camara": proposicao_camara,
        "senado": proposicao_senado,
    }