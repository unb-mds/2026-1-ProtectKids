from sqlmodel import Field, SQLModel
from typing import Optional

class Proposicao(SQLModel, table=True):
    __tablename__ = "proposicoes"
    id: Optional[int] = Field(default=None, primary_key=True)
    id_externo: Optional[int] = Field(index=True, unique=True)
    titulo: str
    descricao: str
    tema: str = "Proteção Infantil Digital"