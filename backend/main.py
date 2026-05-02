from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import Proposicao
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ProtectKids API")

# CORS = TRAVA DE SEGURANÇA 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Quem pode acessar (adicione a URL de produção depois)
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

# Rota POST para Inserir um dado no Banco de Dados
@app.post("/teste-db/")
def criar_proposicao_teste(session: Session = Depends(get_session)):
    nova_proposicao = Proposicao(
        titulo="PL 123/2026", 
        descricao="Teste de integração do FastAPI com PostgreSQL"
    )
    session.add(nova_proposicao)
    session.commit()
    session.refresh(nova_proposicao) # Atualiza o objeto com o ID gerado pelo banco
    
    return nova_proposicao

# Rota GET para Ler os dados do Banco de Dados
@app.get("/teste-db/")
def ler_proposicoes(session: Session = Depends(get_session)):
    proposicoes = session.exec(select(Proposicao)).all()
    return proposicoes