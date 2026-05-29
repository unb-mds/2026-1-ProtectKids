# 📊 Visão Geral

## Objetivo

Desenvolver uma plataforma para monitorar, classificar e analisar proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital. A plataforma permitirá que diferentes perfis de usuários — desde ativistas de ONG até jornalistas de dados e assessores parlamentares — acompanhem o avanço do debate legislativo com profundidade e agilidade, reduzindo o tempo gasto em pesquisa manual e ampliando a capacidade analítica de cada perfil.

---

## Escopo

O sistema coletará dados da API de Dados Abertos da Câmara dos Deputados, extrairá o inteiro teor das proposições e as classificará por subtema utilizando processamento de linguagem natural (NLP). Os resultados serão apresentados em um dashboard interativo que combina visualizações analíticas, rankings de parlamentares e partidos, e filtros por período e tema.

---

## Temas Principais

Os temas monitorados pela plataforma compreendem as principais dimensões da proteção de crianças e adolescentes no ambiente digital:

- **Cyberbullying:** proposições que tratam de assédio, perseguição ou humilhação de menores em ambientes virtuais.
- **Proteção de dados de menores:** regulações sobre coleta, armazenamento e uso de dados pessoais de crianças e adolescentes por plataformas digitais.
- **Exploração sexual online:** projetos que buscam combater a distribuição de conteúdo abusivo, aliciamento e outras formas de violência sexual mediadas por tecnologia.
- **Controle parental:** mecanismos legais ou técnicos que habilitam pais e responsáveis a monitorar ou restringir o acesso de menores a conteúdos digitais.
- **Regulação de plataformas digitais:** obrigações impostas a redes sociais, aplicativos e outros serviços quanto à proteção de usuários menores de idade.
- **Exposição a conteúdo nocivo:** iniciativas legislativas que visam limitar ou sinalizar conteúdos violentos, de ódio ou inadequados para o público infanto-juvenil.

---

# 👤 Personas

## Persona 1 — Joana, Coordenadora de Políticas Públicas em ONG

**Perfil:** Joana tem 38 anos e atua como coordenadora de políticas públicas em uma organização não governamental dedicada à proteção dos direitos da criança e do adolescente, como o Instituto Alana ou a SaferNet. Com formação em direito ou ciências sociais, ela transita entre o universo do ativismo e o da incidência política, participando de audiências públicas, redigindo notas técnicas e construindo alianças com parlamentares sensíveis à sua pauta.

**Objetivos:** Joana precisa mapear continuamente quais deputados e senadores são aliados ou adversários nas pautas de regulação de plataformas digitais e proteção de menores contra exploração online. Seu principal interesse é saber com quem a ONG deve agendar reuniões, quais projetos representam ameaças aos direitos já conquistados e quais abrem oportunidades de avanço legislativo.

**Dores atuais:** Ela perde horas toda semana pesquisando manualmente nos portais da Câmara e do Senado. Um problema frequente é que a ementa — o resumo oficial do projeto de lei — muitas vezes não menciona diretamente o tema de interesse, embora o texto completo contenha alterações relevantes à proteção de menores. Sem um sistema que analise o inteiro teor, essas proposições passam despercebidas até que seja tarde para agir.

**Como a plataforma a ajuda:** O painel de parlamentares e partidos mais ativos permite que Joana crie listas de contatos segmentadas por subtema para ações de *lobby* positivo. A classificação por NLP sobre o texto completo poupa o tempo de leitura e garante que nenhuma proposição relevante passe despercebida, mesmo quando a ementa é vaga ou genérica.

---

## Persona 2 — Roberto, Repórter de Tecnologia e Sociedade

**Perfil:** Roberto tem 28 anos e trabalha como repórter de tecnologia e sociedade em um grande portal de notícias. Sua especialidade são reportagens investigativas baseadas em dados, e ele está sempre em busca de histórias que revelem padrões invisíveis ao olhar cotidiano. Ele tem familiaridade com ferramentas de análise de dados, mas não é programador — prefere interfaces que traduzam dados complexos em visualizações acessíveis.

**Objetivos:** Roberto quer escrever reportagens que mostrem, com evidências concretas, como o Brasil está — ou não está — acompanhando os novos riscos digitais para crianças. Ele precisa identificar tendências emergentes, como o surgimento repentino de projetos sobre inteligência artificial e menores, e construir narrativas com profundidade histórica e comparativa.

**Dores atuais:** É muito difícil enxergar a "figura maior" ou a linha do tempo do debate legislativo a partir das ferramentas oficiais do Congresso. Quando um tema explode nas notícias, Roberto não consegue saber rapidamente se os parlamentares já estavam discutindo o assunto ou se estão completamente atrasados. A ausência de séries temporais dificulta a construção de narrativas baseadas em evidências.

**Como a plataforma o ajuda:** O indicador de evolução temporal por subtema dá a Roberto a manchete pronta: *"Projetos de lei sobre IA e menores crescem 300% em um ano"*. O recurso de identificação de novos temas emergentes complementa essa capacidade analítica, permitindo que ele detecte movimentos legislativos incipientes antes de virarem pauta dominante.

---

## Persona 3 — Camila, Assessora Legislativa

**Perfil:** Camila tem 40 anos e atua como consultora ou assessora legislativa no gabinete de um mandato focado em educação ou tecnologia. Com experiência em redação de projetos de lei, análise de jurisprudência e elaboração de discursos, ela é a ponte entre o deputado ou senador e o universo técnico-jurídico das proposições em tramitação.

**Objetivos:** Camila precisa municiar seu parlamentar com informações precisas, atualizadas e bem contextualizadas para que ele proponha leis inovadoras, evite redundâncias e faça discursos embasados na tribuna. Ela também precisa monitorar o histórico legislativo sobre cada tema para antecipar eventuais objeções durante a votação.

**Dores atuais:** O excesso de informação desorganizada é seu principal inimigo. Quando o deputado pede que ela redija um projeto sobre cyberbullying, ela teme escrever algo que já foi proposto e rejeitado anos atrás — o que expõe o mandato a críticas e retrabalho. A ausência de um repositório estruturado e pesquisável sobre proposições por subtema torna esse risco constante.

**Como a plataforma a ajuda:** O filtro ágil por subtema permite que Camila faça uma auditoria rápida de tudo que já foi apresentado no Congresso sobre controle parental, segurança digital ou proteção de dados de menores. Com isso, ela identifica lacunas legislativas reais e apresenta ao seu parlamentar uma proposta verdadeiramente original e bem fundamentada.

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
