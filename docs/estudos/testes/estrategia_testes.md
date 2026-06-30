#  Estratégia de Testes

Para garantir a confiabilidade do **ProtectKids** sem tornar o processo de desenvolvimento lento, adotamos o conceito clássico da **Pirâmide de Testes**. A ideia central é ter uma base massiva de testes rápidos e isolados, e menos testes no topo (que são mais lentos e complexos).

---

## 1. Pirâmide de Testes

     Unitários (Base)

    Focam em validar o comportamento da menor unidade de código isolável no sistema (geralmente uma única função pura), **sem tocar em componentes externos** como bancos de dados ou APIs.

        example "No contexto do ProtectKids"
        Validar se uma função utilitária de limpeza remove caracteres especiais de uma ementa, ou se o extrator de texto formata strings corretamente.

    Integração (Meio)

    Validam se dois ou mais componentes internos ou sistemas conversam corretamente entre si, garantindo que a união de partes isoladas funciona como o esperado.

        example "No contexto do ProtectKids"
        Verificar se uma rota do FastAPI consegue receber um payload HTTP, processar as validações e persistir o modelo do SQLModel com sucesso dentro de um banco de dados de teste.

    E2E (Topo)

    Simulam a jornada completa do usuário final na aplicação, simulando cliques, fluxos de navegação e interações reais da tela até a persistência final de dados.

        example "No contexto do ProtectKids"
        Simular um usuário entrando no Dashboard em React, aplicando um filtro por tema legislativo e verificando se os gráficos de barras atualizam dinamicamente com os dados reais vindos do banco através da API.

---

## 2. Ecossistema do Backend com pytest e SQLModel

O `pytest` é o framework padrão para testes em Python devido à sua simplicidade e suporte robusto a **Fixtures**. Fixtures são funções que preparam o ambiente para os testes (ligando recursos) e limpam tudo após a execução.

### Simulação do Banco de Dados com SQLite em Memória

Para testar operações de banco sem sujar ou depender do PostgreSQL local/produção, criamos uma fixture que gera um banco **SQLite efêmero em memória RAM** a cada ciclo de teste:

```python title="tests/conftest.py"
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from database import get_session
from main import app

@pytest.fixture(name="session")
def session_fixture():
    engine_teste = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine_teste)
    with Session(engine_teste, expire_on_commit=False) as session:
        yield session
    SQLModel.metadata.drop_all(engine_teste)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    app.dependency_overrides[get_session] = get_session_override
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

!!! tip "Por que SQLite em vez de PostgreSQL?"
    O SQLite em memória garante que os testes rodem em **qualquer máquina**, sem precisar do Docker ou de um banco instalado. Cada teste começa com um banco limpo e isolado, sem interferência entre execuções.

---

## 3. Isolando o Pipeline de ETL com Mocks

O pipeline de ETL **não pode depender de conexões externas ativas**. Se o portal da Câmara dos Deputados estiver fora do ar ou instável, a nossa esteira de CI/CD quebraria. Usamos objetos `Mock` para simular o comportamento dessas dependências externas.

!!! abstract "Estratégias de Mock utilizadas"

    **Mockando a API da Câmara (`requests.get`)**

    Interceptamos a chamada de rede e injetamos uma resposta estática contendo apenas o formato JSON esperado para validar se o nosso parser funciona.

    **Mockando o `pdfplumber`**

    Em vez de abrir e ler um arquivo binário pesado de um PDF real, simulamos o objeto do gerenciador de contexto do `pdfplumber` retornando um texto plano pré-definido.

---

## 4. Otimização de Performance no Motor de NLP

O carregamento do pipeline de linguagem do spaCy (`pt_core_news_sm`) exige processamento pesado e tempo de CPU significativos. Se instanciarmos o modelo a cada teste unitário executado, a suíte de testes demorará minutos para rodar.

!!! success "Estratégia de Otimização: Fixture com escopo de sessão"
    Configurar uma fixture com `scope="session"` garante que o modelo de IA seja carregado na memória RAM **uma única vez** no início da execução da suíte inteira, sendo compartilhado entre todos os testes que avaliam o classificador.

```python title="tests/conftest.py"
import pytest
import spacy

@pytest.fixture(scope="session")
def nlp_model():
    # Carregado apenas 1 vez para todos os testes do backend
    return spacy.load("pt_core_news_sm")
```

---

## 5. Ferramentas de Teste para o Frontend (React)

Para garantir o comportamento do Dashboard e a renderização correta dos gráficos sem quebras visuais, o ecossistema React utiliza duas ferramentas complementares:

| Ferramenta | Papel |
|---|---|
| **Jest** | Executor de testes (test runner). Cria o ambiente simulado do navegador (DOM), gerencia as asserções (`expect`) e calcula a cobertura de código no ambiente JavaScript. |
| **React Testing Library (RTL)** | Fornece utilitários focados em testar o comportamento dos componentes sob a perspectiva do usuário real — busca o que está **visível na tela** (botões por texto, papéis semânticos), não estados internos do código. |

### Casos de Testes Críticos no Frontend

!!! note "Renderização de Elementos-Chave"
    Validar se os cards de resumo e gráficos carregam com a **paleta visual correta** do projeto.

!!! note "Interações do Painel"
    Simular o clique em uma tag de tema ou partido e verificar se a função de filtragem dispara a **requisição esperada na API**.

---

## 6. Como Rodar os Testes

### Pré-requisitos

```bash
# Windows (PowerShell)
cd backend
.\venv\Scripts\Activate.ps1

# Linux/macOS
cd backend
source venv/bin/activate
```

### Comandos principais

```bash
# Rodar toda a suíte
pytest tests/ -v

# Rodar com relatório de cobertura no terminal
pytest tests/ --cov=. --cov-report=term-missing -v

# Gerar relatório visual em HTML
pytest tests/ --cov=. --cov-report=html

# Rodar testes de um arquivo específico
pytest tests/test_analytics.py -v
```

!!! warning "Atenção"
    A pasta `htmlcov/` e o arquivo `.coverage` são gerados localmente e **não devem ser commitados**. Ambos já estão listados no `.gitignore` do projeto.

---

## 7. Cobertura Atual

```
Name                            Stmts   Miss  Cover
----------------------------------------------------
database.py                        10      2    80%
main.py                           165     31    81%
models.py                          38      0   100%
tests/conftest.py                  42      0   100%
tests/test_analytics.py            60      0   100%
tests/test_busca_por_id.py         49      0   100%
tests/test_filtros_origem.py       17      0   100%
tests/test_main.py                 49      0   100%
tests/test_normalizacao.py         17      0   100%
tests/test_tramitacoes.py          38      0   100%
----------------------------------------------------
TOTAL                             381     33    91%
```

!!! success "Cobertura Total: 91% — 43 testes, 0 falhas"
    O projeto supera a marca recomendada de 80% de cobertura, com `models.py` e todos os arquivos de teste atingindo **100%**.