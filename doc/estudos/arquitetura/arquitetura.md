# Estudo de Arquitetura de Software

A arquitetura de software é a organização fundamental do sistema. Ela define quais são os componentes principais, como eles se comunicam e quais restrições devem seguir. 

### Por que é importante?
* **Padronização:** Garante que todo o time fale a mesma língua.
* **Manutenibilidade:** Facilita correções e evoluções no futuro.
* **Gestão de Complexidade:** Divide um problema grande em partes menores e gerenciáveis.

---

##  Pilares da Arquitetura

* **Estrutura:** Define a organização das pastas e arquivos no repositório.
* **Comunicação:** Mapeia o fluxo do dado (ex: como o dado sai da API da Câmara e chega no gráfico do usuário).
* **Qualidade:** Avalia a performance e segurança. Se precisarmos adicionar uma nova funcionalidade, o sistema deve ser robusto o suficiente para não "explodir".

---

##  Conceitos Fundamentais

### **Coesão (Idealmente Alta)**
A coesão mede o quanto as responsabilidades dentro de um único módulo (ou classe/arquivo) fazem sentido juntas. 
> **Objetivo:** Não criar "classes gorda" com funções desconexas. Cada parte deve ter sua própria responsabilidade bem definida.

### **Acoplamento (Idealmente Baixo)**
Mede o quanto um módulo conhece e depende dos detalhes internos de outro.
> **Objetivo:** Evitar entradas e saídas muito específicas que tornam o projeto rígido. Se mudarmos o banco de dados, o frontend não deveria quebrar.

---

##  Arquitetura em Camadas

Dividiremos o software em "andares". Cada andar tem uma função específica e só conversa com o andar imediatamente abaixo dele. No nosso projeto, a estrutura será:

```text
/src
  ├── /presentation   # Frontend (React): O que o usuário vê.
  ├── /api            # Endpoints: Recebe o pedido e devolve a resposta.
  ├── /business       # Lógica (NLP e Filtros): Onde o código "pensa".
  └── /infrastructure # Conexão: Scripts de coleta e acesso ao Banco.

  Uma camada superior pode usar os serviços da camada inferior, mas a camada inferior nunca deve saber que a superior existe. Isso garante o baixo acoplamento que o grupo busca manter.

---

## Por que usar o C4 Model?

O C4 model permite separar o "mapa" do nosso projeto em 4 níveis de detalhamento:

* **Nível 1 (Contexto):** Mostra o sistema no centro e quem interage com ele. Serve para qualquer tipo de pessoa entender a visão macro.
* **Nível 2 (Containers):** Mostra as frameworks e serviços que vamos utilizar em cada etapa do projeto (PostgreSQL, React, FastAPI, etc).
* **Nível 3 (Componentes):** Detalha o que tem dentro de cada container. Exemplo: dentro do container API, temos os componentes "scraper" e "classificador NLP".
* **Nível 4 (Código):** Diagrama de classes do projeto (OBS: costuma não ser utilizado em documentações ágeis).

---

## Por que não utilizar UML?

O UML é considerado um padrão de documentação antigo, criado em uma época em que eram utilizados outros conceitos de arquitetura de software. O C4 model é uma abordagem mais atualizada e alinhada com as práticas modernas de desenvolvimento.

---

## Interface vs. Implementação

A **Interface** serve exclusivamente para mostrar **o que** o código faz (o contrato). Já a lógica propriamente dita (**como** o código faz) deve estar contida inteiramente na **Implementação**.