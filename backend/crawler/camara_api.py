"""
crawler/camara_api.py

Pipeline ETL — Câmara dos Deputados → PostgreSQL
Busca proposições legislativas relacionadas à proteção infantil,
baixa os PDFs, extrai o texto integral, classifica via NLP (spaCy)
e salva as informações enriquecidas no banco.

Uso:
    # A partir da raiz do projeto (backend/)
    python -m crawler.camara_api

    # Ou diretamente, com o PYTHONPATH configurado:
    PYTHONPATH=.. python crawler/camara_api.py
"""

import sys
import os
import logging
import tempfile
import re
import unicodedata
import time
from typing import Optional
from sqlmodel import select, Session, SQLModel
from datetime import datetime
import requests
import fitz
import spacy
import concurrent.futures

# Garante que o módulo backend/ seja encontrado quando executado diretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Inicializa o modelo de NLP do spaCy em Português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    logger.error("Modelo 'pt_core_news_sm' do spaCy não encontrado. Execute o download no Docker antes.")
    raise

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
ENDPOINT_PROPOSICOES = f"{BASE_URL}/proposicoes"
ACCEPT_JSON = "application/json"
JSON_HEADERS = {"Accept": ACCEPT_JSON}
KEYWORDS = [
    "criança internet",
    "crianças internet",
    "adolescente internet",
    "adolescentes internet",
    "menor internet",
    "menores internet",

    "criança digital",
    "crianças digital",
    "adolescente digital",
    "adolescentes digital",
    "menor digital",
    "menores digital",

    "crianças redes sociais",
    "adolescentes redes sociais",
    "menores redes sociais",

    "crianças plataformas digitais",
    "adolescentes plataformas digitais",
    "menores plataformas digitais",

    "controle parental",
    "consentimento parental",
    "verificação de idade",
    "idade mínima redes sociais",

    "dados pessoais crianças",
    "dados pessoais adolescentes",
    "dados pessoais menores",
    "proteção de dados crianças",
    "proteção de dados adolescentes",
    "proteção de dados menores",
    "privacidade crianças",
    "privacidade adolescentes",
    "privacidade menores",
    "LGPD crianças",
    "LGPD adolescentes",

    "cyberbullying",
    "ciberbullying",
    "bullying virtual",
    "intimidação sistemática virtual",

    "aliciamento digital",
    "aliciamento online",
    "exploração sexual infantil online",
    "abuso sexual infantil online",
    "pornografia infantil online",

    "conteúdo nocivo crianças",
    "conteúdo nocivo adolescentes",
    "segurança digital crianças",
    "segurança digital adolescentes",
    "educação digital crianças",
    "educação digital adolescentes",
]

TEMA_PADRAO = "Proteção de Crianças e Adolescentes no Ambiente Digital"

PARAMS_BASE = {
    "siglaTipo": "PL",          
    "itens": 20,                 
    "ordem": "DESC",
    "ordenarPor": "id",
}

LIMITE_PAGINAS = int(os.getenv("MAX_PAGES", 3))
ANO_INICIO_COLETA = int(os.getenv("ANO_INICIO_COLETA", 2015))
ANO_FIM_COLETA = int(os.getenv("ANO_FIM_COLETA", datetime.now().year))

