# Docker Compose

O projeto ProtectKids utiliza o Docker Compose para organizar e executar os serviços necessários para o funcionamento da aplicação em ambiente local.

O arquivo `docker-compose.yml` define três serviços principais:

* `db`: banco de dados PostgreSQL;
* `backend`: API desenvolvida com FastAPI;
* `frontend`: interface web desenvolvida com React e Vite.

Além dos serviços, o arquivo também define um volume persistente para armazenar os dados do banco PostgreSQL.

---

## Estrutura geral

```yaml
services:
  db:
    ...
  backend:
    ...
  frontend:
    ...

volumes:
  postgres_data:
```

A chave `services` agrupa os containers da aplicação.
A chave `volumes` define volumes persistentes utilizados pelos containers.

---

## Serviço `db`

O serviço `db` é responsável por executar o banco de dados PostgreSQL utilizado pelo backend.

```yaml
db:
  container_name: ProtectKids_db
  image: postgres:15
  env_file:
    - .env
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 10s
```

### `container_name`

```yaml
container_name: ProtectKids_db
```

Define o nome do container do banco de dados.

Esse nome facilita a identificação do container ao executar comandos como:

```bash
docker ps
```

---

### `image`

```yaml
image: postgres:15
```

Define que o serviço utilizará a imagem oficial do PostgreSQL na versão 15.

---

### `env_file`

```yaml
env_file:
  - .env
```

Indica que o serviço deve carregar variáveis de ambiente a partir do arquivo `.env`.

No caso do PostgreSQL, as principais variáveis esperadas são:

```env
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=nome_do_banco
```

Essas variáveis configuram o usuário, a senha e o nome do banco criado no container.

---

### `ports`

```yaml
ports:
  - "5432:5432"
```

Mapeia a porta do PostgreSQL.

O primeiro valor representa a porta da máquina local.
O segundo valor representa a porta interna do container.

Neste caso:

```text
localhost:5432 -> container:5432
```

Isso permite acessar o banco PostgreSQL localmente pela porta `5432`.

---

### `volumes`

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Define um volume persistente para armazenar os dados do PostgreSQL.

Sem esse volume, os dados poderiam ser perdidos ao remover o container.

O volume `postgres_data` é definido no final do arquivo:

```yaml
volumes:
  postgres_data:
```

---

### `healthcheck`

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

O `healthcheck` verifica se o PostgreSQL está pronto para receber conexões.

O comando utilizado é:

```bash
pg_isready
```

Ele testa a conexão usando as variáveis:

```env
POSTGRES_USER
POSTGRES_DB
```

O uso de `$${POSTGRES_USER}` e `$${POSTGRES_DB}` é necessário para evitar que o Docker Compose tente substituir essas variáveis antes da execução dentro do container.

Configurações do `healthcheck`:

| Campo          | Função                                           |
| -------------- | ------------------------------------------------ |
| `test`         | Comando usado para testar se o banco está pronto |
| `interval`     | Intervalo entre as tentativas                    |
| `timeout`      | Tempo máximo de espera por tentativa             |
| `retries`      | Número de tentativas antes de marcar como falha  |
| `start_period` | Tempo inicial antes de começar a validar falhas  |

---

## Serviço `backend`

O serviço `backend` é responsável por executar a API do projeto ProtectKids.

```yaml
backend:
  container_name: ProtectKids_backend
  build:
    context: ./backend
    dockerfile: Dockerfile
  # image: ghcr.io/unb-mds/2026-1-protectkids-backend:latest
  ports:
    - "8000:8000"
  volumes:
    - ./backend:/app
  depends_on:
    db:
      condition: service_healthy
  env_file:
    - .env
  command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### `container_name`

```yaml
container_name: ProtectKids_backend
```

Define o nome do container do backend.

Esse nome facilita a identificação do serviço durante testes e depuração.

---

### `build`

```yaml
build:
  context: ./backend
  dockerfile: Dockerfile
