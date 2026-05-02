from sqlmodel import Field, SQLModel
from typing import Optional

class Proposicao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    tema: str = "Proteção Infantil Digital"