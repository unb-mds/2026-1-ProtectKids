# 📊 Visão Geral

## Objetivo

Desenvolver uma plataforma para monitorar, classificar e analisar proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital.

---

## Escopo

O sistema irá:

* Coletar dados da API de Dados Abertos da Câmara dos Deputados
* Extrair o inteiro teor das proposições
* Classificar por subtema
* Apresentar visualizações analíticas em um dashboard interativo

---

## Temas Principais

* Cyberbullying
* Proteção de dados de menores
* Exploração sexual online
* Controle parental
* Regulação de plataformas digitais
* Exposição a conteúdo nocivo

---

# 👤 Personas

## Persona Principal: Articuladora de ONG

* Atua na defesa dos direitos de crianças e adolescentes
* Precisa monitorar projetos de lei
* Busca identificar ameaças ou oportunidades legislativas
* Necessita identificar parlamentares aliados

---

# User Stories

## US01 – Descoberta pelo Inteiro Teor

**Como** articuladora de ONG
**Quero** que o sistema classifique as leis lendo o texto completo
**Para que** eu consiga identificar ameaças mesmo quando não estão explícitas na ementa

### ✔ Critérios de Aceitação

* O sistema deve analisar o inteiro teor
* Deve classificar mesmo sem menção na ementa
* Deve exibir o resultado no dashboard

---

## US02 – Mapeamento de Aliados

**Como** articuladora de ONG
**Quero** visualizar ranking de deputados e partidos
**Para** saber com quem agendar reuniões

### ✔ Critérios de Aceitação

* Permitir seleção por subtema
* Ordenar parlamentares por número de proposições
* Mostrar partidos mais ativos

---

## US03 – Análise Temporal

**Como** articuladora de ONG
**Quero** visualizar evolução temporal das proposições
**Para** identificar tendências

### ✔ Critérios de Aceitação

* Apresentar gráfico por ano
* Permitir filtro por subtema
* Mostrar crescimento ou queda

---

# Requisitos Funcionais

## Must Have

* **RF01**: Extrair metadados da API
* **RF02**: Obter link do inteiro teor
* **RF03**: Extrair texto completo (PDF/TXT)
* **RF04**: Classificar por subtema usando NLP
* **RF05**: Exibir dashboard com volume por subtema
* **RF06**: Ranking de parlamentares
* **RF07**: Ranking de partidos

---

## Should Have

* **RF08**: Gráfico de evolução temporal
* **RF09**: Filtro por subtema

---

## Could Have

* **RF10**: Identificação automática de novos temas

---

## Won't Have (MVP)

* **RF11**: Integração com API do Senado

---

# Requisitos Não Funcionais

## Desempenho e Performance

* **RNF01**: A API do backend (FastAPI) deve responder às consultas de listagem e filtragem do Dashboard em menos de 1.5 segundos, garantindo uma navegação fluida.

* **RNF02**: O script de extração (Crawler) deve processar e salvar cada lote de dados em segundo plano, sem bloquear ou degradar a performance das requisições simultâneas feitas pelos usuários no Frontend.

## Portabilidade e Infraestrutura

* **RNF03**: O sistema deve ser totalmente conteinerizado utilizando Docker e Docker Compose, garantindo que o ambiente de execução seja idêntico em qualquer máquina (Desenvolvimento, Teste ou Produção) executando com um único comando (docker-compose up).

## Resiliência e Tolerância a Falhas

* **RNF04**: O motor de extração de dados deve possuir tratamento de erros para cenários onde a API de Dados Abertos da Câmara estiver fora do ar ou aplicar limite de requisições (Rate Limiting), registrando a falha nos logs sem derrubar o backend.

## Qualidade e Manutenibilidade

* **RNF05**: O código fonte deve obrigatoriamente passar por verificações automatizadas de formatação (Linters como Ruff/ESLint) e execução de testes unitários através de uma pipeline de Integração Contínua (GitHub Actions) a cada Pull Request.

## Usabilidade

* **RNF06**: A interface do usuário (React) deve ser responsiva, garantindo a legibilidade dos textos legislativos e a correta exibição dos gráficos em resoluções desktop (telas grandes) e dispositivos móveis.

---

# Critérios de Aceitação (Gherkin)

## Cenário: Classificação pelo inteiro teor

**Dado que** uma proposição não cita o tema na ementa
**Quando** o sistema analisa o texto completo
**Então** ela deve ser classificada corretamente

---

## Cenário: Visualização de ranking

**Dado que** estou no dashboard
**Quando** seleciono o subtema "Cyberbullying"
**Então** o sistema deve mostrar deputados ordenados

---

## Cenário: Análise temporal

**Dado que** estou no dashboard
**Quando** seleciono um subtema
**Então** devo visualizar a evolução ao longo do tempo

---

# Arquitetura

## Pipeline de Dados

1. Extração via API (Câmara/Senado)
2. Download do inteiro teor
3. Processamento com NLP
4. Classificação por temas e subtemas
5. Armazenamento estruturado

---

## Camada de Visualização

* Dashboard interativo
* Gráficos por subtema
* Rankings de parlamentares
* Filtros por período, tema e deputado

---

## Princípios Arquiteturais

* Separação entre processamento e visualização
* Melhor desempenho e escalabilidade
* Facilidade de manutenção

---

# MVP (Produto Mínimo Viável)

## Integração com API

* Extração de dados
* Download do inteiro teor
* Processamento com NLP
* Armazenamento

---

## Dashboard

* Dados disponíveis
* Classificação por subtema
* Visualização por volume
* Ranking de parlamentares

---

## Critério Geral

O sistema deve permitir análise básica de proposições legislativas com base em temas e subtemas, apresentando os dados de forma clara no dashboard.

---

# 📌 Versionamento

| Versão | Data | Descrição |
| ------ | ---- | --------- |
|    1.0    |   11/04/2026   |      Versão inicial do documento     |
|    1.1    |   03/05/2026   |      Ajustes estruturais e refinamento dos requisitos     |
|    1.2    |   18/05/2026   |     Reinserção da seção de Requisitos Não Funcionais      |