```

Indica que a imagem do backend será construída localmente a partir da pasta `./backend`.

O campo `dockerfile` informa qual Dockerfile será utilizado para montar a imagem.

Essa configuração é adequada para ambiente de desenvolvimento, pois permite executar o backend diretamente a partir do código local do projeto.

---

### Imagem GHCR comentada

```yaml
# image: ghcr.io/unb-mds/2026-1-protectkids-backend:latest
```

Essa linha está comentada e representa uma alternativa para usar uma imagem publicada no GitHub Container Registry.

No ambiente atual de desenvolvimento, foi priorizado o uso de `build` local para evitar problemas de autenticação com imagem privada no GHCR.

Caso a imagem seja futuramente publicada de forma acessível, essa configuração poderá ser revisada.

---

### `ports`

```yaml
ports:
  - "8000:8000"
```

Mapeia a porta da API.

Neste caso:

```text
localhost:8000 -> container:8000
```

Com isso, a API pode ser acessada em:

```text
http://localhost:8000
```

A documentação Swagger da API fica disponível em:

```text
http://localhost:8000/docs
```

---

### `volumes`

```yaml
volumes:
  - ./backend:/app
```

Monta a pasta local `./backend` dentro do container no caminho `/app`.

Isso permite que alterações feitas no código local sejam refletidas dentro do container.

Essa configuração é útil para desenvolvimento, principalmente junto com o modo `--reload` do Uvicorn.

---

### `depends_on`

```yaml
depends_on:
  db:
    condition: service_healthy
```

Define que o backend depende do serviço `db`.

Com a condição `service_healthy`, o backend só será iniciado depois que o banco PostgreSQL passar no `healthcheck`.

Isso evita que a API tente se conectar ao banco antes dele estar pronto.

---

### `env_file`

```yaml
env_file:
  - .env
```

Carrega as variáveis de ambiente do arquivo `.env`.

O backend utiliza principalmente a variável `DATABASE_URL`, responsável pela conexão com o banco de dados.

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@db:5432/nome_do_banco
```

Dentro do Docker Compose, o host do banco deve ser `db`, pois esse é o nome do serviço definido no arquivo.

---

### `command`

```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Define o comando executado ao iniciar o container do backend.

Esse comando inicia a aplicação FastAPI usando o Uvicorn.

Partes do comando:

| Trecho           | Função                                                               |
| ---------------- | -------------------------------------------------------------------- |
| `uvicorn`        | Servidor ASGI usado para executar a API                              |
| `main:app`       | Indica que a aplicação está no arquivo `main.py`, variável `app`     |
| `--host 0.0.0.0` | Permite acesso externo ao container                                  |
| `--port 8000`    | Define a porta da API                                                |
| `--reload`       | Reinicia automaticamente o servidor ao detectar alterações no código |

O parâmetro `--reload` é recomendado para desenvolvimento, mas não deve ser utilizado em produção.

---

## Serviço `frontend`

O serviço `frontend` é responsável por executar a interface web do ProtectKids.

```yaml
frontend:
  container_name: ProtectKids_frontend
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "5173:5173"
  volumes:
    - ./frontend:/app
    - /app/node_modules
  depends_on:
    - backend
  command: npm run dev -- --host
```

---

### `container_name`

```yaml
container_name: ProtectKids_frontend
```

Define o nome do container do frontend.

---

### `build`

```yaml
build:
  context: ./frontend
  dockerfile: Dockerfile
```

Indica que a imagem do frontend será construída localmente a partir da pasta `./frontend`.

O Dockerfile usado será o arquivo localizado dentro dessa pasta.

---

### `ports`

```yaml
ports:
  - "5173:5173"
```

Mapeia a porta usada pelo Vite.

Neste caso:

```text
localhost:5173 -> container:5173
```

Com isso, o frontend pode ser acessado em:

```text
http://localhost:5173
```

---

### `volumes`

```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules
```

O primeiro volume monta a pasta local `./frontend` dentro do container no caminho `/app`.

Isso permite que alterações feitas no código do frontend sejam refletidas no container.

O segundo volume:

```yaml
- /app/node_modules
```

preserva a pasta `node_modules` dentro do container.

Essa configuração evita conflitos entre as dependências instaladas no container e a pasta local do desenvolvedor.

---

### `depends_on`

```yaml
depends_on:
  - backend
