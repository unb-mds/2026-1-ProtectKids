import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://protectkids_user:protectkids_password@db:5432/protectkids_db",
)

DEBUG_SQL = os.getenv("DEBUG_SQL", "false").strip().lower() == "true"

engine = create_engine(
    DATABASE_URL,
    echo=DEBUG_SQL,
    pool_pre_ping=True,
)


def get_session():
    with Session(engine) as session:
        yield session