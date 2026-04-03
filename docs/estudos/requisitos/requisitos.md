#### Requisitos Funcionais (RF)
#### Requisitos Não Funcionais (RFN) 

---
## Técnicas de Elicitação de Requisitos


---
## 🧩 User Stories

### O que é?

Uma _User Story_ é uma descrição **curta e simples** de uma funcionalidade, escrita do ponto de vista do usuário. Serve para **guiar decisões de design e desenvolvimento**.

**Formato padrão:**

> Como **<tipo de usuário>**, quero **< funcionalidade>** para **<benefício>**.

**Exemplo:**

> Como **passageiro**, quero **vincular meu cartão** para **pagar viagens sem dinheiro**.

###  Boas práticas

Toda _User Story_ deve responder:

- **Quem?** → tipo de usuário
- **O quê?** → funcionalidade
- **Por quê?** → objetivo/benefício

**Exemplo:**

> Como **analista de crédito**, quero **visualizar o risco do cliente** para **aprovar crédito com mais segurança**.

###  Critérios de Aceitação

Definem quando a história está **pronta e correta**.

#### 1. Por cenário (Given / When / Then

*Descreve* comportamento esperado:

Cenário: Login válido  
Dado que o usuário está na tela de login  
Quando ele insere credenciais válidas  
Então ele deve acessar o sistema

#### 2. Por regras

*Lista* condições objetivas:

- O sistema deve iniciar o chat ao aceitar atendimento
- Deve conectar com o próximo usuário online
- Deve enviar mensagem padrão de saudação

### Como escrever bem

- Seja **curto e direto**
- Foque no **valor para o usuário**
- Evite detalhes técnicos
- Garanta que seja **testável** (com critérios de aceitação)

Material de Apoio:
- [Histórias de usuários com exemplos e um template - Atlassian](https://www.atlassian.com/br/agile/project-management/user-stories)
- [User Story, Glossário - PM3](https://pm3.com.br/glossario/user-story/)
- [User Story Estruturação e Dicas - CWI](https://cwi.com.br/blog/user-stories-estruturacao-e-dicas-extras/)
- [Agile, User Story - Mountain Goat Software](https://www.mountaingoatsoftware.com/agile/user-stories)

---
## 📊 Priorização de Requisitos
### O que é?

É o processo de decidir **o que deve ser feito primeiro** em um projeto, considerando valor, impacto e limitações (tempo, equipe, orçamento).

Serve para garantir que o time foque no que é **mais importante para o sucesso do produto**.

## Método MoSCoW

### O que é?

É uma técnica simples de priorização que classifica requisitos em **4 níveis de importância**:

- **M — Must Have (Deve ter)**
- **S — Should Have (Deveria ter)**
- **C — Could Have (Poderia ter)**
- **W — Won’t Have (Não terá agora)**

Ajuda o time a **definir o que é essencial vs. opcional**, facilitando decisões e evitando escopo infinito.

### Categorias

- **Must Have (Obrigatório)**
    - Essencial para o produto funcionar
    - Sem isso, o projeto falha
- **Should Have (Importante)**
    - Agrega muito valor
    - Pode ficar para depois sem quebrar o sistema
- **Could Have (Desejável)**
    - “Nice to have”
    - Baixo impacto se não for feito
- **Won’t Have (Agora não)**
    - Fora do escopo atual
    - Evita escopo infinito (_scope creep_)

### Como usar

1. Liste todos os requisitos
2. Alinhe objetivos com stakeholders
3. Classifique cada item nas 4 categorias
4. Defina limites (tempo, esforço, capacidade)
5. Revise e ajuste conforme necessário

### Vantagens

- Simples e rápido de aplicar
- Facilita alinhamento entre equipe
- Ajuda a focar no **MVP (mínimo viável)**
- Reduz conflitos e indecisão

### Cuidados

- Evite colocar “tudo” como Must Have
- Não define prioridade **dentro** de cada grupo
- Pode sofrer viés dos stakeholders

Material de apoio:
- [MoSCoW Prioritization - ProductPlan](https://www.mountaingoatsoftware.com/agile/user-stories)
- [Método MoSCoW: framework para ajudar a priorizar tarefas](https://pm3.com.br/blog/metodo-moscow-framework-para-priorizar-tarefas/)

---
## 🏗️ RNFs e Arquitetura de Software
### Relação entre RNFs e Arquitetura

Os Requisitos Não Funcionais (RNFs) são os principais direcionadores da arquitetura de software. A arquitetura define como o sistema será estruturado*, e essa estrutura é escolhida para atender aos RNFs.

> Em outras palavras: os RNFs influenciam diretamente as decisões arquiteturais.

### Papel dos RNFs na arquitetura

- Servem como **critério para escolher estilos arquiteturais** (ex: camadas, microserviços)
- Guiam decisões sobre:
    - organização dos componentes
    - comunicação entre partes do sistema
    - tecnologias utilizadas
- Determinam **trade-offs** (ex: desempenho vs. manutenibilidade)

### Trade-offs (trocas) arquiteturais

Nem todos os RNFs podem ser maximizados ao mesmo tempo. A arquitetura é, na prática, um equilíbrio entre RNFs.

**Exemplo:**
- Mais camadas → melhor **manutenção**
- Porém → pior **desempenho**
### Exemplos de impacto na arquitetura

- **Desempenho** → uso de cache, sistemas distribuídos
- **Escalabilidade** → microserviços, balanceamento de carga
- **Segurança** → autenticação, isolamento de componentes
- **Manutenibilidade** → modularização, separação de responsabilidades
- **Disponibilidade** → redundância e tolerância a falhas

### Importância de definir cedo

- RNFs devem ser considerados **antes do design arquitetural**
- Mudanças depois são **caras e difíceis**
- Quanto mais complexo o sistema, mais a arquitetura depende dos RNFs

---
