from typing import Optional, List, Annotated
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
async def lifespan(_app: FastAPI):
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
RESPOSTA_ORIGEM_INVALIDA = {
    400: {
        "description": "Origem inválida informada no filtro.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Origem inválida. Use 'Camara' ou 'Senado'."
                }
            }
        },
    }
}

RESPOSTA_PROPOSICAO_NAO_ENCONTRADA = {
    404: {
        "description": "Proposição não encontrada no banco de dados.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Proposição com ID informado não foi encontrada no banco de dados."
                }
            }
        },
    }
}


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

def aplicar_filtros_analytics(
    query,
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
):
    """
    Aplica filtros comuns aos endpoints analíticos.

    Filtros:
    - ano
    - tema_nlp
    - origem
    - uf
    - partido
    """
    if ano:
        query = query.where(Proposicao.ano == ano)

    if tema_nlp:
        query = query.where(Proposicao.classificacao_nlp == tema_nlp)

    origem_padronizada = normalizar_origem(origem)
    origens_consulta = valores_origem_para_consulta(origem_padronizada)

    if origens_consulta:
        query = query.where(Proposicao.origem.in_(origens_consulta))

    if uf:
        query = query.where(Parlamentar.uf == uf.upper())

    if partido:
        query = query.where(Parlamentar.partido == partido.upper())

    return query

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
        dados["fonte_classificacao"] = prop.fonte_classificacao
        dados["trecho_classificacao"] = prop.trecho_classificacao

    return dados
