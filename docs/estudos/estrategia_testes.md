1. Conceitos de Testes Aplicados ao Contexto de MDS
Para garantir a confiabilidade do ProtectKids sem tornar o processo de desenvolvimento lento, adotamos o conceito clássico da Pirâmide de Testes. A ideia central é ter uma base massiva de testes rápidos e isolados, e menos testes no topo (que são mais lentos e complexos).

🧪 Testes Unitários (A Base)
Focam em validar o comportamento da menor unidade de código isolável no sistema (geralmente uma única função pura), sem tocar em componentes externos como bancos de dados ou APIs na internet.

No contexto do ProtectKids: Validar se uma função utilitária de limpeza remove caracteres especiais de uma ementa, ou se o extrator de texto formata strings corretamente.

🔗 Testes de Integração (O Meio)
Validam se dois ou mais componentes internos ou sistemas conversam corretamente entre si, garantindo que a união de partes isoladas funciona como o esperado.

No contexto do ProtectKids: Verificar se uma rota do FastAPI consegue receber um payload HTTP, processar as validações e persistir o modelo do SQLModel com sucesso dentro de um banco de dados de teste.

🖥️ Testes de Ponta a Ponta / E2E (O Topo)
Simulam a jornada completa do usuário final na aplicação, simulando cliques, fluxos de navegação e interações reais da tela até a persistência final de dados.

No contexto do ProtectKids: Simular um usuário entrando no Dashboard em React, aplicando um filtro por tema legislativo e verificando se os gráficos de barras atualizam dinamicamente com os dados reais vindos do banco de dados através da API.

2. Ecossistema do Back-End com pytest e SQLModel
O pytest é o framework padrão para testes em Python devido à sua simplicidade e suporte robusto a Fixtures. Fixtures são funções que preparam o ambiente para os testes (ligando recursos) e limpam tudo após a execução.

Simulação do Banco de Dados com SQLite em Memória
Para testar operações de banco sem sujar ou depender do PostgreSQL local/produção, criamos uma fixture que gera um banco SQLite efêmero em memória RAM a cada ciclo de teste:

import pytest
from sqlmodel import SQLModel, Session, create_engine
from core.database import get_session
from main import app

@pytest.fixture(name="session")
def session_fixture():
    # Cria uma engine isolada em memória para cada teste
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    # Injeta a sessão de testes nas dependências de rotas do FastAPI
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    from fastapi.testclient import TestClient
    yield TestClient(app)
    app.dependency_overrides.clear()

3. Isolando o Pipeline de ETL com Mocks (unittest.mock)
O pipeline de ETL não pode depender de conexões externas ativas. Se o portal da Câmara dos Deputados estiver fora do ar ou instável, a nossa esteira de CI/CD quebraria. Usamos objetos Mock para simular o comportamento dessas dependências externas.

Mockando a API da Câmara (requests.get): Interceptamos a chamada de rede e injetamos uma resposta estática (fictícia) contendo apenas o formato JSON esperado para validar se o nosso parser funciona.

Mockando o pdfplumber: Em vez de abrir e ler um arquivo binário pesado de um PDF real de proposição legislativa, simulamos o objeto do gerenciador de contexto do pdfplumber retornando um texto plano pré-definido.

4. Otimização de Performance no Motor de NLP (spaCy)
O carregamento do pipeline de linguagem do spaCy (pt_core_news_sm) exige processamento pesado e tempo de CPU significativos. Se instanciarmos o modelo a cada teste unitário executado, a suite de testes demorará minutos para rodar.

Estratégia de Otimização: Configurar uma fixture com o escopo de sessão (scope="session"). Isso garante que o modelo de IA seja carregado na memória RAM uma única vez no início da execução da suíte inteira de testes, sendo compartilhado entre todas as funções de teste que avaliam o classificador.

import pytest
import spacy

@pytest.fixture(scope="session")
def nlp_model():
    # Carregado apenas 1 vez para todos os testes do backend
    return spacy.load("pt_core_news_sm")

5. Ferramentas de Teste para o Frontend (React)
Para garantir o comportamento do Dashboard e a renderização correta dos gráficos sem quebras visuais, o ecossistema React utiliza duas ferramentas complementares de mercado:

Jest: Funciona como o executor de testes (test runner). Ele cria o ambiente simulado do navegador (DOM), gerencia as asserções (expect) e calcula a cobertura de código no ambiente JavaScript.

React Testing Library (RTL): Fornece utilitários focados em testar o comportamento dos componentes sob a perspectiva de uso do usuário real. Em vez de testar estados internos do código (como variáveis ocultas), o RTL busca o que está visível na tela (como buscar botões por textos ou papéis semânticos).

Casos de Testes Críticos no Frontend:
Renderização de Elementos-Chave: Validar se os cards de resumo e gráficos carregam com a paleta visual correta do projeto.

Interações do Painel: Simular o clique em uma tag de tema ou partido e verificar se a função de filtragem dispara a requisição esperada na API.