from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select, func
from database import engine, get_session
from models import Proposicao, Parlamentar, Tramitacao
from fastapi.middleware.cors import CORSMiddleware
import spacy
from collections import Counter
from contextlib import asynccontextmanager


nlp = spacy.load("pt_core_news_sm")

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="ProtectKids API", lifespan=lifespan)

# CORS = TRAVA DE SEGURANÇA 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # porta do Vite (5173) adicionada por garantia
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "ProtectKids Online", "message": "API e Banco de Dados conectados com sucesso!"}

# ==========================================
# FUNÇÕES AUXILIARES DE SERIALIZAÇÃO / FILTROS
# ==========================================

ORIGENS_VALIDAS = {
    "camara": "Camara",
    "câmara": "Camara",
    "senado": "Senado",
}


def normalizar_origem(origem: Optional[str]) -> Optional[str]:
    """
    Normaliza a origem recebida pela API.

    Aceita:
    - Camara
    - Câmara
    - Senado

    Retorna o valor padronizado:
    - Camara
    - Senado
    """
    if origem is None:
        return None

    origem_normalizada = ORIGENS_VALIDAS.get(origem.strip().lower())

    if not origem_normalizada:
        raise HTTPException(
            status_code=400,
            detail="Origem inválida. Use 'Camara' ou 'Senado'.",
        )

    return origem_normalizada


def valores_origem_para_consulta(origem_padronizada: Optional[str]) -> Optional[list[str]]:
    """
    Mantém compatibilidade com dados antigos salvos como 'Câmara'.

    Depois que o banco for recriado com o padrão novo, apenas 'Camara'
    será necessário.
    """
    if origem_padronizada == "Camara":
        return ["Camara", "Câmara"]

    if origem_padronizada == "Senado":
        return ["Senado"]

    return None


def serializar_proposicao(prop: Proposicao, incluir_texto: bool = False) -> dict:
    """
    Converte uma proposição do banco em JSON limpo para o frontend.

    Por padrão, NÃO inclui texto_integral, porque esse campo pode ser grande.
    O texto completo só é retornado na rota de detalhe.
    """
    dados = {
        "id_proposicao": prop.id_proposicao,
        "id_externo": prop.id_externo,
        "titulo": f"{prop.tipo} {prop.numero}/{prop.ano}",
        "origem": normalizar_origem(prop.origem) if prop.origem else None,
        "tipo": prop.tipo,
        "numero": prop.numero,
        "ano": prop.ano,
        "ementa": prop.ementa,
        "tema": prop.tema,
        "subtema": prop.subtema,
        "classificacao_nlp": prop.classificacao_nlp,
        "data_apresentacao": prop.data_apresentacao,
        "url_inteiro_teor": prop.url_inteiro_teor,
        "id_autor": prop.id_autor,
        "nome_autor": prop.autor.nome if prop.autor else "Autor Desconhecido",
        "partido_autor": prop.autor.partido if prop.autor else "ND",
        "uf_autor": prop.autor.uf if prop.autor else "ND",
    }

    if incluir_texto:
        dados["texto_integral"] = prop.texto_integral

    return dados
@app.get("/proposicoes")
def get_todas_proposicoes(
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    """
    Retorna a lista resumida de proposições.

    Filtros disponíveis:
    - uf
    - partido
    - ano
    - tema_nlp
    - origem: Camara ou Senado

    Observação:
    - texto_integral não é retornado nesta listagem para evitar resposta pesada.
    - use /proposicoes/{id_busca} para obter detalhes completos.
    """
    query = select(Proposicao)

    if uf or partido:
        query = query.join(
            Parlamentar,
            Proposicao.id_autor == Parlamentar.id_parlamentar,
        )

    if uf:
        query = query.where(Parlamentar.uf == uf.upper())

    if partido:
        query = query.where(Parlamentar.partido == partido.upper())

    if ano:
        query = query.where(Proposicao.ano == ano)

    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)

    origem_padronizada = normalizar_origem(origem)
    origens_consulta = valores_origem_para_consulta(origem_padronizada)

    if origens_consulta:
        query = query.where(Proposicao.origem.in_(origens_consulta))

    query = (
        query
        .order_by(Proposicao.ano.desc(), Proposicao.numero.desc())
        .offset(offset)
        .limit(limit)
    )

    proposicoes_db = session.exec(query).all()

    return [
        serializar_proposicao(prop, incluir_texto=False)
        for prop in proposicoes_db
    ]

@app.get("/proposicoes/{id_busca}")
def get_proposicao_por_id(
    id_busca: str,
    session: Session = Depends(get_session),
):
    """
    Busca uma proposição por:

    - id_proposicao do banco:
      exemplo: /proposicoes/1

    - id_externo da fonte:
      exemplo: /proposicoes/camara-24792026
      exemplo: /proposicoes/senado-123456
    """
    if id_busca.isdigit():
        query = select(Proposicao).where(
            Proposicao.id_proposicao == int(id_busca)
        )
    else:
        query = select(Proposicao).where(
            Proposicao.id_externo == id_busca
        )

    prop = session.exec(query).first()

    if not prop:
        raise HTTPException(
            status_code=404,
            detail=f"Proposição com ID {id_busca} não foi encontrada no banco de dados.",
        )

    return serializar_proposicao(prop, incluir_texto=True)

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

# ==========================================
# 5. ROTA DE NUVEM DE PALAVRAS (DASHBOARD)
# ==========================================
@app.get("/analytics/nuvem-palavras")
def get_nuvem_palavras(
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    Retorna as palavras mais frequentes nas ementas das proposições.
    Ideal para bibliotecas de Word Cloud no frontend.
    """
    query = select(Proposicao.ementa)
    
    if ano:
        query = query.where(Proposicao.ano == ano)
    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)
        
    ementas = session.exec(query).all()
    
    if not ementas:
        return []

    texto_completo = " ".join([e for e in ementas if e])
    doc = nlp(texto_completo)
    
# Lista de jargões legislativos que não agregam valor visual à Nuvem de Palavras
    ruidos_legislativos = {
        "lei", "alterar", "altera", "artigo", "inciso", 
        "parágrafo", "dispor", "estabelecer", "acrescentar", 
        "dar", "providência", "nº", "redação", "sobre",
        
        # Meses do ano
        "janeiro", "fevereiro", "março", "abril", "maio", "junho", 
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
        
        # Novos ruídos estruturais e burocráticos identificados
        "art.", "institui", "instituir", "federal", "dispõe", "requer", 
        "decreto-lei", "audiência", "realização", "termos", "regimento", 
        "interno", "objetivo", "ano", "nacional", "público", "programa", "incluir", "âmbito", "ser", 
    }

    palavras = [
            token.lemma_.lower() 
            for token in doc 
            if not token.is_stop 
            and not token.is_punct 
            and not token.like_num # Remove automaticamente números e anos (ex: 1990, 2026)
            and len(token.text) > 2
            and token.lemma_.lower() not in ruidos_legislativos
            and token.text.lower() not in ruidos_legislativos
        ]
    
    contagem = Counter(palavras)
    top_palavras = contagem.most_common(50)
    
    return [{"text": palavra, "value": frequencia} for palavra, frequencia in top_palavras]