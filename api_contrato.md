# Contrato da API — ProtectKids

Este documento define o contrato de integração entre o backend FastAPI e o frontend React/Vite do projeto **ProtectKids**.

## URL Base

Ambiente local:

```text
http://localhost:8000
```

Configuração recomendada no frontend:

```env
VITE_API_URL=http://localhost:8000
```

```javascript
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});
```

---

# 1. Status da API

## `GET /`

Verifica se a API está ativa.

### Resposta 200

```json
{
  "message": "API ProtectKids está no ar!"
}
```

---

# 2. Listar proposições

## `GET /proposicoes`

Retorna uma lista paginada e resumida de proposições.

Esta rota deve ser usada para listagens, cards, tabelas e dashboards. Ela **não retorna `texto_integral`**.

## Parâmetros

| Parâmetro  | Tipo    | Obrigatório | Descrição                                                    |
| ---------- | ------- | ----------- | ------------------------------------------------------------ |
| `uf`       | string  | Não         | Filtra pela UF do autor. Exemplo: `DF`.                      |
| `partido`  | string  | Não         | Filtra pelo partido do autor. Exemplo: `PT`.                 |
| `ano`      | integer | Não         | Filtra pelo ano da proposição.                               |
| `tema_nlp` | string  | Não         | Filtra pela classificação temática.                          |
| `origem`   | string  | Não         | Valores aceitos: `Camara` ou `Senado`.                       |
| `limit`    | integer | Não         | Quantidade de itens retornados. Padrão: `50`. Máximo: `200`. |
| `offset`   | integer | Não         | Quantidade de itens ignorados. Padrão: `0`.                  |

## Exemplo

```http
GET /proposicoes?origem=Camara&limit=10&offset=0
```

## Resposta 200

```json
[
  {
    "id_proposicao": 3,
    "id_externo": "camara-2634854",
    "titulo": "PL 3270/2026",
    "origem": "Camara",
    "tipo": "PL",
    "numero": 3270,
    "ano": 2026,
    "ementa": "Institui a Política Nacional de Infraestrutura Familiar e Acessível nas Praias Brasileiras...",
    "tema": "Protecao Infantil",
    "subtema": "criança",
    "classificacao_nlp": "Proteção Geral",
    "data_apresentacao": "2026-06-23",
    "url_inteiro_teor": "https://www.camara.leg.br/...",
    "id_autor": 220540,
    "nome_autor": "Duda Ramos",
    "partido_autor": "PODE",
    "uf_autor": "RR"
  }
]
```

## Erro 400 — origem inválida

```json
{
  "detail": "Origem inválida. Use 'Camara' ou 'Senado'."
}
```

---

# 3. Detalhar proposição

## `GET /proposicoes/{id_busca}`

Retorna os dados completos de uma proposição.

O parâmetro `id_busca` aceita:

| Formato              | Exemplo          |
| -------------------- | ---------------- |
| ID interno           | `3`              |
| ID externo da Câmara | `camara-2634854` |
| ID externo do Senado | `senado-123456`  |

## Exemplo

```http
GET /proposicoes/camara-2634854
```

## Resposta 200

```json
{
  "id_proposicao": 3,
  "id_externo": "camara-2634854",
  "titulo": "PL 3270/2026",
  "origem": "Camara",
  "tipo": "PL",
  "numero": 3270,
  "ano": 2026,
  "ementa": "Institui a Política Nacional de Infraestrutura Familiar e Acessível nas Praias Brasileiras...",
  "tema": "Protecao Infantil",
  "subtema": "criança",
  "classificacao_nlp": "Proteção Geral",
  "data_apresentacao": "2026-06-23",
  "url_inteiro_teor": "https://www.camara.leg.br/...",
  "id_autor": 220540,
  "nome_autor": "Duda Ramos",
  "partido_autor": "PODE",
  "uf_autor": "RR",
  "texto_integral": "Texto integral extraído do PDF..."
}
```

## Erro 404