def fetch_proposicoes_por_keyword(keyword: str) -> list[dict]:
    """
    Consulta a API da Câmara por palavra-chave, varrendo ano a ano.

    Isso aumenta a cobertura histórica sem usar coleta ampla.
    Diferente da coleta ampla, aqui toda busca ainda precisa ter uma keyword.
    """
    resultados: list[dict] = []

    for ano in range(ANO_FIM_COLETA, ANO_INICIO_COLETA - 1, -1):
        for pagina in range(1, LIMITE_PAGINAS + 1):
            params = {
                **PARAMS_BASE,
                "keywords": keyword,
                "ano": ano,
                "pagina": pagina,
            }

            logger.info(
                "Buscando Câmara | keyword='%s' | ano=%s | página %s/%s",
                keyword,
                ano,
                pagina,
                LIMITE_PAGINAS,
            )

            response = fazer_requisicao_com_retry(
                ENDPOINT_PROPOSICOES,
                params=params,
                headers=JSON_HEADERS,
                timeout=60,
            )

            if response is None:
                logger.error(
                    "Falha ao buscar Câmara para keyword='%s', ano=%s, página=%s.",
                    keyword,
                    ano,
                    pagina,
                )
                break

            try:
                dados = response.json().get("dados", [])
            except ValueError:
                logger.error(
                    "Resposta inválida da Câmara para keyword='%s', ano=%s, página=%s.",
                    keyword,
                    ano,
                    pagina,
                )
                break

            if not dados:
                break

            for dado in dados:
                dado["_keyword_origem"] = keyword

            resultados.extend(dados)

            logger.info(
                "%s proposições encontradas | keyword='%s' | ano=%s | página=%s.",
                len(dados),
                keyword,
                ano,
                pagina,
            )

    return resultados

def fetch_todas_proposicoes() -> list[dict]:
    """
    Executa a extração principal da Câmara usando apenas palavras-chave.

    A coleta ampla por ano foi removida porque estava trazendo muitos
    falsos positivos fora do escopo do ProtectKids, como proposições sobre
    agropecuária, inadimplência, consumidor e temas administrativos.

    Estratégia atual:
    - busca por palavras-chave relacionadas à proteção digital infantil;
    - remove duplicatas pelo ID da API da Câmara;
    - transforma e classifica apenas os resultados encontrados por keyword.
    """
    todas: dict[int, dict] = {}

    for keyword in KEYWORDS:
        proposicoes = fetch_proposicoes_por_keyword(keyword)

        for prop in proposicoes:
            api_id = prop.get("id")

            if api_id and api_id not in todas:
                todas[api_id] = prop

    logger.info(
        "Total de proposições únicas encontradas por palavras-chave: %s",
        len(todas),
    )

    return list(todas.values())
def escolher_autor_preferencial(dados_autores: list[dict]) -> dict:
    """
    Escolhe o melhor autor para a proposição.

    A API da Câmara às vezes retorna autores institucionais como:
    - Câmara dos Deputados
    - Mesa Diretora
    - Comissão

    Para o ranking do ProtectKids, preferimos um autor parlamentar,
    quando existir.
    """
    if not dados_autores:
        return {}

    # 1. Preferência máxima: autor com URI de deputado.
    for autor in dados_autores:
        uri = autor.get("uri", "") or ""
        tipo = str(autor.get("tipo", "") or "").lower()

        if "/deputados/" in uri or "deputado" in tipo:
            return autor

    # 2. Segunda preferência: autor que já venha com partido e UF.
    for autor in dados_autores:
        if autor.get("siglaPartido") and autor.get("siglaUf"):
            return autor

    # 3. Fallback: mantém o primeiro autor retornado pela API.
    return dados_autores[0]


