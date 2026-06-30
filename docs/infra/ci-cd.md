# ⚙️ Integração Contínua (CI/CD)

O **ProtectKids** utiliza **GitHub Actions** para automatizar a execução dos testes a cada Pull Request direcionado à branch `main`, garantindo que nenhuma alteração quebre o comportamento esperado da API antes do merge.

---

## Pipeline Atual

**Arquivo:** `.github/workflows/ci.yml`

```yaml
name: ProtectKids CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout do código
      uses: actions/checkout@v4

    - name: Configurar Python 3.11
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Instalar dependências
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov httpx

    - name: Rodar Pytest com cobertura
      run: |
        cd backend
        pytest tests/ --cov=. --cov-report=term-missing
```

---

## Quando o CI é Acionado

| Evento | Comportamento |
|---|---|
| `push` na `main` | Roda a suíte completa de testes |
| `pull_request` para `main` | Roda a suíte e bloqueia merge se houver falha |

---

## O que o CI Valida

A cada execução, o pipeline garante que:

- Todas as dependências do `requirements.txt` são instaláveis no ambiente Linux
- Os **43 testes** da suíte passam sem falhas
- O relatório de cobertura (`--cov-report=term-missing`) é exibido no log da Action, mostrando quais linhas ainda não estão cobertas

!!! info "Por que `term-missing` e não `html`?"
    No CI não faz sentido gerar um relatório HTML — ninguém vai abrir um arquivo dentro do runner do GitHub Actions. O `term-missing` exibe a cobertura diretamente no log da Action, que é acessível por qualquer membro do squad na aba **Checks** do PR.

---

## Isolamento do Banco de Dados no CI

Os testes **não dependem do PostgreSQL** para rodar. O pipeline não precisa subir nenhum serviço de banco de dados porque a suíte utiliza **SQLite em memória**, substituindo a dependência `get_session` via `dependency_overrides` do FastAPI.

Isso significa que o CI é:

- ✅ **Rápido** — sem tempo de espera para subir containers
- ✅ **Simples** — sem configuração de serviços externos no workflow
- ✅ **Portável** — roda igual no Windows (local) e no Ubuntu (CI)

!!! warning "Atenção para testes futuros"
    Se futuramente forem criados testes que dependam de conexão real com o PostgreSQL (por exemplo, testes de migrations ou procedures), será necessário adicionar um serviço de banco ao workflow:
    ```yaml
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: senha
          POSTGRES_DB: legislativo_db
        ports:
          - 5432:5432
    ```

---

## Como Acompanhar o CI no GitHub

1. Abra o Pull Request no GitHub
2. Role até a seção **"Checks"** na parte inferior da página
3. Clique em **"Details"** ao lado do workflow `ProtectKids CI`
4. Acompanhe os steps em tempo real — o log do step **"Rodar Pytest com cobertura"** mostra o resultado de cada teste e a tabela de cobertura

!!! success "CI verde = PR pronto para review"
    Um ✅ verde no CI indica que todos os testes passaram e o código está seguro para ser revisado e mergeado.

---

## Dependências de Testes (`requirements.txt`)

As seguintes bibliotecas são necessárias para rodar a suíte localmente e no CI:

```
pytest==8.3.4
pytest-cov==7.1.0
httpx==0.27.0
```

!!! tip "Instalação local"
    ```bash
    pip install -r backend/requirements.txt
    ```