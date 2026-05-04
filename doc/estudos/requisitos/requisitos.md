#### Requisitos Funcionais (RF)

### O que são?

Os **Requisitos Funcionais** descrevem **o que o sistema deve fazer**, ou seja, as funcionalidades e comportamentos esperados.

Eles representam as ações, serviços e operações que o sistema deve executar para atender às necessidades do usuário.

### Exemplos

* O sistema deve permitir login com e-mail e senha
* O usuário pode cadastrar um novo cliente
* O sistema deve gerar relatórios de vendas
* O sistema deve permitir envio de mensagens no chat

---

#### Requisitos Não Funcionais (RFN)

### O que são?

Os **Requisitos Não Funcionais** descrevem **como o sistema deve se comportar**, ou seja, características de qualidade, desempenho e restrições.

Eles não tratam diretamente de funcionalidades, mas impactam **a experiência e a arquitetura do sistema**.

### Exemplos

* O sistema deve responder em até 2 segundos
* Deve suportar 1.000 usuários simultâneos
* Deve garantir criptografia de dados
* Deve estar disponível 99,9% do tempo

---

### 🔍 Diferença entre RF e RNF

| Requisitos Funcionais (RF)        | Requisitos Não Funcionais (RNF)        |
| --------------------------------- | -------------------------------------- |
| Definem **o que o sistema faz**   | Definem **como o sistema se comporta** |
| Focados em funcionalidades        | Focados em qualidade e restrições      |
| Visíveis diretamente pelo usuário | Nem sempre visíveis ao usuário         |
| Ex: "Cadastrar usuário"           | Ex: "Cadastro deve ocorrer em até 1s"  |

---

## Técnicas de Elicitação de Requisitos

### O que são?

São métodos utilizados para **coletar, entender e definir os requisitos** de um sistema junto aos stakeholders.

---

### 🧠 Brainstorm

#### O que é?

Uma técnica colaborativa onde a equipe gera **ideias livremente**, sem julgamentos iniciais.

#### Objetivo

Explorar possibilidades, levantar funcionalidades e identificar necessidades do sistema.

#### Vantagens

* Estimula criatividade
* Gera muitas ideias rapidamente
* Envolve diferentes perspectivas

#### Cuidados

* Evitar críticas durante a geração de ideias
* Filtrar e organizar depois

---

### 📄 Análise de Documentos

#### O que é?

Consiste em analisar materiais já existentes para extrair requisitos.

#### Exemplos de documentos

* Sistemas antigos
* Relatórios
* Planilhas
* Regras de negócio
* Documentações técnicas

#### Vantagens

* Base concreta de informações
* Reduz risco de esquecer requisitos importantes

---

### 🎤 Entrevistas

#### O que é?

Conversas estruturadas ou semi-estruturadas com stakeholders.

#### Objetivo

Entender necessidades, dores e expectativas diretamente com os usuários ou clientes.

#### Tipos

* Estruturada (perguntas fixas)
* Semi-estruturada (flexível)
* Aberta (exploratória)

#### Vantagens

* Informação detalhada
* Permite esclarecer dúvidas em tempo real

---

### 🔎 Análise de Documentação de API (Dados Abertos da Câmara)

#### O que é?

Consiste em estudar a documentação da API para entender **quais dados estão disponíveis e como utilizá-los**.

#### Objetivo

Identificar **o que é possível extrair**, como integrar e quais funcionalidades podem ser construídas a partir dos dados.

---

### O que analisar?

* **Endpoints disponíveis**

  * Ex: `/deputados`, `/proposicoes`
* **Métodos HTTP**

  * GET, POST, etc.
* **Parâmetros de consulta**

  * Filtros como nome, data, partido
* **Formato de resposta**

  * Geralmente JSON
* **Limitações da API**

  * Paginação, limites de requisição

---

### Exemplos do que pode ser extraído

* Lista de deputados
* Dados de partidos políticos
* Proposições (projetos de lei)
* Votações realizadas
* Despesas parlamentares

---

### Possíveis funcionalidades a partir da API