```json
{
  "detail": "Proposição com ID camara-999999999 não foi encontrada no banco de dados."
}
```

---

# 4. Tramitações

## `GET /proposicoes/{id_externo}/tramitacoes`

Retorna o histórico de tramitações de uma proposição.

## Exemplo

```http
GET /proposicoes/camara-2634854/tramitacoes
```

## Resposta 200

```json
[
  {
    "data_hora": "2026-06-23T15:10:00",
    "orgao": "MESA",
    "descricao": "Apresentação de Proposição"
  }
]
```

Observação: nesta versão, as tramitações estão mais consolidadas para proposições da Câmara.

---

# 5. Ranking de parlamentares

## `GET /analytics/parlamentares/ranking`

Retorna o ranking de parlamentares por quantidade de proposições cadastradas.

## Parâmetros

| Parâmetro  | Tipo    | Obrigatório | Descrição                                                    |
| ---------- | ------- | ----------- | ------------------------------------------------------------ |
| `ano`      | integer | Não         | Filtra pelo ano da proposição.                               |
| `tema_nlp` | string  | Não         | Filtra pela classificação temática.                          |
| `origem`   | string  | Não         | Valores aceitos: `Camara` ou `Senado`.                       |
| `uf`       | string  | Não         | Filtra pela UF do autor. Exemplo: `DF`.                      |
| `partido`  | string  | Não         | Filtra pelo partido do autor. Exemplo: `PT`.                 |
| `limit`    | integer | Não         | Quantidade de itens retornados. Padrão: `10`. Máximo: `100`. |

## Exemplos

```http
GET /analytics/parlamentares/ranking
```

```http
GET /analytics/parlamentares/ranking?origem=Camara&limit=5
```

```http
GET /analytics/parlamentares/ranking?ano=2026&tema_nlp=Proteção Geral&limit=10
```

## Resposta 200

```json
[
  {
    "nome": "Duda Ramos",
    "partido": "PODE",
    "uf": "RR",
    "total_proposicoes": 3
  }
]
```

---

# 6. Ranking de partidos

## `GET /analytics/partidos/ranking`

Retorna o ranking de partidos por quantidade de proposições cadastradas.

## Parâmetros

| Parâmetro  | Tipo    | Obrigatório | Descrição                                                    |
| ---------- | ------- | ----------- | ------------------------------------------------------------ |
| `ano`      | integer | Não         | Filtra pelo ano da proposição.                               |
| `tema_nlp` | string  | Não         | Filtra pela classificação temática.                          |
| `origem`   | string  | Não         | Valores aceitos: `Camara` ou `Senado`.                       |
| `uf`       | string  | Não         | Filtra pela UF do autor. Exemplo: `DF`.                      |
| `partido`  | string  | Não         | Filtra pelo partido do autor. Exemplo: `PT`.                 |
| `limit`    | integer | Não         | Quantidade de itens retornados. Padrão: `10`. Máximo: `100`. |

## Exemplos

```http
GET /analytics/partidos/ranking
```

```http
GET /analytics/partidos/ranking?origem=Senado&limit=5
```

```http
GET /analytics/partidos/ranking?ano=2026&uf=DF&limit=10
```

## Resposta 200

```json
[
  {
    "partido": "PODE",
    "total_proposicoes": 5
  }
]
```

---

# 7. Nuvem de palavras

## `GET /analytics/nuvem-palavras`

Retorna as palavras mais frequentes nas ementas das proposições cadastradas.

Esta rota deve ser usada na **tela inicial do projeto**, conforme requisito solicitado para exibição da nuvem de palavras.

A nuvem de palavras é gerada a partir das **ementas** das proposições, não do texto integral dos PDFs.

## Parâmetros

