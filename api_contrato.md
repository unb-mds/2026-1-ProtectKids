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