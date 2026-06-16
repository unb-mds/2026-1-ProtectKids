import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Pega a URL de conexão do ambiente. 
load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://usuario:senha@db:5432/legislativo_db" 
)

# Cria a engine do banco de dados. echo=True faz o SQL aparecer no terminal
engine = create_engine(DATABASE_URL, echo=True)

# Função geradora de sessões para ser injetada nas rotas do FastAPI
def get_session():
    with Session(engine) as session:
        yield session