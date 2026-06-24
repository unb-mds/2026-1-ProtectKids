"""
crawler/senado_api.py

Pipeline ETL — Senado Federal → PostgreSQL
"""
import sys
import os
import logging
import requests
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, SQLModel
import concurrent.futures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar

# Reaproveita a inteligência do pipeline da Câmara
from crawler.camara_api import (
    KEYWORDS,
    TEMA_PADRAO,
    classificar_com_ia,
    save_proposicoes,
    extrair_texto_pdf,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL_SENADO = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"

def find_value(obj, target_key: str):
    """Busca recursivamente por uma chave no JSON, ignorando maiúsculas/minúsculas e aninhamentos."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == target_key.lower():
                return v
            res = find_value(v, target_key)
            if res is not None:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_value(item, target_key)
            if res is not None:
                return res
    return None

def fetch_proposicoes_senado(keyword: str) -> list[dict]:
    params = {"palavraChave": keyword}
    headers = {"Accept": "application/json"}
    
    logger.info(f"Buscando no Senado pela keyword: '{keyword}'")
    try:
        resp = requests.get(BASE_URL_SENADO, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        dados = resp.json()
        
        materias = dados.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
        
        if isinstance(materias, dict):
            materias = [materias]
            
        for m in materias:
            m["_keyword_origem"] = keyword
            
        logger.info(f"Encontradas {len(materias)} matérias no Senado para '{keyword}'.")
        return materias
    except Exception as exc:
        logger.error(f"Erro ao buscar no Senado: {exc}")
        return []

def transform_materia_senado(materia_bruta: dict) -> Optional[tuple]:
    """O Adaptador resiliente atualizado com as chaves reais do Senado."""
    codigo_materia = find_value(materia_bruta, "Codigo")
    if not codigo_materia:
        return None
        
    id_externo_formatado = f"senado-{codigo_materia}"
    
    sigla = find_value(materia_bruta, "Sigla") or "PL"
    numero = find_value(materia_bruta, "Numero") or 0
    ano = find_value(materia_bruta, "Ano") or 2026
    
    ementa = find_value(materia_bruta, "Ementa") or "Sem ementa disponível"
    ementa = str(ementa).strip()
    
    # 1. Monta o Parlamentar (Tratando a string única do Senado)
    autor_string = find_value(materia_bruta, "Autor") or "Desconhecido"
    nome_autor = autor_string
    partido = "ND"
    uf = "ND"
    
    # Se a string vier no formato "Nome (PARTIDO/UF)", nós a dividimos:
    if "(" in autor_string and ")" in autor_string:
        partes = autor_string.split("(")
        nome_autor = partes[0].strip() # Pega o que vem antes do parêntese
        
        # Pega o que está dentro do parêntese e divide pela barra
        partido_uf = partes[1].replace(")", "").split("/")
        if len(partido_uf) == 2:
            partido = partido_uf[0].strip()
            uf = partido_uf[1].strip()
            
    # Como o Senado não enviou o ID numérico do autor, criamos um numérico baseado no nome
    id_autor = abs(hash(nome_autor)) % 1000000 
    
    parlamentar = Parlamentar(
        id_parlamentar=id_autor,
        nome=nome_autor,
        partido=partido,
        uf=uf
    )
        
    # 2. Formata a Data
    data_apres = None
    data_str = find_value(materia_bruta, "Data")
    if data_str:
        try:
            data_apres = datetime.fromisoformat(str(data_str)[:10]).date()
        except:
            pass
        # 3. NLP & PDF (ATUALIZADO COM FALLBACK PARA IMAGENS)
    subtema_origem = materia_bruta.get("_keyword_origem", "Geral")
    url_pdf_real = f"https://legis.senado.leg.br/sdleg-getter/documento/download/materia/{codigo_materia}"
    
    # extrai o texto limpo
    texto_pdf = extrair_texto_pdf(url_pdf_real)
    
    # O PLANO B: Se vier vazio (documento escaneado ou erro de leitura)
    if not texto_pdf:
        texto_pdf = (
            "O texto integral desta matéria está indisponível para extração digital.\n\n"
            f"Ementa Original: {ementa}"
        )
    classificacao_ia = classificar_com_ia(texto=texto_pdf, ementa=ementa)

    # 4. Monta a Proposicao
    proposicao = Proposicao(
        id_externo=id_externo_formatado,
        origem="Senado",
        id_autor=id_autor,
        tipo=str(sigla),
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        tema=TEMA_PADRAO,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf_real,
        subtema=subtema_origem,
        texto_integral=texto_pdf,
        classificacao_nlp=classificacao_ia,
)
    
    return (proposicao, parlamentar)

def obter_ids_existentes(origem_alvo: str) -> set:
    """
    Busca no banco todos os IDs externos já cadastrados para evitar 
    o reprocessamento de NLP.
    """
    with Session(engine) as session:
        statement = select(Proposicao.id_externo).where(Proposicao.origem == origem_alvo)
        resultados = session.exec(statement).all()
        return set(resultados)

def run_pipeline_senado():
    logger.info("=== Iniciando pipeline ETL do Senado Inteligente ===")
    SQLModel.metadata.create_all(engine)
    
    ids_existentes = obter_ids_existentes(origem_alvo="Senado")
    logger.info(f"Cache local: {len(ids_existentes)} proposições do Senado já existem no banco.")
    
    tuplas = []
    ids_processados_nesta_run = set()
    materias_ineditas = []
    
    # Coleta todas as matérias inéditas primeiro
    for keyword in KEYWORDS:
        materias = fetch_proposicoes_senado(keyword)
        for mat in materias:
            codigo = find_value(mat, "Codigo") 
            if not codigo:
                continue
                
            id_externo_formatado = f"senado-{codigo}"
            
            if id_externo_formatado in ids_existentes or id_externo_formatado in ids_processados_nesta_run:
                continue
                
            ids_processados_nesta_run.add(id_externo_formatado)
            materias_ineditas.append(mat)
                
    if not materias_ineditas:
        logger.info("=== Pipeline do Senado concluído. Nenhuma matéria inédita para processar hoje. ===")
        return

    logger.info(f"Iniciando download paralelo de {len(materias_ineditas)} PDFs do Senado...")

    # Dispara 10 downloads simultâneos
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {
            executor.submit(transform_materia_senado, mat): mat 
            for mat in materias_ineditas
        }
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                tuplas.append(resultado)
                    
    if tuplas:
        total_salvo = save_proposicoes(tuplas)
        logger.info(f"=== Pipeline do Senado concluído. {total_salvo} registros normalizados salvos. ===")
    else:
        logger.info("=== Pipeline do Senado concluído. Nenhuma matéria nova processada. ===")


if __name__ == "__main__":
    run_pipeline_senado()