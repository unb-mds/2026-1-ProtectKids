# 🛡️ ProtectKids

Plataforma de transparência e monitoramento legislativo voltada à análise de proposições relacionadas à proteção de crianças e adolescentes no ambiente digital.

## 🔎 Visão Geral

O **ProtectKids** é uma plataforma desenvolvida com o objetivo de centralizar, monitorar e analisar proposições legislativas em tramitação na **Câmara dos Deputados** e no **Senado Federal**.

O sistema tem foco em pautas relacionadas à proteção infantil, segurança digital de menores, privacidade, combate ao cyberbullying, exploração online e demais temas associados à proteção de crianças e adolescentes no ambiente digital.

A aplicação utiliza técnicas de **Processamento de Linguagem Natural (NLP)** para classificar automaticamente proposições legislativas e gerar indicadores analíticos, como rankings, filtros temáticos e nuvem de palavras.

---

## 🎨 Protótipos no Figma

Acesse os protótipos e materiais visuais do projeto:

- [Board do Projeto no Figma](https://www.figma.com/board/KBZc1R8RPPHBiZ1eoiRzFM/ProtectKids-mds?node-id=0-1&t=rHYhSFDUosKKo5mr-0)
- [Protótipo do Frontend](https://www.figma.com/design/OYd8YVckfiX0JiuJWmijDg/Prototipo-Site-MDS-squad-10?node-id=0-1&p=f&t=uiEuDatc96qDLOEM-0)

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.11**
- **FastAPI**
- **SQLModel**
- **SQLAlchemy**
- **PostgreSQL**
- **spaCy** para NLP

### Frontend

- **React**
- **Vite**
- **JavaScript**
- **Tailwind CSS**
- **Axios**

### Infraestrutura e DevOps

- **Docker**
- **Docker Compose**
- **GitHub Actions**
- **MkDocs**
- **GitHub Pages**

---

## 🚀 Como Rodar o Projeto Localmente

A execução local é feita com **Docker Compose**, subindo automaticamente os serviços de banco de dados, backend e frontend.

### Pré-requisitos

Antes de iniciar, verifique se você possui instalado:

- Git
- Docker
- Docker Compose

---

## 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-ProtectKids.git
cd 2026-1-ProtectKids
```

---

## 2. Configurar variáveis de ambiente

Na raiz do projeto, crie uma cópia do arquivo `.env.example` com o nome `.env`.

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Para execução local com Docker Compose, o arquivo `.env` deve conter valores semelhantes aos abaixo:

```env
POSTGRES_USER=protectkids_user
POSTGRES_PASSWORD=protectkids_password
POSTGRES_DB=protectkids_db

DATABASE_URL=postgresql://protectkids_user:protectkids_password@db:5432/protectkids_db

DEBUG_SQL=false
MAX_PAGES=2
ANO_INICIO_COLETA=2015
ANO_FIM_COLETA=2026
SPACY_MODEL=pt_core_news_sm

CORS_ORIGINS=http://localhost,http://localhost:80,http://localhost:5173,http://localhost:3000

VITE_API_URL=http://localhost:8000
```

> ⚠️ O arquivo `.env` contém configurações locais e não deve ser enviado para o GitHub.

---

## 3. Subir os serviços com Docker Compose

Na raiz do projeto, execute:

```bash
docker compose up -d --build
```
O esperado é que os serviços de banco, backend e frontend estejam em execução.

---

## 4. Popular o banco de dados

Após subir os containers, é necessário executar os crawlers para coletar e salvar os dados legislativos.

Execute os comandos abaixo na raiz do projeto:

```bash
docker compose exec backend python -m crawler.camara_api
docker compose exec backend python -m crawler.senado_api
docker compose exec backend python -m crawler.tramitacoes_api
docker compose exec backend python -m crawler.tramitacoes_senado_api
```

Esses comandos coletam proposições e tramitações da Câmara dos Deputados e do Senado Federal.

---

## 5. Acessar a aplicação

Após subir os serviços e popular o banco, acesse:

| Serviço | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger da API | http://localhost:8000/docs |

---


## 🧪 Testes e Cobertura de Código

O projeto possui testes automatizados para backend e frontend.

### Backend

O backend utiliza:

- `pytest`
- `pytest-cov`
- `TestClient` do FastAPI

Os testes estão localizados em:

```text
backend/tests/
```

Para executar os testes do backend, entre na pasta `backend`:

```bash
cd backend
```

No Windows PowerShell, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Execute os testes com cobertura:

```powershell
$env:PYTHONPATH="."
python -m pytest tests/ -q --cov=main --cov=models --cov=database --cov-report=term-missing --cov-fail-under=70
```

Resultado obtido na validação final:

```text
66 testes passando
Cobertura total: 92.02%
Cobertura mínima exigida: 70%
```

### Frontend

O frontend utiliza:

- `Vitest`
- `Testing Library`
- `@vitest/coverage-v8`

Para executar os testes do frontend via Docker, rode na raiz do projeto:

```bash
docker compose run --rm frontend npm test -- --run
```

Para executar os testes com cobertura:

```bash
docker compose run --rm frontend npm run test:coverage
```

Para validar o build de produção:

```bash
docker compose run --rm frontend npm run build
```

Resultado obtido na validação final:

```text
7 testes passando
Cobertura total: 80.31%
Build de produção executado com sucesso
```

## 📖 Documentação Completa

A documentação técnica do projeto está disponível via GitHub Pages:

[Documentação ProtectKids](https://unb-mds.github.io/2026-1-ProtectKids/)

A documentação inclui informações sobre:

- Visão geral do projeto
- Requisitos
- Arquitetura
- Infraestrutura
- Testes

---

## 👥 Equipe

| Nome | GitHub |
|---|---|
| Augusto Garcia | [@augustogmedeiros](https://github.com/augustogmedeiros) |
| Carlos Gabriel | [@cgbriel28](https://github.com/cgbriel28) |
| Danielly Mendes | [@DaniellyMendes](https://github.com/DaniellyMendes) |
| Mariana Soares | [@marispmorais](https://github.com/marispmorais) |
| Wanda Maria | [@Wandinhawright](https://github.com/Wandinhawright) |
| Yara Xavier | [@VegasVegas](https://github.com/VegasVegas) |

---

## 📄 Licença

Este projeto é destinado estritamente para fins acadêmicos e de pesquisa no contexto da disciplina Métodos de Desenvolvimento de Software da Universidade de Brasília.