def fetch_autor_da_proposicao(id_proposicao_api: int) -> dict:
    """
    Busca o autor principal de uma proposição da Câmara.

    Preferimos autores parlamentares, quando existirem, para evitar salvar
    "Câmara dos Deputados" como autor principal no ranking.
    """
    url_autores = f"{BASE_URL}/proposicoes/{id_proposicao_api}/autores"

    resp_autores = fazer_requisicao_com_retry(
        url_autores,
        headers=JSON_HEADERS,
        timeout=30,
    )

    if resp_autores is None:
        logger.warning(
            "Não foi possível buscar autores da proposição %s.",
            id_proposicao_api,
        )
        return {}

    try:
        dados_autores = resp_autores.json().get("dados", [])
    except ValueError:
        logger.warning(
            "Resposta inválida ao buscar autores da proposição %s.",
            id_proposicao_api,
        )
        return {}

    if not dados_autores:
        return {}

    autor = escolher_autor_preferencial(dados_autores)
    uri_autor = autor.get("uri", "") or ""

    # Se não for deputado, provavelmente é autor institucional.
    # Nesse caso, não há partido/UF confiável.
    if "/deputados/" not in uri_autor:
        autor["siglaPartido"] = autor.get("siglaPartido") or "ND"
        autor["siglaUf"] = autor.get("siglaUf") or "ND"
        return autor

    resp_perfil = fazer_requisicao_com_retry(
        uri_autor,
        headers=JSON_HEADERS,
        timeout=30,
    )

    if resp_perfil is None:
        logger.warning(
            "Não foi possível buscar perfil do autor da proposição %s.",
            id_proposicao_api,
        )
        autor["siglaPartido"] = autor.get("siglaPartido") or "ND"
        autor["siglaUf"] = autor.get("siglaUf") or "ND"
        return autor

    try:
        perfil = resp_perfil.json().get("dados", {})
    except ValueError:
        logger.warning(
            "Resposta inválida ao buscar perfil do autor da proposição %s.",
            id_proposicao_api,
        )
        autor["siglaPartido"] = autor.get("siglaPartido") or "ND"
        autor["siglaUf"] = autor.get("siglaUf") or "ND"
        return autor

    status = perfil.get("ultimoStatus", {}) or {}

    autor["siglaPartido"] = (
        status.get("siglaPartido")
        or autor.get("siglaPartido")
        or "ND"
    )

    autor["siglaUf"] = (
        status.get("siglaUf")
        or autor.get("siglaUf")
        or "ND"
    )

    autor["nome"] = (
        status.get("nomeEleitoral")
        or perfil.get("nomeCivil")
        or autor.get("nome")
        or "Desconhecido"
    )

    return autor

def fetch_detalhes_proposicao(id_proposicao_api: int) -> dict:
    url_detalhes = f"{BASE_URL}/proposicoes/{id_proposicao_api}"

    resp = fazer_requisicao_com_retry(
        url_detalhes,
        headers=JSON_HEADERS,
        timeout=30,
    )

    if resp is None:
        logger.warning("Não foi possível buscar detalhes da proposição %s.", id_proposicao_api)
        return {}

    try:
        return resp.json().get("dados", {})
    except ValueError:
        logger.warning("Resposta inválida ao buscar detalhes da proposição %s.", id_proposicao_api)
        return {}
    
def fazer_requisicao_com_retry(
    url: str,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: int = 30,
    max_tentativas: int = 3,
    espera_inicial: int = 2,
) -> Optional[requests.Response]:
    """
    Executa uma requisição HTTP GET com retry simples.

    Retorna:
    - Response em caso de sucesso;
    - None em caso de falha definitiva.
    """
    for tentativa in range(1, max_tentativas + 1):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            if 400 <= response.status_code < 500:
                logger.warning(
                    "Erro cliente %s ao acessar %s. Sem retry.",
                    response.status_code,
                    url,
                )
                return None

            response.raise_for_status()
            return response

        except requests.Timeout:
            logger.warning(
                "Timeout ao acessar %s. Tentativa %s/%s.",
                url,
                tentativa,
                max_tentativas,
            )

        except requests.RequestException as exc:
            logger.warning(
                "Erro HTTP ao acessar %s. Tentativa %s/%s. Erro: %s",
                url,
                tentativa,
                max_tentativas,
                exc,
            )

        if tentativa < max_tentativas:
            espera = espera_inicial * tentativa
            logger.info("Aguardando %s segundos antes de tentar novamente.", espera)
            time.sleep(espera)

    logger.error("Falha definitiva ao acessar %s.", url)
    return None

