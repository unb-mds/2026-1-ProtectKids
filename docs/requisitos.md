# Visão Geral

## Objetivo

Desenvolver uma plataforma para monitorar, classificar e analisar proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital. A plataforma permitirá que diferentes perfis de usuários — desde ativistas de ONG até jornalistas de dados e assessores parlamentares — acompanhem o avanço do debate legislativo com profundidade e agilidade, reduzindo o tempo gasto em pesquisa manual e ampliando a capacidade analítica de cada perfil.

---

## Escopo

O sistema coletará dados da API de Dados Abertos da Câmara dos Deputados e do Senado Federal, extrairá o inteiro teor das proposições e as classificará por subtema utilizando processamento de linguagem natural (NLP). Os resultados serão apresentados em um painel interativo que combina visualizações analíticas, rankings de parlamentares e partidos, e filtros por período e tema.

---

## Temas Principais

Os temas monitorados pela plataforma compreendem as principais dimensões da proteção de crianças e adolescentes no ambiente digital:

- **Cyberbullying e Crimes Virtuais:** proposições que tratam de assédio, perseguição ou humilhação de menores em ambientes virtuais.
- **Proteção de Dados e Privacidade Infantil:** regulações sobre a coleta, o armazenamento, o tratamento e o compartilhamento de dados pessoais de crianças e adolescentes, bem como medidas para garantir sua privacidade e segurança no ambiente digital.
- **Redes Sociais e Plataformas Digitais:** projetos que estabelecem deveres, responsabilidades e mecanismos de governança para redes sociais, aplicativos e plataformas digitais, com foco na proteção de crianças e adolescentes durante o uso desses serviços.
- **Educação e Cultura:** proposições voltadas à promoção da educação digital, da cidadania online e da conscientização de crianças, adolescentes, famílias e educadores sobre o uso seguro, ético e responsável das tecnologias e plataformas digitais.
- **Educação Digital e Cidadania Online:** iniciativas que promovem a educação para o uso seguro, ético, crítico e responsável das tecnologias digitais, fortalecendo a cidadania digital de crianças, adolescentes, famílias e educadores.
- **Exploração Sexual Online e Aliciamento Digital:** projetos que buscam prevenir, combater e punir a exploração sexual, o aliciamento, o compartilhamento de material de abuso sexual infantil e outras formas de violência sexual praticadas por meio de tecnologias digitais.

---

# Personas

## Persona 1 — Joana, Coordenadora de Políticas Públicas em ONG

**Perfil:** Joana tem 38 anos e atua como coordenadora de políticas públicas em uma organização não governamental dedicada à proteção dos direitos da criança e do adolescente, como o Instituto Alana ou a SaferNet. Com formação em direito ou ciências sociais, ela transita entre o universo do ativismo e o da incidência política, participando de audiências públicas, redigindo notas técnicas e construindo alianças com parlamentares sensíveis à sua pauta.

**Objetivos:** Joana precisa mapear continuamente quais deputados e senadores são aliados ou adversários nas pautas de regulação de plataformas digitais e proteção de menores contra exploração online. Seu principal interesse é saber com quem a ONG deve agendar reuniões, quais projetos representam ameaças aos direitos já conquistados e quais abrem oportunidades de avanço legislativo.

**Dores atuais:** Ela perde horas toda semana pesquisando manualmente nos portais da Câmara e do Senado. Um problema frequente é que a ementa — o resumo oficial do projeto de lei — muitas vezes não menciona diretamente o tema de interesse, embora o texto completo contenha alterações relevantes à proteção de menores. Sem um sistema que analise o inteiro teor, essas proposições passam despercebidas até que seja tarde para agir.

**Como a plataforma a ajuda:** O painel de parlamentares e partidos mais ativos permite que Joana crie listas de contatos segmentadas por subtema para ações de *lobby* positivo. A classificação por NLP sobre o texto completo poupa o tempo de leitura e garante que nenhuma proposição relevante passe despercebida, mesmo quando a ementa é vaga ou genérica. A plataforma consolida informações da Câmara e do Senado em uma única visão, permitindo análises integradas do Congresso Nacional.

---

## Persona 2 — Roberto, Repórter de Tecnologia e Sociedade

