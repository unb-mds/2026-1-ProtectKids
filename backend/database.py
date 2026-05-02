import os
from sqlmodel import create_engine, Session

# Pega a URL de conexão do Docker
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://augusto:squad10@db:5432/legislativo_db")

# Cria a engine do banco de dados. echo=True faz o SQL aparecer no terminal (bom para debug)
engine = create_engine(DATABASE_URL, echo=True)

# Função geradora de sessões para ser injetada nas rotas do FastAPI
def get_session():
    with Session(engine) as session:
        yield session