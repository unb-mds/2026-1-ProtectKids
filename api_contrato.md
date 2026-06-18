# 📄 Contrato de Integração da API - ProtectKids (Backend -> Frontend)

**Base URL Local:** `http://localhost:8000`  
**Documentação Interativa (Swagger):** `http://localhost:8000/docs`

O backend expõe 6 rotas principais, divididas entre dados transacionais (busca de leis) e rotas analíticas (dashboards). Todos os endpoints retornam dados no formato `JSON`.

---

### 1. Buscar Todas as Proposições (Com Filtros)
Retorna a lista de projetos de lei, ideal para a tela de "Busca Avançada" ou "Auditoria".

* **Endpoint:** `GET /proposicoes`
* **Query Parameters (Opcionais):**
  * `uf` (string): Ex: `SP`, `RJ`.
  * `partido` (string): Ex: `PL`, `PT`, `PSOL`.
  * `ano` (int): Ex: `2026`.
  * `tema_nlp` (string): Ex: `Cyberbullying`, `Exploração sexual online`.
* **Exemplo de Chamada:** `/proposicoes?ano=2026&tema_nlp=Cyberbullying`
* **Resposta Esperada (200 OK):**
```json
[
  {
    "id_proposicao": 1,
    "id_externo": "24792026",
    "titulo": "PL 2479/2026",
    "ementa": "Altera o ECA para criminalizar...",
    "ano": 2026,
    "classificacao_nlp": "Cyberbullying",
    "origem": "Camara",
    "nome_autor": "João Silva"
  }
]
```

---

### 2. Buscar Detalhes de uma Lei
Retorna os dados completos de uma única lei.

* **Endpoint:** `GET /proposicoes/{id_busca}`
* **Path Parameter:**
  * `id_busca` (int ou string): Pode ser o ID do banco ou o `id_externo` oficial da Câmara/Senado.
* **Resposta Esperada (200 OK):** Objeto JSON único contendo os detalhes da proposição.

---

### 3. Linha do Tempo (Histórico de Tramitações)
Alimenta o componente visual de "Status/Passo a Passo" de uma lei específica. Já vem ordenado da tramitação mais recente (topo) para a mais antiga.

* **Endpoint:** `GET /proposicoes/{id_externo}/tramitacoes`
* **Path Parameter:**
  * `id_externo` (string): Obrigatório. O ID oficial da lei.
* **Resposta Esperada (200 OK):**
```json
[
  {
    "data_hora": "2026-05-18T14:30:00",
    "orgao": "Mesa Diretora",
    "descricao": "Apresentação do Projeto de Lei..."
  }
]
```

---

### 4. Dashboard: Ranking de Parlamentares
Retorna os deputados/senadores que mais propõem leis sobre proteção infantil.

* **Endpoint:** `GET /analytics/parlamentares/ranking`
* **Query Parameters (Opcionais):** `ano`, `tema_nlp`.
* **Resposta Esperada (200 OK):**
```json
[
  {
    "nome": "João Silva",
    "partido": "PL",
    "uf": "SP",
    "total_projetos": 15
  }
]
```

---

### 5. Dashboard: Ranking de Partidos
Retorna o volume agregado de leis propostas por cada partido.

* **Endpoint:** `GET /analytics/partidos/ranking`
* **Query Parameters (Opcionais):** `ano`, `tema_nlp`.
* **Resposta Esperada (200 OK):**
```json
[
  {
    "partido": "PL",
    "total_projetos": 45
  },
  {
    "partido": "PT",
    "total_projetos": 38
  }
]
```

---

### 6. Dashboard: Nuvem de Palavras
Analisa os textos das leis (NLP) e devolve as palavras centrais para a biblioteca de Word Cloud da página inicial, já sem pontuações ou jargões legislativos ("lei", "artigo", meses do ano, etc).

* **Endpoint:** `GET /analytics/nuvem-palavras`
* **Query Parameters (Opcionais):** `ano`, `tema_nlp`.
* **Resposta Esperada (200 OK):**
```json
[
  {
    "text": "criança",
    "value": 150
  },
  {
    "text": "internet",
    "value": 95
  }
]
```

---

## ⚠️ Anexos de Integração (Dicionários e Erros)

Para garantir que os filtros do frontend funcionem perfeitamente com o banco de dados e que as telas de erro sejam amigáveis, a equipe de React deve observar os seguintes padrões:

### A. Dicionário de Domínio (Valores Exatos para Filtros)
Ao montar os componentes de `Select` ou `Dropdown` para os filtros, os valores enviados na URL (`Query Parameters`) devem ser **exatamente** iguais a estas strings (Case Sensitive), caso contrário, a API retornará uma lista vazia.

* **origem:** `Camara` ou `Senado` *(Sem acentos)*
* **tema_nlp:** 
  * `Cyberbullying`
  * `Proteção de dados de menores`
  * `Exploração sexual online`
  * `Controle parental`
  * `Regulação de plataformas digitais`
  * `Exposição a conteúdo nocivo`

### B. Contrato de Exceções (Tratamento de Erros)
Quando uma requisição falha (ex: buscar os detalhes de um ID que não existe no banco de dados), o backend não devolve HTML ou texto solto. Ele devolve o status HTTP correspondente (ex: `404 Not Found`) e um JSON padronizado com a chave `detail`. 

O frontend deve capturar essa chave para exibir "Toasts" ou Alertas ao usuário.

* **Exemplo de Resposta de Erro (404 ou 500):**
```json
{
  "detail": "Proposição com ID 12345 não foi encontrada no banco de dados."
}
```
*(No Axios, isso seria acessado via `error.response.data.detail`)*

### C. Configuração de Variáveis de Ambiente (Vite/React)
O backend já está com o CORS configurado para aceitar requisições locais das portas `3000` e `5173`. Para que o frontend saiba com quem falar sem deixar a URL chumbada no código, criem um arquivo `.env` na raiz do projeto React com a seguinte variável:

```env
VITE_API_URL=http://localhost:8000
```
*(Todas as chamadas do Axios/Fetch devem usar essa base URL).*