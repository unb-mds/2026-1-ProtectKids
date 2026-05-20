from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select, func
from database import engine, get_session
from models import Proposicao, Parlamentar
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ProtectKids API")

# CORS = TRAVA DE SEGURANÇA 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Quem pode acessar (adicionar a URL de produção depois)
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE
    allow_headers=["*"],
)
# evento que roda junto com o docker, ele cria tabelas utilizando o postgres
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"status": "ProtectKids Online", "message": "API e Banco de Dados conectados com sucesso!"}

@app.get("/proposicoes")
def get_todas_proposicoes(session: Session = Depends(get_session)):
    """
    Retorna a lista completa de leis sobre proteção infantil cadastradas.
    """
    proposicoes = session.exec(select(Proposicao)).all()
    return proposicoes

@app.get("/analytics/parlamentares/ranking")
def get_ranking_parlamentares(session: Session = Depends(get_session)):
    statement = (
        select(
            Parlamentar.nome,
            Parlamentar.partido,
            Parlamentar.uf,
            func.count(Proposicao.id_proposicao).label("total_projetos")
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
        .group_by(Parlamentar.nome, Parlamentar.partido, Parlamentar.uf)
        .order_by(func.count(Proposicao.id_proposicao).desc())
    )
    
    resultados = session.exec(statement).all()
    
    return [
        {
            "nome": row.nome, 
            "partido": row.partido, 
            "uf": row.uf, 
            "total_projetos": row.total_projetos
        }
        for row in resultados
    ]

@app.get("/analytics/partidos/ranking")
def get_ranking_partidos(session: Session = Depends(get_session)):
    statement = (
        select(
            Parlamentar.partido,
            func.count(Proposicao.id_proposicao).label("total_projetos")
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
        .group_by(Parlamentar.partido)
        .order_by(func.count(Proposicao.id_proposicao).desc())
    )
    
    resultados = session.exec(statement).all()
    
    return [
        {
            "partido": row.partido, 
            "total_projetos": row.total_projetos
        }
        for row in resultados
    ]