* Dashboard de gastos públicos
* Consulta de deputados por estado
* Monitoramento de projetos de lei
* Análise de votações

---

### Importância

* Ajuda a definir **requisitos funcionais reais** baseados em dados disponíveis
* Evita criar funcionalidades impossíveis
* Direciona decisões técnicas desde o início

---

## 🧩 User Stories

### O que é?

Uma *User Story* é uma descrição **curta e simples** de uma funcionalidade, escrita do ponto de vista do usuário. Serve para **guiar decisões de design e desenvolvimento**.

**Formato padrão:**

> Como **<tipo de usuário>**, quero **< funcionalidade>** para **<benefício>**.

**Exemplo:**

> Como **passageiro**, quero **vincular meu cartão** para **pagar viagens sem dinheiro**.

### Boas práticas

Toda *User Story* deve responder:

* **Quem?** → tipo de usuário
* **O quê?** → funcionalidade
* **Por quê?** → objetivo/benefício

**Exemplo:**

> Como **analista de crédito**, quero **visualizar o risco do cliente** para **aprovar crédito com mais segurança**.

### Critérios de Aceitação

Definem quando a história está **pronta e correta**.

#### 1. Por cenário (Given / When / Then)

*Descreve* comportamento esperado:

Cenário: Login válido
Dado que o usuário está na tela de login
Quando ele insere credenciais válidas
Então ele deve acessar o sistema

#### 2. Por regras

*Lista* condições objetivas:

* O sistema deve iniciar o chat ao aceitar atendimento
* Deve conectar com o próximo usuário online
* Deve enviar mensagem padrão de saudação

### Como escrever bem

* Seja **curto e direto**
* Foque no **valor para o usuário**
* Evite detalhes técnicos
* Garanta que seja **testável** (com critérios de aceitação)

---

### Material de Apoio:

* https://www.atlassian.com/br/agile/project-management/user-stories
* https://pm3.com.br/glossario/user-story/
* https://cwi.com.br/blog/user-stories-estruturacao-e-dicas-extras/
* https://www.mountaingoatsoftware.com/agile/user-stories

---

## 📊 Priorização de Requisitos

### O que é?

É o processo de decidir **o que deve ser feito primeiro** em um projeto, considerando valor, impacto e limitações (tempo, equipe, orçamento).

Serve para garantir que o time foque no que é **mais importante para o sucesso do produto**.

---

## Método MoSCoW

### O que é?

É uma técnica simples de priorização que classifica requisitos em **4 níveis de importância**:

* **M — Must Have (Deve ter)**
* **S — Should Have (Deveria ter)**
* **C — Could Have (Poderia ter)**
* **W — Won’t Have (Não terá agora)**

Ajuda o time a **definir o que é essencial vs. opcional**, facilitando decisões e evitando escopo infinito.

---

### Categorias

* **Must Have (Obrigatório)**

  * Essencial para o produto funcionar
  * Sem isso, o projeto falha

* **Should Have (Importante)**

  * Agrega muito valor
  * Pode ficar para depois sem quebrar o sistema

* **Could Have (Desejável)**

  * “Nice to have”
  * Baixo impacto se não for feito

* **Won’t Have (Agora não)**

  * Fora do escopo atual
  * Evita escopo infinito (*scope creep*)

---

### Como usar

1. Liste todos os requisitos
2. Alinhe objetivos com stakeholders
3. Classifique cada item nas 4 categorias
4. Defina limites (tempo, esforço, capacidade)
5. Revise e ajuste conforme necessário

---

### Vantagens

* Simples e rápido de aplicar
* Facilita alinhamento entre equipe
* Ajuda a focar no **MVP (mínimo viável)**
* Reduz conflitos e indecisão

---

### Cuidados

* Evite colocar “tudo” como Must Have
* Não define prioridade **dentro** de cada grupo
* Pode sofrer viés dos stakeholders

---

### Material de apoio:

* https://www.mountaingoatsoftware.com/agile/user-stories
* https://pm3.com.br/blog/metodo-moscow-framework-para-priorizar-tarefas/

---

## 🏗️ RNFs e Arquitetura de Software

### Relação entre RNFs e Arquitetura

