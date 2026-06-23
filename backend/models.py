from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date, datetime

class Parlamentar(SQLModel, table=True):
    __tablename__ = "parlamentares"
    id_parlamentar: int = Field(primary_key=True)
    nome: str
    partido: Optional[str] = Field(default="ND") 
    uf: Optional[str] = Field(default="ND")

    proposicoes: List["Proposicao"] = Relationship(back_populates="autor")


class Proposicao(SQLModel, table=True):
    __tablename__ = "proposicoes"
    id_proposicao: Optional[int] = Field(default=None, primary_key=True)
    id_externo: str = Field(index=True, unique=True) 
    id_autor: Optional[int] = Field(default=None, foreign_key="parlamentares.id_parlamentar")
    origem: str = Field(default="Camara")
    tipo: str
    numero: int
    ano: int
    ementa: str
    tema: str = "Protecao Infantil Digital"
    data_apresentacao: Optional[date] = None
    url_inteiro_teor: Optional[str] = Field(default=None)   
    subtema: Optional[str] = Field(default=None)            
    texto_integral: Optional[str] = Field(default=None)     
    classificacao_nlp: Optional[str] = Field(default=None)  
    tramitacoes: List["Tramitacao"] = Relationship(back_populates="proposicao")
    autor: Optional[Parlamentar] = Relationship(back_populates="proposicoes")


# CORREÇÃO 1: A classe agora está fora (sem o recuo)
class Tramitacao(SQLModel, table=True):
    __tablename__ = "tramitacoes" # Padronizando o nome para o plural também
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # CORREÇÃO 2: Apontando para o __tablename__ correto ("proposicoes")
    id_proposicao_externo: str = Field(foreign_key="proposicoes.id_externo") 
    
    data_hora: datetime
    orgao: str # Ex: "Mesa Diretora", "CCJC", "Plenário"
    descricao: str # O que aconteceu (ex: "Aprovado requerimento", "Enviado para sanção")
    
    # Relacionamento de volta para a proposição
    proposicao: Optional["Proposicao"] = Relationship(back_populates="tramitacoes")