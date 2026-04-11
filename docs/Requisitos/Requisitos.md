## Controle de Versões

| Autor(a)        | Detalhamento                                            | Versão | Data       |
| --------------- | ------------------------------------------------------- | ------ | ---------- |
| Danielly Mendes | Criação do documento e coleta de requisitos  funcionais | 1.0    | 10/04/2026 |

## 1. Visão Geral

### Objetivo

Desenvolver uma plataforma para monitorar, classificar e analisar proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital.

### Escopo

O sistema irá coletar dados da API de Dados Abertos da Câmara dos Deputados, extrair o inteiro teor das proposições, classificá-las por subtema e apresentar visualizações analíticas em um dashboard interativo.

### Temas Principais

- Cyberbullying
    
- Proteção de dados de menores
    
- Exploração sexual online
    
- Controle parental
    
- Regulação de plataformas digitais
    
- Exposição a conteúdo nocivo
    

---

## 2. Personas

### Persona Principal

**Articuladora de ONG**

- Atua na defesa dos direitos de crianças e adolescentes
    
- Precisa monitorar projetos de lei
    
- Busca identificar ameaças ou oportunidades legislativas
    
- Necessita identificar parlamentares aliados
    

---

## 3. User Stories

### US01 – Descoberta pelo Inteiro Teor

Como articuladora de ONG, quero que o sistema classifique as leis lendo o texto completo delas, para que eu consiga identificar ameaças à segurança digital de menores mesmo quando não estão explícitas na ementa.

Critérios de Aceitação:

- O sistema deve analisar o inteiro teor do documento
    
- Deve classificar mesmo quando o tema não aparece na ementa
    
- Deve exibir o resultado no dashboard
    

---

### US02 – Mapeamento de Aliados

Como articuladora de ONG, quero visualizar um ranking dos deputados e partidos com mais proposições sobre proteção infantil online, para saber com quem devo agendar reuniões.

Critérios de Aceitação:

- Deve permitir seleção por subtema
    
- Deve ordenar parlamentares por número de proposições
    
- Deve permitir visualizar partidos mais ativos
    

---

### US03 – Análise Temporal

Como articuladora de ONG, quero visualizar a evolução temporal das proposições por tema, para identificar tendências e novos assuntos emergentes.

Critérios de Aceitação:

- Deve apresentar gráfico por ano
    
- Deve permitir filtrar por subtema
    
- Deve mostrar crescimento ou queda de propostas
    

---

## 4. Requisitos Funcionais (RF)

| ID   | Descrição                 | Prioridade  |
| ---- | ------------------------- | ----------- |
| RF01 | Extrair metadados da API  | Must Have   |
| RF02 | Extrair inteiro teor      | Must Have   |
| RF03 | Classificar por subtema   | Must Have   |
| RF04 | Exibir dashboard          | Must Have   |
| RF05 | Ranking de parlamentares  | Must Have   |
| RF06 | Gráfico temporal          | Should Have |
| RF07 | Descoberta de novos temas | Could Have  |

### Must Have

RF01: O sistema deve extrair diariamente os metadados das proposições legislativas pela API da Câmara.

RF02: O sistema deve obter o link do inteiro teor das proposições.

RF03: O sistema deve extrair o texto completo das proposições (PDF/TXT).

RF04: O sistema deve classificar as proposições por subtema utilizando palavras-chave e NLP.

RF05: O sistema deve exibir um dashboard com o volume de proposições por subtema.

RF06: O sistema deve apresentar ranking de parlamentares mais ativos.

RF07: O sistema deve apresentar ranking de partidos mais ativos.

### Should Have

RF08: O sistema deve exibir gráfico de evolução temporal das proposições.

RF09: O sistema deve permitir filtro por subtema.

### Could Have

RF10: O sistema deve identificar automaticamente novos temas emergentes.

### Won't Have (MVP)

RF11: O sistema não terá integração com a API do Senado nesta versão.