def extrair_texto_pdf(url_pdf: Optional[str]) -> str:
    """
    Baixa um PDF e extrai seu texto usando PyMuPDF.

    A função usa arquivo temporário e garante limpeza com finally,
    evitando que arquivos fiquem acumulados em caso de erro.
    """
    if not url_pdf:
        return ""

    temp_pdf_path = None

    try:
        response = fazer_requisicao_com_retry(url_pdf, timeout=30)

        if response is None:
            return ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf_path = temp_pdf.name

        texto = ""

        with fitz.open(temp_pdf_path) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()

        return texto.strip()

    except Exception as exc:
        logger.exception("Erro ao extrair texto do PDF %s.", url_pdf)
        return ""

    finally:
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except OSError as exc:
                logger.warning(
                    "Não foi possível remover arquivo temporário %s: %s",
                    temp_pdf_path,
                    exc,
                )

CATEGORIA_PADRAO = "Proteção Geral no Ambiente Digital"

TERMOS_SIMBOLICOS = [
    "voto de aplauso",
    "voto de louvor",
    "voto de congratulação",
    "voto de congratulações",
    "voto de pesar",
    "título de cidadão",
    "titulo de cidadao",
    "homenagem",
    "sessão solene",
    "sessao solene",
    "data comemorativa",
    "dia nacional",
]