**Perfil:** Roberto tem 28 anos e trabalha como repórter de tecnologia e sociedade em um grande portal de notícias. Sua especialidade são reportagens investigativas baseadas em dados, e ele está sempre em busca de histórias que revelem padrões invisíveis ao olhar cotidiano. Ele tem familiaridade com ferramentas de análise de dados, mas não é programador — prefere interfaces que traduzam dados complexos em visualizações acessíveis.

**Objetivos:** Roberto quer escrever reportagens que mostrem, com evidências concretas, como o Brasil está — ou não está — acompanhando os novos riscos digitais para crianças. Ele precisa identificar quais subtemas recebem maior atenção no Congresso, localizar rapidamente projetos relevantes e compreender como diferentes assuntos estão distribuídos dentro do debate legislativo.

**Dores atuais:** As ferramentas oficiais do Congresso dificultam a obtenção de uma visão consolidada do cenário legislativo. Encontrar projetos relacionados a um tema específico exige consultas demoradas, e comparar a relevância de diferentes subtemas ou identificar áreas pouco discutidas demanda muito trabalho manual.

**Como a plataforma o ajuda:** A classificação automática dos projetos por subtema e as visualizações da distribuição das proposições permitem que Roberto compreenda rapidamente o panorama legislativo. Com filtros e gráficos intuitivos, ele identifica os assuntos mais recorrentes, encontra projetos relacionados ao tema de sua reportagem e obtém evidências para embasar análises e contextualizar suas matérias de forma mais ágil.

---

## Persona 3 — Camila, Assessora Legislativa

**Perfil:** Camila tem 40 anos e atua como consultora ou assessora legislativa no gabinete de um mandato focado em educação ou tecnologia. Com experiência em redação de projetos de lei, análise de jurisprudência e elaboração de discursos, ela é a ponte entre o deputado ou senador e o universo técnico-jurídico das proposições em tramitação.

**Objetivos:** Camila precisa municiar seu parlamentar com informações precisas, atualizadas e bem contextualizadas para que ele proponha leis inovadoras, evite redundâncias e faça discursos embasados na tribuna. Ela também precisa monitorar o histórico legislativo sobre cada tema para antecipar eventuais objeções durante a votação.

**Dores atuais:** O excesso de informação desorganizada é seu principal inimigo. Quando o deputado pede que ela redija um projeto sobre cyberbullying, ela teme escrever algo que já foi proposto e rejeitado anos atrás — o que expõe o mandato a críticas e retrabalho. A ausência de um repositório estruturado e pesquisável sobre proposições por subtema torna esse risco constante.

**Como a plataforma a ajuda:** O filtro ágil por subtema permite que Camila faça uma auditoria rápida de tudo que já foi apresentado no Congresso sobre Proteção de Dados e Privacidade Infantil, segurança digital ou Exploração Sexual Online e Aliciamento Digital. Com isso, ela identifica lacunas legislativas reais e apresenta ao seu parlamentar uma proposta verdadeiramente original e bem fundamentada.

---

# User Stories

## US01 – Descoberta pelo Inteiro Teor

**Como** coordenadora de políticas públicas em uma ONG,  
**Quero** que o sistema classifique as proposições legislativas com base na leitura do texto completo — e não apenas da ementa —  
**Para que** eu consiga identificar ameaças e oportunidades mesmo quando o tema não está explicitamente mencionado no resumo oficial.

### Critérios de Aceitação

O sistema deve realizar o download e a análise do inteiro teor de cada proposição disponível na API da Câmara. A classificação por subtema deve ocorrer independentemente de o tema aparecer ou não na ementa. O resultado da classificação deve ser exibido de forma clara no painel, com indicação de qual parte do texto fundamentou a categorização.

---

## US02 – Mapeamento de Aliados Parlamentares

**Como** coordenadora de políticas públicas em uma ONG,  
**Quero** visualizar um ranking de parlamentares (deputados e senadores) e partidos ordenado por volume de proposições em cada subtema,  
**Para** saber com quem devo agendar reuniões e priorizar esforços de incidência política.

### Critérios de Aceitação

