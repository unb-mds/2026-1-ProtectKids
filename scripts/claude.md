# CLAUDE.md

## Projeto

ProtectKids - Plataforma voltada ao monitoramento de dados legislativos com foco na protecao infanto-juvenil no ambiente digital.

## Constituicao

### Confiabilidade e Infraestrutura
1. O ambiente deve subir sempre com um unico comando `docker-compose up`. Nao adicione dependencias que exijam instalacoes complexas fora dos conteineres.
2. Credenciais, senhas e URLs de conexao com o banco de dados (ex: `DATABASE_URL`) devem usar variaveis de ambiente (`.env`). Nunca faca *hardcode* de dados sensiveis no codigo.
3. O codigo nao deve ser integrado a branch `main` se quebrar os linters ou os testes da nossa Pipeline de CI (GitHub Actions).

### Arquitetura e Integracao
4. O Backend (FastAPI) e o Frontend (React) devem permanecer estritamente desacoplados. A comunicacao deve ocorrer exclusivamente via requisicoes HTTP (REST), com o CORS devidamente configurado no backend.
5. Utilize o `SQLModel` para definir o banco de dados no Backend. Ele atua como fonte unica de verdade para a criacao de tabelas e validacao de dados (unindo SQLAlchemy e Pydantic).
6. O Crawler da Camara deve ser mantido dentro do diretorio `/backend`, reutilizando o ambiente Python, mas suas requisicoes externas devem ser separadas da logica de rotas do FastAPI.

### Regras de Negocio e Escopo
7. A extracao de dados da API da Camara dos Deputados deve filtrar rigorosamente proposicoes legislativas relacionadas ao escopo infanto-juvenil. Nao popule o banco com leis fora deste tema.
8. A documentacao tecnica (MkDocs) deve ser atualizada para refletir o estado real da arquitetura atual (C4 Model, diagramas e rotas da API).

---

## Convencoes tecnicas

- **Linguagens:** Python 3 (Backend/Crawler) e JavaScript/JSX (Frontend).
- **Frontend / UI:** React v19+ construido com Vite.
- **Backend / API:** FastAPI com Uvicorn.
- **Persistencia:** PostgreSQL v15 mapeado com SQLModel.
- **Testes:** Pytest (Backend) e Vitest + React Testing Library (Frontend).
- **Infraestrutura:** Docker e Docker-compose.
- **Estrutura de pastas principal:**
  - `backend/` - Codigo da API, modelos de banco e crawler.
  - `frontend/` - Aplicacao React/Vite.
  - `docs/` - Documentacao estatica usando MkDocs.
  - `.github/workflows/` — Pipelines de CI/CD.
- **Convencoes de nomenclatura:**
  - **Python (Backend):** `snake_case` para arquivos, funcoes e variaveis. `PascalCase` para classes e modelos do banco.
  - **React (Frontend):** `PascalCase.jsx` para componentes. `camelCase` para funcoes e variaveis.
  - **Testes:** Prefixo `test_` no Python e sufixo `.test.jsx` no React.

---

## Como me ajudar

- **Sempre proponha a mudanca minima** que realiza a tarefa solicitada. Nao refatore codigo nao relacionado "de passagem".
- **Se uma mudanca que voce fosse gerar viola a Constituicao, pare e avise** antes de escrever codigo. Nao tente conciliar silenciosamente.
- **Prefira escrever testes antes (ou junto) do codigo** quando a tarefa tem criterios de aceitacao objetivos. Cada criterio vira pelo menos um teste.
- **Uma tarefa por vez.** Nao implemente duas tarefas no mesmo diff, mesmo que parecam relacionadas.
- **Nao invente decisoes tecnicas fora do plano.** Se o plano da funcionalidade nao cobre o ponto, pare e pergunte antes de escolher biblioteca, arquitetura ou abordagem.
- **Commits pequenos** com mensagem referenciando a tarefa (ex: `feat(crawler): adiciona extracao de proposicoes da camara`).
- **Respeite o que ja existe.** Antes de criar um novo arquivo/estrutura, verifique se a solucao pode viver em codigo existente.
- **Leia antes de editar.** Use as ferramentas de leitura para entender o contexto do arquivo antes de aplicar mudancas.

---

## Fora de escopo padrao

A menos que o pedido diga o contrario, **nao faca**:

- Adicionar dependencias externas novas sem consultar a viabilidade no `requirements.txt` ou `package.json`.
- Reformatar codigo existente que fuja do escopo da Issue atual.
- Alterar a estrutura de pastas principal (`/backend`, `/frontend`, `/docs`).
- Tocar em testes de outras funcionalidades.
- Criar documentacao nao solicitada (README, comentarios "de cortesia", etc).
- Fazer commits sem revisao explicita.

---

## Funcionalidades

### Crawler da Camara dos Deputados

**Status:** tarefas

#### Spec

Contexto: A plataforma ProtectKids necessita de uma base de dados real para monitoramento legislativo. Este crawler consulta a API publica de Dados Abertos da Camara para alimentar nosso banco PostgreSQL interno com proposicoes que envolvem protecao infanto-juvenil.

Comportamento observavel: O sistema executa um script Python que faz requisicoes HTTP para a Camara, filtra os resultados com base em palavras-chave predefinidas, limpa os dados e insere as informacoes estruturadas (titulo, descricao, ementa) diretamente no banco de dados.