TERMOS_ESTRATEGICOS = [
    "audiência pública",
    "audiencia publica",
    "regime de urgência",
    "regime de urgencia",
    "convocação",
    "convocacao",
    "pedido de informação",
    "pedido de informacao",
    "comissão parlamentar",
    "comissao parlamentar",
    "requerimento",
]
CATEGORIAS_NLP = {
    "Exploração Sexual Online e Aliciamento Digital": {
        "frases": [
            "exploração sexual online",
            "exploracao sexual online",
            "exploração infantil online",
            "exploracao infantil online",
            "aliciamento digital",
            "aliciamento de criança pela internet",
            "aliciamento de crianca pela internet",
            "aliciamento de adolescente pela internet",
            "abuso sexual online",
            "pornografia infantil online",
            "material de abuso sexual infantil",
            "crime sexual pela internet",
            "violência sexual online",
            "violencia sexual online",
        ],
        "termos": [
            "exploração",
            "exploracao",
            "aliciamento",
            "abuso",
            "sexual",
            "pornografia",
            "pedofilia",
        ],
    },

    "Proteção de Dados e Privacidade Infantil": {
        "frases": [
            "proteção de dados de menores",
            "protecao de dados de menores",
            "dados pessoais de crianças",
            "dados pessoais de criancas",
            "dados pessoais de adolescentes",
            "tratamento de dados de crianças",
            "tratamento de dados de criancas",
            "tratamento de dados de adolescentes",
            "privacidade infantil",
            "privacidade de crianças",
            "privacidade de criancas",
            "consentimento parental",
            "consentimento dos pais",
            "lgpd",
            "lei geral de proteção de dados",
            "lei geral de protecao de dados",
            "biometria de crianças",
            "biometria de criancas",
            "reconhecimento facial de crianças",
            "reconhecimento facial de criancas",
        ],
        "termos": [
            "privacidade",
            "lgpd",
            "consentimento",
            "parental",
            "biometria",
        ],
    },

    "Redes Sociais e Plataformas Digitais": {
        "frases": [
            "rede social",
            "redes sociais",
            "plataforma digital",
            "plataformas digitais",
            "serviço digital",
            "servico digital",
            "serviços digitais",
            "servicos digitais",
            "controle parental",
            "verificação de idade",
            "verificacao de idade",
            "idade mínima",
            "idade minima",
            "perfil infantil",
            "conta infantil",
            "usuário menor de idade",
            "usuario menor de idade",
            "criança em rede social",
            "crianca em rede social",
            "adolescente em rede social",
            "responsabilidade das plataformas",
            "responsabilidade de plataformas digitais",
            "influenciador mirim",
            "influenciadores mirins",
        ],
        "termos": [
            "rede",
            "social",
            "plataforma",
            "aplicativo",
            "perfil",
            "conta",
            "idade",
            "verificação",
            "verificacao",
            "parental",
            "influenciador",
            "influenciadores",
            "responsabilidade",
        ],
    },

    "Conteúdo Nocivo e Segurança Online": {
        "frases": [
            "conteúdo nocivo",
            "conteudo nocivo",
            "conteúdo impróprio",
            "conteudo improprio",
            "conteúdo inadequado",
            "conteudo inadequado",
            "segurança online",
            "seguranca online",
            "segurança digital",
            "seguranca digital",
            "recomendação algorítmica",
            "recomendacao algoritmica",
            "moderação de conteúdo",
            "moderacao de conteudo",
            "tempo de tela",
            "conteúdo pornográfico",
            "conteudo pornografico",
            "conteúdo violento",
            "conteudo violento",
            "automutilação",
            "automutilacao",
            "suicídio",
            "suicidio",
        ],
        "termos": [
            "conteúdo",
            "conteudo",
            "nocivo",
            "impróprio",
            "improprio",
            "inadequado",
            "segurança",
            "seguranca",
            "moderação",
            "moderacao",
            "algoritmo",
            "algorítmico",
            "algoritmico",
            "recomendação",
            "recomendacao",
            "tela",
            "pornográfico",
            "pornografico",
            "violento",
        ],
    },

    "Cyberbullying e Crimes Virtuais": {
        "frases": [
            "cyberbullying",
            "intimidação sistemática virtual",
            "intimidacao sistematica virtual",
            "crime virtual",
            "crime cibernético",
            "crime cibernetico",
            "violência digital",
            "violencia digital",
            "ameaça virtual",
            "ameaca virtual",
            "assédio virtual",
            "assedio virtual",
            "perseguição virtual",
            "perseguicao virtual",
            "humilhação online",
            "humilhacao online",
        ],
        "termos": [
            "cyberbullying",
            "virtual",
            "cibernético",
            "cibernetico",
            "crime",
            "ameaça",
            "ameaca",
            "assédio",
            "assedio",
            "perseguição",
            "perseguicao",
            "humilhação",
            "humilhacao",
            "internet",
            "online",
        ],
    },

    "Educação Digital e Cidadania Online": {
        "frases": [
            "educação digital",
            "educacao digital",
            "cidadania digital",
            "alfabetização midiática",
            "alfabetizacao midiática",
            "alfabetizacao midiática",
            "alfabetização digital",
            "alfabetizacao digital",
            "uso seguro da internet",
            "segurança digital nas escolas",
            "seguranca digital nas escolas",
            "prevenção ao cyberbullying",
            "prevencao ao cyberbullying",
            "educação para uso da internet",
            "educacao para uso da internet",
        ],
        "termos": [
            "educação",
            "educacao",
            "cidadania",
            "alfabetização",
            "alfabetizacao",
            "midiática",
            "midiatica",
            "escola",
            "ensino",
            "prevenção",
            "prevencao",
            "conscientização",
            "conscientizacao",
        ],
    },
}

MAX_CARACTERES_NLP = 80000
PONTUACAO_MINIMA = 2


def normalizar_texto(valor: Optional[str]) -> str:
    """
    Normaliza texto para comparação:
    - minúsculas;
    - sem acentos;
    - espaços normalizados.
    """
    if not valor:
        return ""

    texto = str(valor).lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

TERMOS_INFANTIS_ESCOPO = (
    "criança",
    "crianca",
    "crianças",
    "criancas",
    "adolescente",
    "adolescentes",
    "menor",
    "menores",
    "infantil",
    "infantojuvenil",
    "infanto-juvenil",
)

TERMOS_DIGITAIS_ESCOPO = (
    "internet",
    "online",
    "digital",
    "digitais",
    "virtual",
    "virtuais",
    "rede social",
    "redes sociais",
    "plataforma digital",
    "plataformas digitais",
    "aplicativo",
    "aplicativos",
    "dados pessoais",
    "proteção de dados",
    "protecao de dados",
    "privacidade",
    "lgpd",
    "algoritmo",
    "algoritmos",
    "inteligência artificial",
    "inteligencia artificial",
)