O painel deve permitir a seleção de um subtema específico para filtrar o ranking. Os parlamentares devem ser ordenados pelo número de proposições apresentadas naquele subtema, exibindo nome, casa legislativa (Câmara ou Senado) partido e quantidade de proposições. Os partidos também devem ser ranqueados de forma agregada, facilitando a identificação de bancadas estratégicas.

---

## US04 – Auditoria de Proposições por Subtema

**Como** assessora legislativa,  
**Quero** filtrar rapidamente todas as proposições recuperadas da Câmara e do Senado sobre um subtema específico,  
**Para** garantir que qualquer projeto elaborado pelo meu parlamentar seja original, relevante e bem fundamentado, evitando redundâncias com proposições anteriores.

### Critérios de Aceitação

O sistema deve permitir a busca e filtragem de proposições por subtema, com exibição de título, ementa, autor, data de apresentação e situação atual de cada proposição. A listagem deve ordenar as proposições por data, permitindo também ordenação por parlamentar ou partido.

---

# Requisitos Funcionais

## Must Have

**RF01 — Extração de metadados via API:** O sistema deve consumir a API de Dados Abertos da Câmara dos Deputados e do Senado Federal para obter os metadados de cada proposição, incluindo título, ementa, autor, partido, data de apresentação e situação atual.

**RF02 — Obtenção do link do inteiro teor:** Para cada proposição recuperada, o sistema deve identificar e armazenar o link para o documento completo (PDF ou TXT) disponível nos servidores da Câmara ou Senado.

**RF03 — Extração do texto completo:** O sistema deve realizar o download e a extração do conteúdo textual de documentos em formato PDF, tornando-os disponíveis para processamento.

**RF04 — Classificação por subtema via NLP:** O sistema deve aplicar um modelo de processamento de linguagem natural para classificar cada proposição em um ou mais subtemas predefinidos, com base no conteúdo do texto completo.

**RF05 — Painel com volume por subtema:** O sistema deve exibir um painel interativo que mostre a distribuição de proposições por subtema, com suporte a filtros por período.

**RF06 — Ranking de parlamentares:** O sistema deve exibir um ranking de parlamentares (deputados e senadores) ordenado pelo número de proposições apresentadas, filtrável por subtema.

**RF07 — Ranking de partidos:** O sistema deve exibir um ranking de partidos políticos ordenado pelo volume agregado de proposições relacionadas aos temas monitorados, filtrável por subtema.

**RF08 - Identificação da Casa Legislativa:** O sistema deve registrar a origem de cada proposição (Câmara ou Senado) e permitir filtragem por casa legislativa.

---

## Should Have

**RF09 — Filtro por subtema:** Todos os painéis do sistema devem suportar filtragem dinâmica por subtema, refletindo os resultados em tempo real nas visualizações exibidas.

---

## Could Have

**RF10 — Identificação automática de novos temas:** O sistema deve ser capaz de identificar clusters temáticos emergentes que não se encaixem nos subtemas cadastrados, sugerindo novos temas ao administrador da plataforma para revisão e eventual inclusão.

---

## Won't Have (MVP)

**RF11 – Evolução Temporal das Proposições:** Disponibilizar visualizações e indicadores que apresentem a evolução temporal das proposições legislativas ao longo dos anos.

**RF12 – Identificação de Temas Emergentes:** Identificar automaticamente novos temas por meio de técnicas de agrupamento ou classificação, sugerindo categorias emergentes para análise.

---

# Requisitos Não Funcionais

## Desempenho e Performance

* **RNF01**: A API do backend (FastAPI) deve responder às consultas de listagem e filtragem do painel em menos de 1.5 segundos, garantindo uma navegação fluida.

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

**Dado que** uma proposição legislativa não menciona nenhum dos temas monitorados em sua ementa  
**Quando** o sistema realiza o processamento do texto completo da proposição  
**Então** ela deve ser classificada corretamente no subtema correspondente e exibida no painel com as demais proposições daquele subtema

---

## Cenário: Visualização do ranking de parlamentares

**Dado que** estou visualizando o painel da plataforma  
**Quando** seleciono o subtema "Cyberbullying e Crimes Virtuais" no painel de parlamentares  
**Então** o sistema deve exibir uma lista de deputados ordenada pelo número de proposições apresentadas sobre aquele subtema, com nome, partido e quantidade visíveis

