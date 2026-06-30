# 🛡️ ProtectKids

Plataforma de transparência e monitoramento legislativo baseada em Inteligência Artificial.
## 🔎 Visão Geral

O *ProtectKids* é uma plataforma desenvolvida para centralizar, monitorar e analisar proposições legislativas (Projetos de Lei) em tramitação na Câmara dos Deputados. O foco do sistema está em monitorar pautas voltadas para a proteção infantil, segurança digital de menores e o combate ao cyberbullying.

Utilizando técnicas de Processamento de Linguagem Natural (NLP), o sistema classifica automaticamente os temas das ementas extraídas, gerando indicadores inteligentes em um painel analítico para facilitar o acompanhamento dessas legislações.

---

# 🎨 Protótipo no Figma

Acesse o design e a prototipação da interface do projeto:

[Link do Projeto no Figma](https://www.figma.com/board/KBZc1R8RPPHBiZ1eoiRzFM/ProtectKids-mds?node-id=0-1&t=rHYhSFDUosKKo5mr-0)

[Link do protótipo do frontend](https://www.figma.com/design/OYd8YVckfiX0JiuJWmijDg/Prototipo-Site-MDS-squad-10?node-id=0-1&p=f&t=uiEuDatc96qDLOEM-0)

---

# 🛠️ Tecnologias Utilizadas

### Backend
- *Python* (FastAPI)
- *SQLModel* / *SQLAlchemy*
- *PostgreSQL*
- *spaCy* (NLP)

### Frontend
- *React* (Vite + JavaScript)
- *Tailwind CSS*

### Infraestrutura & DevOps
- *Docker* & *Docker Compose*
- *GitHub Actions* (CI/CD)

---
### 🚀 Como Rodar o Projeto (Quickstart)

Certifique-se de ter o **Git**, o **Docker** e o **Docker Compose** instalados e ativos em sua máquina antes de prosseguir.

**1. Clonar o repositório**

```bash
git clone https://github.com/unb-mds/2026-1-ProtectKids.git
cd 2026-1-ProtectKids
```

**2. Configurar Variáveis de Ambiente**
Antes de iniciar o Docker, é necessário definir as credenciais do banco de dados local.
- Na raiz do projeto, faça uma cópia do arquivo `.env.example` e renomeie-a para `.env`.
- Preencha o arquivo com os seguintes dados padrão de desenvolvimento:
```env
POSTGRES_USER=augusto
POSTGRES_PASSWORD=squad10
POSTGRES_DB=legislativo_db
DATABASE_URL=postgresql://augusto:squad10@db:5432/legislativo_db
MAX_PAGES=3
```

**3. Subir a Infraestrutura**
Baixe as imagens oficiais mais recentes da nuvem (GHCR) e inicie os serviços do banco, backend e frontend.
```bash
docker compose up --build -d
```
*(Aguarde alguns instantes até os contêineres inicializarem)*

**4. Popular o Banco de Dados (ETL)**
Para utilizar o sistema, é necessário baixar os dados oficiais da internet. Execute os scripts abaixo na ordem:

Primeiro, baixe as proposições de lei base da Câmara e do Senado:
```bash
docker-compose exec backend python -m crawler.camara_api
docker-compose exec backend python -m crawler.senado_api
```
Em seguida, baixe o histórico de tramitações das leis recém-salvas:
```bash
docker-compose exec backend python -m crawler.tramitacoes_api
```

**5. Acessar a aplicação**
- **Interface Web (Frontend):** http://localhost:5173
- **API Rest (Backend):** http://localhost:8000
- **Documentação Swagger:** http://localhost:8000/docs

---

## 🧪 Testes e Cobertura de Código

O backend utiliza [`pytest`](https://docs.pytest.org/) para testes automatizados e [`pytest-cov`](https://pytest-cov.readthedocs.io/) para medir a cobertura de código.

### Pré-requisitos

Certifique-se de que o ambiente virtual está ativado e as dependências instaladas:

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Rodando os testes

Para rodar toda a suíte de testes:

```bash
pytest tests/
```

### Gerando relatório de cobertura

Para rodar os testes e gerar um relatório visual em HTML:

```bash
pytest tests/ --cov=. --cov-report=html
```

Esse comando cria a pasta `htmlcov/` na raiz do backend. Para visualizar o relatório, abra o arquivo `htmlcov/index.html` no navegador.

Se preferir ver a cobertura direto no terminal, sem abrir o navegador:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

A flag `term-missing` mostra no terminal exatamente quais linhas do código ainda não estão cobertas por testes.

> ⚠️ **Atenção:** a pasta `htmlcov/` e o arquivo `.coverage` são gerados localmente por cada desenvolvedor e **não devem ser commitados**. Eles já estão listados no `.gitignore` do projeto.


**💡 Dica de Desenvolvimento:** Caso o banco precise ser totalmente resetado ou suas variáveis do `.env` alteradas, utilize o comando `docker-compose down -v` para destruir os volumes internos e limpe o ambiente antes de subir a infraestrutura novamente.

---

## 📖 Documentação Completa (MkDocs)

Para detalhes profundos sobre a arquitetura da aplicação, documentação técnica, modelagem do banco de dados PostgreSQL e guias de contribuição, consulte a nossa documentação oficial integrada:

[Documentação ProtectKids](https://unb-mds.github.io/2026-1-ProtectKids/)

## 👥 Equipe

| Nome | GitHub |
|---|---|
| Augusto Garcia | [@augustogmedeiros](https://github.com/augustogmedeiros) |
| Carlos Gabriel | [@cgbriel28](https://github.com/cgbriel28) |
| Danielly Mendes | [@DaniellyMendes](https://github.com/DaniellyMendes) |
| Mariana Soares | [@marispmorais](https://github.com/marispmorais) |
| Ryan Lira | [@Golira12](https://github.com/Golira12) |
| Wanda Maria | [@Wandinhawright](https://github.com/Wandinhawright) |
| Yara Xavier | [@VegasVegas](https://github.com/VegasVegas) |

## 📄 Licença

Este projeto é destinado estritamente para fins acadêmicos e de pesquisa.