TERMOS_RISCO_EXPLICITO = (
    "cyberbullying",
    "ciberbullying",
    "bullying virtual",
    "intimidação sistemática virtual",
    "intimidacao sistematica virtual",
    "aliciamento digital",
    "aliciamento online",
    "exploração sexual infantil online",
    "exploracao sexual infantil online",
    "abuso sexual infantil online",
    "pornografia infantil online",
    "controle parental",
    "consentimento parental",
)

TERMOS_FORA_ESCOPO = (
    "herança digital",
    "heranca digital",
    "patrimônio digital",
    "patrimonio digital",
    "bens digitais",
    "ativo digital",
    "ativos digitais",
    "rastreabilidade bovina",
    "agricultura familiar",
    "inadimplente",
    "inadimplentes",
    "inadimplência",
    "inadimplencia",
    "débitos decorrentes",
    "debitos decorrentes",
    "serviços públicos essenciais",
    "servicos publicos essenciais",
    "código de defesa do consumidor",
    "codigo de defesa do consumidor",
    "cadastro de inadimplente",
    "cadastros de inadimplentes",
)


def contem_termo(conteudo: str, termos: tuple[str, ...]) -> bool:
    return any(normalizar_texto(termo) in conteudo for termo in termos)


def esta_no_escopo_protectkids(texto: str | None, ementa: str | None) -> bool:
    """
    Decide se a proposição pertence ao escopo do ProtectKids.

    Usa somente a ementa e o texto real da proposição.
    Não usa a keyword de busca, para evitar falso positivo.
    """
    conteudo = normalizar_texto(f"{ementa or ''} {texto or ''}")

    if not conteudo:
        return False

    if contem_termo(conteudo, TERMOS_FORA_ESCOPO):
        return False

    if contem_termo(conteudo, TERMOS_RISCO_EXPLICITO):
        return True

    tem_infantil = contem_termo(conteudo, TERMOS_INFANTIS_ESCOPO)
    tem_digital = contem_termo(conteudo, TERMOS_DIGITAIS_ESCOPO)

    return tem_infantil and tem_digital

def gerar_lemas(texto: Optional[str]) -> list[str]:
    """
    Gera lemas normalizados usando spaCy.
    O texto é limitado para evitar estouro de memória com PDFs muito grandes.
    """
    if not texto:
        return []

    texto_limitado = str(texto)[:MAX_CARACTERES_NLP]
    doc = nlp(texto_limitado.lower())

    return [
        normalizar_texto(token.lemma_)
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.like_num
        and len(token.text) > 2
    ]


def calcular_pontuacao_categoria(
    regras: dict,
    ementa_normalizada: str,
    texto_normalizado: str,
    lemas_ementa: list[str],
    lemas_texto: list[str],
) -> int:
    """
    Calcula pontuação ponderada de uma categoria.

    A ementa tem peso maior porque costuma resumir melhor a proposição.
    O texto integral entra como reforço, não como decisão absoluta.
    """
    pontuacao = 0

    frases = regras.get("frases", [])
    termos = {normalizar_texto(termo) for termo in regras.get("termos", [])}

    for frase in frases:
        frase_normalizada = normalizar_texto(frase)

        if frase_normalizada and frase_normalizada in ementa_normalizada:
            pontuacao += 6

        if frase_normalizada and frase_normalizada in texto_normalizado:
            pontuacao += 2

    for lema in lemas_ementa:
        if lema in termos:
            pontuacao += 3

    for lema in lemas_texto:
        if lema in termos:
            pontuacao += 1

    return pontuacao


