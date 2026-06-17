from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select, func
from database import engine, get_session
from models import Proposicao, Parlamentar, Tramitacao
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
# 1. ROTA DE PROPOSIÇÕES E DETALHES (COM FILTROS E AUTOR)
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
    """
    query = select(Proposicao)
    
    if uf or partido:
        query = query.join(Parlamentar, Proposicao.id_autor == Parlamentar.id_parlamentar)
        
    if uf:
        query = query.where(Parlamentar.uf == uf.upper())
    if partido:
        query = query.where(Parlamentar.partido == partido.upper())
    if ano:
        query = query.where(Proposicao.ano == ano)
    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)
        
    proposicoes_db = session.exec(query).all()
    
    # Injetando o nome do autor na resposta
    resultados = []
    for prop in proposicoes_db:
        prop_dict = prop.dict() # Converte o objeto SQLModel em um dicionário
        prop_dict["nome_autor"] = prop.autor.nome if prop.autor else "Autor Desconhecido"
        resultados.append(prop_dict)
        
    return resultados

@app.get("/proposicoes/{id_busca}")
def get_proposicao_por_id(id_busca: int, session: Session = Depends(get_session)):
    """
    Busca tanto pela chave primária quanto pelo id_externo da câmara.
    """
    query = select(Proposicao).where(
        (Proposicao.id_proposicao == id_busca) | (Proposicao.id_externo == id_busca)
    )
    prop = session.exec(query).first()
    
    if not prop:
        return None
        
    prop_dict = prop.dict()
    prop_dict["nome_autor"] = prop.autor.nome if prop.autor else "Autor Desconhecido"
    
    return prop_dict

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

# ==========================================
# 4. ROTA DE HISTÓRICO DE TRAMITAÇÕES
# ==========================================

# Cria o modelo de resposta para o frontend receber um JSON limpo
class TramitacaoResponse(BaseModel):
    data_hora: datetime
    orgao: str
    descricao: str

@app.get("/proposicoes/{id_externo}/tramitacoes", response_model=List[TramitacaoResponse])
def obter_tramitacoes(id_externo: str, session: Session = Depends(get_session)):
    """
    Retorna a linha do tempo do andamento de uma proposição.
    """
    # Passo A: Verificar se a lei existe no banco
    proposicao = session.exec(
        select(Proposicao).where(Proposicao.id_externo == id_externo)
    ).first()
    
    if not proposicao:
        raise HTTPException(
            status_code=404, 
            detail=f"Proposição com ID {id_externo} não foi encontrada no banco de dados."
        )

    # Passo B: Buscar as tramitações vinculadas a essa lei, ordenando da mais recente para a mais antiga
    statement = (
        select(Tramitacao)
        .where(Tramitacao.id_proposicao_externo == id_externo)
        .order_by(Tramitacao.data_hora.desc())
    )
    
    tramitacoes = session.exec(statement).all()

    return tramitacoes