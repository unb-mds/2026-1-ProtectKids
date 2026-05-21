from typing import Optional
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select, func
from database import engine, get_session
from models import Proposicao, Parlamentar
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ProtectKids API")

# CORS = TRAVA DE SEGURANÇA 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # porta do Vite (5173) adicionada por garantia
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"status": "ProtectKids Online", "message": "API e Banco de Dados conectados com sucesso!"}

# ==========================================
# 1. ROTA DE PROPOSIÇÕES (COM FILTROS)
# ==========================================
@app.get("/proposicoes")
def get_todas_proposicoes(
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    Retorna a lista de leis. O frontend pode usar os parâmetros na URL para filtrar.
    Exemplo: /proposicoes?uf=SP&ano=2023&tema_nlp=Cyberbullying e Crimes Virtuais
    """
    query = select(Proposicao)
    
    # Se o frontend pedir filtro de UF ou Partido, precisamos "juntar" a tabela do Parlamentar na busca
    if uf or partido:
        query = query.join(Parlamentar, Proposicao.id_autor == Parlamentar.id_parlamentar)
        
    # Aplica os filtros apenas se o frontend tiver enviado o parâmetro
    if uf:
        query = query.where(Parlamentar.uf == uf.upper())
    if partido:
        query = query.where(Parlamentar.partido == partido.upper())
    if ano:
        query = query.where(Proposicao.ano == ano)
    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)
        
    proposicoes = session.exec(query).all()
    return proposicoes

# ==========================================
# 2. ROTA DE RANKING DE PARLAMENTARES (COM FILTROS)
# ==========================================
@app.get("/analytics/parlamentares/ranking")
def get_ranking_parlamentares(
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = (
        select(
            Parlamentar.nome,
            Parlamentar.partido,
            Parlamentar.uf,
            func.count(Proposicao.id_proposicao).label("total_projetos")
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
    )
    
    # Filtra os gráficos se o frontend pedir
    if ano:
        query = query.where(Proposicao.ano == ano)
    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)
        
    query = (
        query.group_by(Parlamentar.id_parlamentar, Parlamentar.nome, Parlamentar.partido, Parlamentar.uf)
        .order_by(func.count(Proposicao.id_proposicao).desc())
    )
    
    resultados = session.exec(query).all()
    
    return [
        {"nome": row[0], "partido": row[1], "uf": row[2], "total_projetos": row[3]}
        for row in resultados
    ]

# ==========================================
# 3. ROTA DE RANKING DE PARTIDOS (COM FILTROS)
# ==========================================
@app.get("/analytics/partidos/ranking")
def get_ranking_partidos(
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = (
        select(
            Parlamentar.partido,
            func.count(Proposicao.id_proposicao).label("total_projetos")
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
    )
    
    if ano:
        query = query.where(Proposicao.ano == ano)
    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)
        
    query = query.group_by(Parlamentar.partido).order_by(func.count(Proposicao.id_proposicao).desc())
    
    resultados = session.exec(query).all()
    
    return [
        {"partido": row[0], "total_projetos": row[1]}
        for row in resultados
    ]