| Parâmetro  | Tipo    | Obrigatório | Descrição                                                       |
| ---------- | ------- | ----------- | --------------------------------------------------------------- |
| `ano`      | integer | Não         | Filtra pelo ano da proposição.                                  |
| `tema_nlp` | string  | Não         | Filtra pela classificação temática.                             |
| `origem`   | string  | Não         | Valores aceitos: `Camara` ou `Senado`.                          |
| `uf`       | string  | Não         | Filtra pela UF do autor. Exemplo: `DF`.                         |
| `partido`  | string  | Não         | Filtra pelo partido do autor. Exemplo: `PT`.                    |
| `limit`    | integer | Não         | Quantidade de palavras retornadas. Padrão: `50`. Máximo: `100`. |

## Exemplos

```http
GET /analytics/nuvem-palavras
```

```http
GET /analytics/nuvem-palavras?limit=50
```

```http
GET /analytics/nuvem-palavras?origem=Camara&limit=30
```

```http
GET /analytics/nuvem-palavras?origem=Senado&limit=30
```

```http
GET /analytics/nuvem-palavras?ano=2026&tema_nlp=Proteção Geral&limit=30
```

## Resposta 200

```json
[
  {
    "text": "criança",
    "value": 18
  },
  {
    "text": "adolescente",
    "value": 14
  },
  {
    "text": "proteção",
    "value": 10
  }
]
```

## Tipo esperado no frontend

```typescript
type PalavraNuvem = {
  text: string;
  value: number;
};
```

---

# 8. Taxonomia temática

O campo `classificacao_nlp` pode retornar:

```text
Cyberbullying e Crimes Virtuais
Adoção e Orfanatos
Violência e Abuso
Educação e Cultura
Proteção Geral
Simbólico/Ruído
Articulação Estratégica
```

O campo `tema` usa o valor padrão:

```text
Protecao Infantil
```

A classificação usa processamento de linguagem natural com spaCy e regras heurísticas.

---

# 9. Funções recomendadas no frontend

## Buscar proposições

```javascript
export async function buscarProposicoes(params = {}) {
  const { data } = await api.get("/proposicoes", { params });
  return data;
}
```

Exemplo:

```javascript
const proposicoes = await buscarProposicoes({
  origem: "Camara",
  limit: 10,
  offset: 0,
});
```

## Buscar detalhe

```javascript
export async function buscarProposicaoPorId(idBusca) {
  const { data } = await api.get(`/proposicoes/${idBusca}`);
  return data;
}
```

## Buscar tramitações

```javascript
export async function buscarTramitacoes(idExterno) {
  const { data } = await api.get(`/proposicoes/${idExterno}/tramitacoes`);
  return data;
}
```

## Buscar nuvem de palavras

```javascript
export async function buscarNuvemPalavras(params = {}) {
  const { data } = await api.get("/analytics/nuvem-palavras", { params });
  return data;
}
```

Exemplo de uso na Home:

```javascript
const palavras = await buscarNuvemPalavras({
  origem: "Camara",
  limit: 50,
});
```

## Buscar ranking de parlamentares

```javascript
export async function buscarRankingParlamentares(params = {}) {
  const { data } = await api.get("/analytics/parlamentares/ranking", { params });
  return data;
}
```

## Buscar ranking de partidos

```javascript
export async function buscarRankingPartidos(params = {}) {
  const { data } = await api.get("/analytics/partidos/ranking", { params });
  return data;
}
```

Exemplo:

```javascript
const rankingPartidos = await buscarRankingPartidos({
  origem: "Senado",
  limit: 5,
});
```

---

# 10. Orientações para o frontend

A tela inicial deve consumir:

```http
GET /analytics/nuvem-palavras
```

Também é possível criar abas ou filtros na Home usando:

```http
GET /analytics/nuvem-palavras?origem=Camara
GET /analytics/nuvem-palavras?origem=Senado
```

A tela de listagem deve consumir:

```http
GET /proposicoes
```

A tela de detalhes deve consumir:

```http
GET /proposicoes/{id_busca}
GET /proposicoes/{id_externo}/tramitacoes
```

A listagem não possui `texto_integral`. O texto completo só aparece na rota de detalhe.

Os endpoints de analytics aceitam filtros para permitir dashboards dinâmicos por origem, ano, tema, UF e partido.
