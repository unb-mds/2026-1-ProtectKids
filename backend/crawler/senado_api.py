"""
Pipeline ETL — Senado Federal → PostgreSQL
"""
import sys
import os
import logging
import requests
from typing import Optional
from datetime import datetime
from sqlmodel import Session, select, SQLModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import engine
from models import Proposicao, Parlamentar

# Reaproveita a inteligência do pipeline da Câmara!
from crawler.camara_api import KEYWORDS, classificar_com_ia, save_proposicoes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL_SENADO = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"

def fetch_proposicoes_senado(keyword: str) -> list[dict]:
    """Busca matérias no Senado baseadas em palavras-chave."""
    params = {"palavraChave": keyword}
    headers = {"Accept": "application/json"}
    
    logger.info(f"Buscando no Senado pela keyword: '{keyword}'")
    try:
        resp = requests.get(BASE_URL_SENADO, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        dados = resp.json()
        
        # O JSON do Senado é profundamente aninhado
        materias = dados.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
        
        # Se a API retornar apenas 1 resultado, ela devolve um dict em vez de list. Normalizamos isso:
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
    """O Adaptador: converte a estrutura do Senado para a estrutura do ProtectKids"""
    identificacao = materia_bruta.get("IdentificacaoMateria", {})
    dados_basicos = materia_bruta.get("DadosBasicosMateria", {})
    
    codigo_materia = identificacao.get("CodigoMateria")
    if not codigo_materia:
        return None
        
    id_externo_formatado = f"senado-{codigo_materia}"
    
    sigla = identificacao.get("SiglaSubtipoMateria", "PL")
    numero = identificacao.get("NumeroMateria", 0)
    ano = identificacao.get("AnoMateria", 2026)
    ementa = dados_basicos.get("EmentaMateria", "Sem ementa disponível").strip()
    
    # 1. Monta o Parlamentar (Autor)
    parlamentar = None
    id_autor = None
    autores_bloco = materia_bruta.get("Autores", {}).get("Autor", [])
    
    if isinstance(autores_bloco, dict):
        autores_bloco = [autores_bloco]
        
    if autores_bloco:
        autor_principal = autores_bloco[0]
        identificacao_autor = autor_principal.get("IdentificacaoParlamentar", {})
        
        id_autor_str = identificacao_autor.get("CodigoParlamentar")
        id_autor = int(id_autor_str) if id_autor_str else 888888
        
        parlamentar = Parlamentar(
            id_parlamentar=id_autor,
            nome=identificacao_autor.get("NomeParlamentar", autor_principal.get("NomeAutor", "Desconhecido")),
            partido=identificacao_autor.get("SiglaPartidoParlamentar", "ND"),
            uf=identificacao_autor.get("UfParlamentar", "ND")
        )
        
    # 2. Formata a Data
    data_apres = None
    data_str = dados_basicos.get("DataApresentacao")
    if data_str:
        try:
            data_apres = datetime.fromisoformat(data_str).date()
        except:
            pass

    # 3. NLP & PDF
    # Para o MVP do Senado, confiamos na Ementa para o NLP (o spaCy vai classificar com base na Ementa)
    subtema_origem = materia_bruta.get("_keyword_origem", "Geral")
    classificacao_ia = classificar_com_ia(texto=None, ementa=ementa)
    url_pdf_mock = f"https://legis.senado.leg.br/sdleg-getter/documento/download/materia/{codigo_materia}"

    # 4. Monta a Proposicao
    proposicao = Proposicao(
        id_externo=id_externo_formatado,
        origem="Senado",
        id_autor=id_autor,
        tipo=sigla,
        numero=int(numero),
        ano=int(ano),
        ementa=ementa,
        data_apresentacao=data_apres,
        url_inteiro_teor=url_pdf_mock,
        subtema=subtema_origem,
        texto_integral=None, # Pulando extração crua de PDF por enquanto para focar na integração
        classificacao_nlp=classificacao_ia
    )
    
    return (proposicao, parlamentar)

def run_pipeline_senado():
    logger.info("=== Iniciando pipeline ETL do Senado ===")
    SQLModel.metadata.create_all(engine)
    
    tuplas = []
    ids_processados = set()
    
    for keyword in KEYWORDS:
        materias = fetch_proposicoes_senado(keyword)
        for mat in materias:
            codigo = mat.get("IdentificacaoMateria", {}).get("CodigoMateria")
            if codigo and codigo not in ids_processados:
                ids_processados.add(codigo)
                resultado = transform_materia_senado(mat)
                if resultado:
                    tuplas.append(resultado)
                    
    total_salvo = save_proposicoes(tuplas)
    logger.info(f"=== Pipeline do Senado concluído. {total_salvo} registros normalizados salvos. ===")

if __name__ == "__main__":
    run_pipeline_senado()