## Cenário: Auditoria de proposições antes de redigir projeto

**Dado que** sou uma assessora legislativa e preciso verificar o que já foi proposto sobre "Proteção de Dados e Privacidade Infantil"  
**Quando** aplico o filtro por subtema "Proteção de Dados e Privacidade Infantil" no painel de proposições  
**Então** o sistema deve exibir uma listagem completa das proposições classificadas naquele subtema, ordenada por data, com título, autor e situação atual de cada uma

---

# Arquitetura

## Pipeline de Dados

O fluxo de processamento da plataforma é composto por cinco etapas sequenciais e bem delimitadas:

1. **Extração via API:** consumo periódico da API da Câmara dos Deputados e do Senado para recuperação de metadados e links das proposições.
2. **Download do inteiro teor:** obtenção dos documentos PDF ou TXT referenciados nos metadados de cada proposição.
3. **Processamento com NLP:** extração do conteúdo textual e aplicação do modelo de classificação por subtema.
4. **Classificação e enriquecimento:** associação de cada proposição aos subtemas identificados, enriquecendo o registro com os resultados da análise.
5. **Armazenamento estruturado:** persistência dos dados em base de dados relacional ou documental, otimizada para as consultas do painel.

---

## Camada de Visualização

O painel interativo será o ponto de acesso central da plataforma para todos os perfis de usuário. Ele deverá oferecer:

- Gráficos de volume de proposições por subtema
- Rankings de parlamentares e partidos, filtráveis por subtema
- Filtros combinados por período, tema, deputado e partido

---

## Princípios Arquiteturais

A arquitetura da plataforma segue três princípios fundamentais. O primeiro é a separação clara entre o pipeline de processamento de dados e a camada de visualização, garantindo que cada componente possa evoluir independentemente. O segundo é o foco em desempenho e escalabilidade, de forma que o crescimento no volume de proposições processadas não comprometa a experiência do usuário no painel. O terceiro é a facilidade de manutenção, com código modular e interfaces bem definidas entre os componentes do sistema.

---

# MVP (Produto Mínimo Viável)

O MVP da plataforma entregará as funcionalidades essenciais para que os perfis de usuário prioritários possam começar a utilizá-la de forma produtiva.

## Integração com API e Processamento

O MVP incluirá a extração de dados e metadados da API da Câmara e do Senado, o download e a leitura do inteiro teor das proposições, o processamento com NLP para classificação por subtema e o armazenamento estruturado dos resultados.

## Painel

O painel do MVP apresentará as proposições classificadas por subtema, com visualização do volume por categoria, gráficos básicos de distribuição e o ranking de parlamentares e partidos mais ativos.

## Critério Geral de Aceitação do MVP

O sistema deve permitir a análise básica de proposições legislativas relacionadas à proteção de crianças e adolescentes no ambiente digital, classificando-as por tema e subtema com base no inteiro teor e apresentando os dados de forma clara, filtrável e acessível no painel.
---

#  Versionamento

| Versão | Data | Descrição |
| ------ | ---- | --------- |
|    1.0    |   11/04/2026   |      Versão inicial do documento     |
|    1.1    |   03/05/2026   |      Ajustes estruturais e refinamento dos requisitos     |
|    1.2    |   18/05/2026   |     Reinserção da seção de Requisitos Não Funcionais      |
|    1.3.0    |   29/05/2026   |     Aprimoramento de requisitos e adiciona personas       |
|    1.3.1    |   30/05/2026   |     Adiciona e melhora User stories       |
|    1.3.2    |   08/06/2026   |     Complementa descrição de RFs e complmenta critérios de aceite |
|    1.4    |   15/06/2026      |    Ajusta descrição do MVP e arquitetura                          |
|    1.5    |   16/06/2026      |    Inclui explicitamente integração com API do Senado             |
|    1.5.1  |   23/06/2026      |    Reorganização dos requisitos funcionais, remoção da funcionalidade de evolução temporal do escopo do MVP e atualização dos subtemas monitorados.|
|   1.5.2   |   30/06/2026      | Revisão e alinhamento da especificação de requisitos, com atualização dos subtemas, reorganização dos requisitos funcionais e correção de inconsistências.|