def classificar_com_ia(texto: Optional[str], ementa: str) -> str:
    """
    Classifica a proposição usando:
    - filtros rápidos para ruído legislativo;
    - spaCy para lematização;
    - pontuação ponderada por categoria.

    Observação:
    esta abordagem é NLP heurístico, não modelo supervisionado treinado.
    """
    ementa_normalizada = normalizar_texto(ementa)
    texto_normalizado = normalizar_texto(texto)

    if not ementa_normalizada and not texto_normalizado:
        return CATEGORIA_PADRAO

    is_simbolico = any(
        normalizar_texto(termo) in ementa_normalizada
        for termo in TERMOS_SIMBOLICOS
    )

    is_estrategico = any(
        normalizar_texto(termo) in ementa_normalizada
        for termo in TERMOS_ESTRATEGICOS
    )

    if is_simbolico and not is_estrategico:
        return "Simbólico/Ruído"

    if is_estrategico:
        return "Atuação Legislativa e Fiscalização"

    try:
        lemas_ementa = gerar_lemas(ementa)
        lemas_texto = gerar_lemas(texto)

        pontuacoes = {
            categoria: calcular_pontuacao_categoria(
                regras=regras,
                ementa_normalizada=ementa_normalizada,
                texto_normalizado=texto_normalizado,
                lemas_ementa=lemas_ementa,
                lemas_texto=lemas_texto,
            )
            for categoria, regras in CATEGORIAS_NLP.items()
        }

        categoria_vencedora = max(pontuacoes, key=pontuacoes.get)

        if pontuacoes[categoria_vencedora] >= PONTUACAO_MINIMA:
            return categoria_vencedora

        return CATEGORIA_PADRAO

    except Exception:
        logger.exception("Erro no processamento NLP.")
        return CATEGORIA_PADRAO

def contem_indicador_protecao_infantil(
    texto: Optional[str],
    ementa: Optional[str],
) -> bool:
    """
    Mantida por compatibilidade com outros arquivos.
    Usa a nova regra de escopo.
    """
    return esta_no_escopo_protectkids(texto, ementa)

def transform_proposicao(dado_bruto: dict, autor_bruto: dict) -> Optional[tuple]:
    sigla = dado_bruto.get("siglaTipo", "PL")
    numero = dado_bruto.get("numero")
    ano = dado_bruto.get("ano")
    ementa = dado_bruto.get("ementa", "").strip()

    if not numero or not ano or not ementa:
        return None

    id_bruto = dado_bruto.get("id")
    id_externo_formatado = f"camara-{id_bruto}"

    parlamentar = None
    id_autor = None

    if autor_bruto:
        uri = autor_bruto.get("uri", "")

        try:
            id_autor = int(uri.rstrip("/").split("/")[-1])
        except (ValueError, IndexError):
            logger.warning("Não foi possível extrair ID do autor pela URI: %s", uri)
            id_autor = 999999

        parlamentar = Parlamentar(
            id_parlamentar=id_autor,
            nome=autor_bruto.get("nome", "Desconhecido"),
            partido=autor_bruto.get("siglaPartido", "ND"),
            uf=autor_bruto.get("siglaUf", "ND"),
        )

    data_apres = None
    data_str = dado_bruto.get("dataApresentacao")

    if data_str:
        try:
            data_apres = datetime.fromisoformat(data_str).date()
        except ValueError:
            logger.warning("Data de apresentação inválida: %s", data_str)

    url_pdf = dado_bruto.get("urlInteiroTeor")
    texto_pdf = extrair_texto_pdf(url_pdf) or ""

    subtema_origem = dado_bruto.get("_keyword_origem", "Geral")

    if not esta_no_escopo_protectkids(
        texto=texto_pdf,
        ementa=ementa,
    ):
        logger.info(
            "Proposição Câmara %s descartada: fora do escopo ProtectKids. Ementa: %s",
            id_externo_formatado,
            ementa[:180],
        )
        return None
    classificacao_ia = classificar_com_ia(texto_pdf, ementa)

    proposicao = Proposicao(
        id_externo=id_externo_formatado,
        id_autor=id_autor,
        origem="Camara",
        tipo=sigla,
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        tema=TEMA_PADRAO,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf,
        subtema=subtema_origem,
        texto_integral=texto_pdf,
        classificacao_nlp=classificacao_ia,
    )

    return (proposicao, parlamentar)