```

Define que o frontend depende do backend.

Isso organiza a ordem de inicialização dos serviços, fazendo com que o backend seja iniciado antes do frontend.

---

### `command`

```yaml
command: npm run dev -- --host
```

Executa o servidor de desenvolvimento do frontend.

Esse comando inicia o Vite em modo de desenvolvimento e permite acesso ao serviço fora do container.

Uma alternativa mais explícita seria:

```yaml
command: npm run dev -- --host 0.0.0.0
```

---

## Volume `postgres_data`

```yaml
volumes:
  postgres_data:
```

Define o volume persistente usado pelo banco PostgreSQL.

Esse volume armazena os dados do banco fora do ciclo de vida do container.

Assim, mesmo que o container do banco seja removido e recriado, os dados podem ser mantidos.

---

## Comunicação entre os serviços

Dentro da rede criada automaticamente pelo Docker Compose, os containers conseguem se comunicar usando o nome do serviço.

Por isso, o backend deve acessar o banco usando o host:

```text
db
```

Exemplo de `DATABASE_URL`:

```env
DATABASE_URL=postgresql://usuario:senha@db:5432/nome_do_banco
```

Não deve ser usado `localhost` para conectar o backend ao banco dentro do Docker, pois `localhost` dentro do container do backend aponta para o próprio container do backend.

---

## Portas utilizadas

| Serviço    | Porta local | Porta interna | URL local               |
| ---------- | ----------: | ------------: | ----------------------- |
| PostgreSQL |        5432 |          5432 | `localhost:5432`        |
| Backend    |        8000 |          8000 | `http://localhost:8000` |
| Frontend   |        5173 |          5173 | `http://localhost:5173` |

---

## Arquivo `.env`

O arquivo `.env` deve conter as variáveis necessárias para configurar o banco e o backend.

Exemplo:

```env
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=protectkids_db
DATABASE_URL=postgresql://usuario:senha@db:5432/protectkids_db
```

O arquivo `.env` não deve ser versionado no GitHub.

Para isso, ele deve estar listado no `.gitignore`.

O repositório deve manter apenas um arquivo `.env.example`, sem credenciais reais.

---

## Como executar o ambiente

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando constrói as imagens locais e inicia os containers.

Para parar os containers:

```bash
docker compose down
```

Para parar os containers e remover o volume do banco:

```bash
docker compose down -v
```

Atenção: o comando `docker compose down -v` remove o volume `postgres_data` e apaga os dados locais do banco.

---

## Como verificar os containers

```bash
docker ps
```

Para visualizar os logs:

```bash
docker compose logs
```

Logs específicos do backend:

```bash
docker compose logs backend
```

Logs específicos do banco:

```bash
docker compose logs db
```

Logs específicos do frontend:

```bash
docker compose logs frontend
```

---

## Resumo da configuração

| Serviço    | Função           | Tecnologia        | Porta |
| ---------- | ---------------- | ----------------- | ----- |
| `db`       | Banco de dados   | PostgreSQL 15     | 5432  |
| `backend`  | API da aplicação | FastAPI + Uvicorn | 8000  |
| `frontend` | Interface web    | React + Vite      | 5173  |

---

## Observações importantes

* O backend utiliza build local para facilitar o desenvolvimento.
* A imagem do GHCR permanece comentada como alternativa futura.
* O banco possui `healthcheck` para evitar falhas de conexão no início da aplicação.
* O backend só inicia após o banco estar saudável.
* O frontend depende do backend para organizar a ordem de inicialização.
* As variáveis sensíveis devem ficar no `.env`.
* O arquivo `.env.example` deve ser mantido atualizado no repositório.