@app.get(
    "/proposicoes",
    responses=RESPOSTA_ORIGEM_INVALIDA,
)
def get_todas_proposicoes(
    session: Annotated[Session, Depends(get_session)],
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
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

@app.get(
    "/proposicoes/{id_busca}",
    responses=RESPOSTA_PROPOSICAO_NAO_ENCONTRADA,
)
def get_proposicao_por_id(
    id_busca: str,
    session: Annotated[Session, Depends(get_session)],
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

@app.get(
    "/analytics/parlamentares/ranking",
    responses=RESPOSTA_ORIGEM_INVALIDA,
)
def get_ranking_parlamentares(
    session: Annotated[Session, Depends(get_session)],
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Retorna o ranking de parlamentares com mais proposições cadastradas.

    Filtros disponíveis:
    - ano
    - tema_nlp
    - origem: Camara ou Senado
    - uf
    - partido
    - limit
    """
    query = (
        select(
            Parlamentar.nome,
            Parlamentar.partido,
            Parlamentar.uf,
            func.count(Proposicao.id_proposicao).label("total_proposicoes"),
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
    )

    query = aplicar_filtros_analytics(
        query=query,
        ano=ano,
        tema_nlp=tema_nlp,
        origem=origem,
        uf=uf,
        partido=partido,
    )

    query = (
        query
        .group_by(
            Parlamentar.id_parlamentar,
            Parlamentar.nome,
            Parlamentar.partido,
            Parlamentar.uf,
        )
        .order_by(func.count(Proposicao.id_proposicao).desc())
        .limit(limit)
    )

    resultados = session.exec(query).all()

    return [
        {
            "nome": row[0],
            "partido": row[1],
            "uf": row[2],
            "total_proposicoes": row[3],
        }
        for row in resultados
    ]


@app.get(
    "/analytics/partidos/ranking",
    responses=RESPOSTA_ORIGEM_INVALIDA,
)
def get_ranking_partidos(
    session: Annotated[Session, Depends(get_session)],
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Retorna o ranking de partidos com mais proposições cadastradas.

    Filtros disponíveis:
    - ano
    - tema_nlp
    - origem: Camara ou Senado
    - uf
    - partido
    - limit
    """
    query = (
        select(
            Parlamentar.partido,
            func.count(Proposicao.id_proposicao).label("total_proposicoes"),
        )
        .join(Proposicao, Proposicao.id_autor == Parlamentar.id_parlamentar)
    )

    query = aplicar_filtros_analytics(
        query=query,
        ano=ano,
        tema_nlp=tema_nlp,
        origem=origem,
        uf=uf,
        partido=partido,
    )

    query = (
        query
        .group_by(Parlamentar.partido)
        .order_by(func.count(Proposicao.id_proposicao).desc())
        .limit(limit)
    )

    resultados = session.exec(query).all()

    return [
        {
            "partido": row[0],
            "total_proposicoes": row[1],
        }
        for row in resultados
    ]

SUBTEMAS_ANALYTICS_IGNORADOS = {
    "Simbólico/Ruído",
    "Simbólico",
    "Ruído",
    "Nao classificado",
    "Não classificado",

    "Adoção e Orfanatos",
    "Adoção e Orfandade",
    "Educação e Cultura",
    "Violência e Abuso",
    "Proteção Geral",
    "Fora do escopo digital",
}


@app.get("/analytics/subtemas", responses=RESPOSTA_ORIGEM_INVALIDA)
def get_analytics_subtemas(
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    incluir_ruido: bool = Query(default=False),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """
    Retorna a quantidade de proposições agrupadas por classificação NLP/subtema.

    Esta rota alimenta os gráficos de volume por subtema no frontend.

    Filtros disponíveis:
    - ano
    - tema_nlp
    - origem: Camara ou Senado
    - uf
    - partido
    - incluir_ruido
    - limit
    """
    query = select(
        Proposicao.classificacao_nlp,
        Proposicao.subtema,
        func.count(Proposicao.id_proposicao).label("total_proposicoes"),
    )

    if uf or partido:
        query = query.join(
            Parlamentar,
            Proposicao.id_autor == Parlamentar.id_parlamentar,
        )

    query = aplicar_filtros_analytics(
        query=query,
        ano=ano,
        tema_nlp=tema_nlp,
        origem=origem,
        uf=uf,
        partido=partido,
    )

    query = query.group_by(
        Proposicao.classificacao_nlp,
        Proposicao.subtema,
    )

    resultados = session.exec(query).all()

    contagem_por_subtema = {}

    for classificacao_nlp, subtema, total in resultados:
        nome = classificacao_nlp or subtema or "Não classificado"
        nome = str(nome).strip()

        if not incluir_ruido and nome in SUBTEMAS_ANALYTICS_IGNORADOS:
            continue

        contagem_por_subtema[nome] = contagem_por_subtema.get(nome, 0) + total

    itens_ordenados = sorted(
        contagem_por_subtema.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:limit]

    total_geral = sum(total for _, total in itens_ordenados)

    return [
        {
            "nome": nome,
            "total_proposicoes": total,
            "percentual": round((total / total_geral) * 100, 2)
            if total_geral
            else 0,
        }
        for nome, total in itens_ordenados
    ]

class TramitacaoResponse(BaseModel):
    data_hora: datetime
    orgao: str
    descricao: str

@app.get(
    "/proposicoes/{id_externo}/tramitacoes",
    response_model=List[TramitacaoResponse],
    responses=RESPOSTA_PROPOSICAO_NAO_ENCONTRADA,
)
def obter_tramitacoes(
    id_externo: str,
    session: Annotated[Session, Depends(get_session)],
):
    """
    Retorna a linha do tempo do andamento de uma proposição.
    """
    proposicao = session.exec(
        select(Proposicao).where(Proposicao.id_externo == id_externo)
    ).first()
    
    if not proposicao:
        raise HTTPException(
            status_code=404, 
            detail=f"Proposição com ID {id_externo} não foi encontrada no banco de dados."
        )

    statement = (
        select(Tramitacao)
        .where(Tramitacao.id_proposicao_externo == id_externo)
        .order_by(Tramitacao.data_hora.desc())
    )
    
    tramitacoes = session.exec(statement).all()

    return tramitacoes

@app.get(
    "/analytics/nuvem-palavras",
    responses=RESPOSTA_ORIGEM_INVALIDA,
)
def get_nuvem_palavras(
    session: Annotated[Session, Depends(get_session)],
    ano: Optional[int] = None,
    tema_nlp: Optional[str] = None,
    origem: Optional[str] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    """
    Retorna as palavras mais frequentes nas ementas das proposições.

    Esta rota deve ser usada na tela inicial do projeto para a nuvem de palavras.

    Filtros disponíveis:
    - ano
    - tema_nlp
    - origem: Camara ou Senado
    - uf
    - partido
    - limit
    """
    query = select(Proposicao.ementa)

    if uf or partido:
        query = query.join(
            Parlamentar,
            Proposicao.id_autor == Parlamentar.id_parlamentar,
        )

    query = aplicar_filtros_analytics(
        query=query,
        ano=ano,
        tema_nlp=tema_nlp,
        origem=origem,
        uf=uf,
        partido=partido,
    )

    ementas = session.exec(query).all()

    if not ementas:
        return []

    texto_completo = " ".join([ementa for ementa in ementas if ementa])

    if not texto_completo.strip():
        return []

    doc = nlp(texto_completo)

    ruidos_legislativos = {
        "lei", "alterar", "altera", "artigo", "inciso",
        "parágrafo", "paragrafo", "dispor", "estabelecer",
        "acrescentar", "dar", "providência", "providencia",
        "nº", "redação", "redacao", "sobre",

        "janeiro", "fevereiro", "março", "marco", "abril",
        "maio", "junho", "julho", "agosto", "setembro",
        "outubro", "novembro", "dezembro",

        "art.", "institui", "instituir", "federal", "dispõe",
        "dispoe", "requer", "decreto-lei", "audiência",
        "audiencia", "realização", "realizacao", "termos",
        "regimento", "interno", "objetivo", "ano", "nacional",
        "público", "publico", "programa", "incluir", "âmbito",
        "ambito", "ser",
    }

    palavras = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.like_num
        and len(token.text) > 2
        and token.lemma_.lower() not in ruidos_legislativos
        and token.text.lower() not in ruidos_legislativos
    ]

    contagem = Counter(palavras)
    top_palavras = contagem.most_common(limit)

    return [
        {
            "text": palavra,
            "value": frequencia,
        }
        for palavra, frequencia in top_palavras
    ]