def obter_ids_existentes(origem_alvo: str) -> set:
    """
    Busca no banco todos os IDs externos já cadastrados para evitar 
    o download repetido de PDFs e reprocessamento de NLP.
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(Proposicao.origem == origem_alvo)
        resultados = session.exec(statement).all()
        return set(resultados)

def save_proposicoes(tuplas_prop_autor: list[tuple]) -> int:
    inseridos = 0
    with Session(engine) as session:
        for prop, autor in tuplas_prop_autor:
            try:
                if autor:
                    existente_autor = session.exec(
                        select(Parlamentar).where(Parlamentar.id_parlamentar == autor.id_parlamentar)
                    ).first()
                    if not existente_autor:
                        session.add(autor)
                        session.flush()

                existente_prop = session.exec(
                    select(Proposicao).where(Proposicao.id_externo == prop.id_externo)
                ).first()
                
                if not existente_prop:
                    session.add(prop)
                    session.flush()
                    inseridos += 1
                    
            except Exception as exc:
                logger.warning(f"Erro ao adicionar proposicao {prop.numero}: {exc}")
                session.rollback()
                continue
                
        session.commit()
    return inseridos

def processar_materia_individual(dado: dict) -> Optional[tuple]:
    """
    Função isolada para ser executada em paralelo (Thread).
    Faz o download do PDF e passa pela IA de forma independente.
    """
    id_bruto = dado.get("id")
    id_externo_formatado = f"camara-{id_bruto}"

    try:
        autor_bruto = fetch_autor_da_proposicao(id_bruto)
        detalhes_brutos = fetch_detalhes_proposicao(id_bruto)
        
        dado["urlInteiroTeor"] = detalhes_brutos.get("urlInteiroTeor")
        
        resultado = transform_proposicao(dado, autor_bruto)
        if resultado:
            logger.info(f"Nova matéria processada: {id_externo_formatado}")
        return resultado
    
    except Exception:
        logger.exception(
            "Erro na thread ao processar %s.",
            id_externo_formatado,
        )
    return None
def run_pipeline() -> None:
    logger.info("=== Iniciando pipeline ETL Inteligente (PDF + NLP) ===")
    SQLModel.metadata.create_all(engine)

    ids_existentes = obter_ids_existentes(origem_alvo="Camara")
    logger.info(f"Cache local: {len(ids_existentes)} proposições da Câmara já existem.")

    dados_brutos = fetch_todas_proposicoes()
    if not dados_brutos:
        logger.warning("Nenhuma proposição capturada na extração externa.")
        return

    tuplas: list[tuple] = []
    ids_processados_nesta_run = set()
    dados_ineditos = []

    for dado in dados_brutos:
        id_bruto = dado.get("id")
        id_externo_formatado = f"camara-{id_bruto}"
        
        if id_externo_formatado not in ids_existentes and id_externo_formatado not in ids_processados_nesta_run:
            dados_ineditos.append(dado)
            ids_processados_nesta_run.add(id_externo_formatado)

    if not dados_ineditos:
        logger.info("=== Pipeline concluído. Nenhuma matéria inédita para processar hoje. ===")
        return

    logger.info(f"Iniciando download paralelo de {len(dados_ineditos)} PDFs. Isso será rápido...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {
            executor.submit(processar_materia_individual, d): d
            for d in dados_ineditos
        }
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                tuplas.append(resultado)

    if tuplas:
        total_salvo = save_proposicoes(tuplas)
        logger.info(f"=== Pipeline concluído. {total_salvo} novos registros inseridos com NLP. ===")

if __name__ == "__main__":
    run_pipeline()