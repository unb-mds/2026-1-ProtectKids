# Sprint 03 - Estruturação Inicial do Sistema

## Objetivo

A Sprint 03 marcou a transição do planejamento arquitetural para o desenvolvimento efetivo do **ProtectKids**. Nesta iteração, a equipe concentrou seus esforços na criação das estruturas iniciais do sistema, estabelecendo os fundamentos necessários para o desenvolvimento das funcionalidades previstas nas próximas sprints.

Além da implementação da base técnica do frontend e do backend, foram realizadas atividades voltadas à modelagem do banco de dados, refinamento dos requisitos e estruturação da documentação oficial do projeto. Como resultado, o ProtectKids passou a contar com um ambiente de desenvolvimento funcional, documentação centralizada e uma arquitetura preparada para evolução contínua.

---

## Entregas Realizadas

### Backend e Banco de Dados

* Modelagem e implementação inicial do esquema do banco de dados utilizando **PostgreSQL**;
* Configuração da estrutura base da API utilizando **FastAPI**;
* Desenvolvimento da primeira rota mockada para validação da infraestrutura e apoio às integrações futuras.

### Frontend

* Inicialização do projeto utilizando **React** e **Vite**;
* Organização da estrutura inicial de diretórios;
* Configuração das principais dependências do ambiente de desenvolvimento.

### Requisitos e Documentação

* Revisão e refinamento das **User Stories**, garantindo maior clareza e alinhamento dos requisitos;
* Elaboração do **README** oficial do repositório, contendo instruções de instalação, execução e contribuição;
* Configuração da documentação utilizando **MkDocs** e automatização do deploy por meio do **GitHub Pages**, centralizando toda a documentação técnica do projeto.

---

## Issues da Sprint

## Issues da Sprint

| Issue | Descrição | Responsável | Status |
|------|-----------|-------------|--------|
| #22 | Revisão e refinamento das User Stories | @Danielly-Mendes | ✅ Concluído |
| #23 | Configuração do MkDocs e publicação da documentação via GitHub Pages | @cgbriel28 | ✅ Concluído |
| #24 | Inicialização do projeto e configuração da estrutura base | @Golira12 / @wandinhawright | ✅ Concluído |
| #25 | Modelagem e implementação do schema inicial do banco de dados | @augustogmedeiros | ✅ Concluído |
| #26 | Criação do README oficial do repositório | @VegasVvegas | ✅ Concluído |
| #27 | Configuração do FastAPI e implementação da rota mockada inicial | @marispmorais | ✅ Concluído |
| #186 | Ajustes no layout CSS da documentação | @cgbriel28 | ✅ Concluído |

---

## Resultados Obtidos

Ao término da Sprint 03, foram alcançados os seguintes resultados:

* Estrutura inicial do frontend preparada para o desenvolvimento das interfaces;
* Backend configurado e operacional com a primeira rota funcional;
* Banco de dados modelado e implementado;
* Requisitos revisados e alinhados com os objetivos do projeto;
* Documentação oficial estruturada e publicada no GitHub Pages;
* README completo para facilitar a entrada de novos colaboradores.

---

## Conclusão

A Sprint 03 consolidou os primeiros componentes concretos do ProtectKids. Com a infraestrutura básica do sistema implementada, a documentação oficial publicada e os requisitos refinados, a equipe estabeleceu uma base sólida para o desenvolvimento das funcionalidades de negócio nas próximas iterações, reduzindo riscos de integração e promovendo maior organização do projeto.

# Ata da Sprint 3 - Arquitetura e organização técnica

## Pauta
* Definir a arquitetura inicial.
* Separar responsabilidades entre frontend, backend, banco e ETL.
* Organizar como a documentação apresentaria o sistema.

## O que foi conversado
* Foi conversado que a arquitetura precisava deixar claro o papel de cada parte do sistema.
* Augusto explicou e corrigiu pontos de backend e integração.
* Mariana contribuiu com a visão de dados, banco e testes.
* Ryan e Wanda avaliaram o impacto da arquitetura nas telas e no Figma.
* Yara discutiu Docker, ambiente local e comunicação entre serviços.
* Carlos registrou pendências da sprint e organizou o fluxo de acompanhamento.
* Danielly apoiou a documentação da arquitetura.

## Deliberações
* O grupo deliberou a separação entre API, banco de dados, frontend e processo de coleta/tratamento de dados.
* Foi decidido documentar a arquitetura em camadas, explicando o papel de cada componente.
* A equipe decidiu manter o Docker como referência para padronizar o ambiente.

## Encaminhamentos
* Augusto e Mariana seguiriam com backend, modelos e dados.
* Ryan e Wanda seguiriam com telas e protótipo.
* Yara cuidaria da estrutura de ambiente e Docker.
* Danielly ajustaria a documentação arquitetural.