**Criterios de aceitacao:**
1. O script deve conectar-se com sucesso ao endpoint `/api/v2/proposicoes` da Camara.
2. Apenas proposicoes contendo termos relacionados a protecao infantil devem ser processadas.
3. Os dados devem ser mapeados corretamente para a classe `Proposicao` do SQLModel.
4. Os dados devem ser persistidos no PostgreSQL sem gerar duplicatas de ID.

**Casos de borda:**
- Caso a API da Camara retorne Timeout ou Status 500, o script deve fazer *log* do erro e tentar novamente (retry) sem derrubar a aplicacao.
- Leis com ementas vazias devem ser tratadas com valor padrao.

**Fora de escopo desta spec:**
- Extracao de dados do Senado Federal (apenas Camara neste momento).
- Visualizacao dos dados extraidos no frontend.

#### Plano

**Referencia:** spec acima. Constituicao relevante: principios 5, 6 e 7.

**Decisoes tecnicas:**

- **Ferramenta de Requisicao:**
  - **Escolha:** Biblioteca `requests`.
  - **Alternativas consideradas:** `Scrapy`, `httpx`.
  - **Rationale:** Como a API da Camara fornece JSON limpo e direto, o `Scrapy` e muito pesado (overkill) e feito para "raspar" HTML. O `requests` e simples, nativo e resolve o problema rapidamente para o MVP.

- **Persistencia de Dados:**
  - **Escolha:** Uso da sessao do SQLAlchemy importada do `database.py`.
  - **Rationale:** Garante que estamos inserindo dados validando a mesma tipagem e arquitetura que o FastAPI utiliza nas rotas.

**Tradeoffs aceitos:**
1. A extracao inicial nao rodara de forma agendada (Cron). Sera executada manualmente para popular a base de dados na Release 1. A automatizacao fica para o futuro.

**Dependencias:**
- `requests` (para comunicacao HTTP).
- `sqlmodel` (para manipulacao do banco).

#### Tarefas

1. **Estruturacao do Modulo**
   - **Depende de:** Integracao do FastAPI com Postgres (Concluida).
   - **Pronto quando:** A pasta `/crawler` for criada dentro de `/backend` com um arquivo `camara_api.py` base contendo importacoes.
   - **Fora de escopo:** Executar requisicoes reais a API.

2. **Implementacao da Busca (Fetch)**
   - **Depende de:** Estruturacao do Modulo.
   - **Pronto quando:** A funcao conseguir fazer um GET para a Camara, passar parametros de busca e retornar uma lista JSON de proposicoes no terminal.

3. **Implementacao da Carga (Load/Insert)**
   - **Depende de:** Implementacao da Busca.
   - **Pronto quando:** A funcao iterar sobre a lista JSON, instanciar objetos `Proposicao` e executar `session.commit()` persistindo os dados no Postgres.

### Dashboard de Produtividade (Observabilidade)

**Status:** tarefas

#### Spec

Contexto: Para avaliar o desempenho da equipe e acompanhar os indicadores do projeto, precisamos de um sistema de observabilidade que gere metricas de produtividade automaticamente a partir do historico do repositorio.

Comportamento observavel: O sistema utiliza GitHub Actions para rodar um script (via API do GitHub ou clone local) que varre o historico (`git log`) extraindo dados de commits, issues, tempo de resolucao e tamanho das diffs. Esses dados sao compilados, salvos em um arquivo `data.json` e exibidos em uma pagina web estatica (`index.html`) contendo graficos dinamicos renderizados com a biblioteca D3.js. 

**Criterios de aceitacao:**
1. Os dados brutos devem ser salvos e mantidos em um arquivo chamado `data.json`.
2. A pagina web (`index.html`) deve importar e utilizar `d3.js` para desenhar os graficos.
3. O sistema deve calcular indicadores como: Commit/Tempo, Issue/Tempo e Qualidade (caracteres por issue e diff do commit).
4. O processo deve ser totalmente automatizado via GitHub Actions a cada push na branch `main`.

#### Plano

**Referencia:** spec acima.

**Decisoes tecnicas:**
- **Coleta de Dados:**
  - **Escolha:** Script automatizado via GitHub Actions usando `git log` local e API do GitHub.
  - **Rationale:** Extrair os dados diretamente do ambiente de CI/CD garante que as metricas estejam sempre atualizadas sem depender da maquina local de nenhum desenvolvedor.

- **Visualizacao (Frontend do Dashboard):**
  - **Escolha:** HTML/CSS puro + `d3.js` lendo de um arquivo estatico `data.json`.
  - **Rationale:** E a forma mais leve de criar graficos complexos sem precisar levantar um framework inteiro so para uma pagina de metricas.

#### Tarefas

1. **Criar a Action de Coleta de Dados**
   - **Depende de:** `—`
   - **Pronto quando:** Uma Action for criada para extrair o `git log` e dados de issues, processar as metricas (commit/tempo, issue/tempo, qualidade/diff) e salvar o resultado em um arquivo `data.json`.

2. **Desenvolver a Interface Grafica (Dashboard)**
   - **Depende de:** `-`
   - **Pronto quando:** Um arquivo `index.html` for criado contendo a estrutura base, o CSS para estilizacao e a logica em `d3.js` capaz de ler o `data.json` mockado e renderizar os graficos de produtividade.

3. **Criar a Action de Atualizacao Continua**
   - **Depende de:** Tarefas 1 e 2.
   - **Pronto quando:** Uma segunda Action (ou um passo na primeira) for configurada para escutar eventos de commit na branch `main`, rodar o coletor de dados para atualizar o `data.json` e garantir que a pagina do dashboard exiba os dados mais recentes.