Os Requisitos Não Funcionais (RNFs) são os principais direcionadores da arquitetura de software. A arquitetura define como o sistema será estruturado, e essa estrutura é escolhida para atender aos RNFs.

> Em outras palavras: os RNFs influenciam diretamente as decisões arquiteturais.

### Papel dos RNFs na arquitetura

* Servem como **critério para escolher estilos arquiteturais** (ex: camadas, microserviços)
* Guiam decisões sobre:

  * organização dos componentes
  * comunicação entre partes do sistema
  * tecnologias utilizadas
* Determinam **trade-offs** (ex: desempenho vs. manutenibilidade)

### Trade-offs (trocas) arquiteturais

Nem todos os RNFs podem ser maximizados ao mesmo tempo. A arquitetura é, na prática, um equilíbrio entre RNFs.

**Exemplo:**

* Mais camadas → melhor **manutenção**
* Porém → pior **desempenho**

### Exemplos de impacto na arquitetura

* **Desempenho** → uso de cache, sistemas distribuídos
* **Escalabilidade** → microserviços, balanceamento de carga
* **Segurança** → autenticação, isolamento de componentes
* **Manutenibilidade** → modularização, separação de responsabilidades
* **Disponibilidade** → redundância e tolerância a falhas

### Importância de definir cedo

* RNFs devem ser considerados **antes do design arquitetural**
* Mudanças depois são **caras e difíceis**
* Quanto mais complexo o sistema, mais a arquitetura depende dos RNFs

---
## 📚 Documentação de Requisitos: Wiki vs Repositório

### O que é Wiki?

Uma **Wiki** é um ambiente de documentação em formato de **páginas interligadas**, semelhante a um site.  
O conteúdo é organizado por navegação e links, facilitando leitura e colaboração.

### Repositório (docs/)

A documentação é mantida em **arquivos (ex: `.md`) dentro do projeto**, organizada em pastas e versionada com Git.

### Comparação

| Critério              | Wiki                            | Repositório (`docs/`)            |
| --------------------- | ------------------------------- | -------------------------------- |
| Organização           | Páginas com navegação por links | Estrutura de pastas e arquivos   |
| Edição                | Simples, via navegador          | Requer Git                       |
| Versionamento         | Limitado                        | Completo (histórico de mudanças) |
| Rastreabilidade       | Baixa                           | Alta (via commits e PRs)         |
| Colaboração           | Fácil para não técnicos         | Melhor para times técnicos       |
| Integração com código | Baixa                           | Total                            |
| Controle de mudanças  | Menor                           | Maior                            |

### Vantagens e Desvantagens

|                  | Wiki                                                                                                      | Repositório                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Vantagens**    | - Fácil de usar e editar<br>- Boa navegação<br>- Acessível para todos os perfis                           | - Versionamento completo<br>- Integração com PRs e issues<br>- Maior controle e rastreabilidade |
| **Desvantagens** | - Menor controle de versões<br>- Pode desatualizar facilmente<br>- Menor integração com o desenvolvimento | - Exige conhecimento básico de Git<br>- Menos amigável para não técnicos                        |


---

## 🎯 Recomendação

> Utilizar **documentação no repositório (`docs/`) como padrão principal**.

Considerando que o projeto está inserido em uma disciplina de Métodos e Desenvolvimento de Software, com caráter técnico e complexidade média, o uso do repositório permite aplicar na prática conceitos essenciais como versionamento, uso de branches, Pull Requests e rastreabilidade das decisões. Além disso, essa abordagem mantém a documentação integrada ao código, facilitando a organização, revisão e evolução do projeto ao longo do tempo.

A Wiki pode ser utilizada de forma complementar, especialmente para facilitar a navegação ou apresentação do conteúdo, mas não deve ser a fonte principal da documentação.

Material de apoio:
- [https://www.altexsoft.com/blog/technical-documentation-in-software-development-types-best-practices-and-tools/](https://www.altexsoft.com/blog/technical-documentation-in-software-development-types-best-practices-and-tools/)
- [https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)
- https://www.atlassian.com/work-management/knowledge-sharing/wiki