# Sprint 04 - Integração, Automação e Extração de Dados

## Objetivo

A Sprint 04 teve como principal objetivo consolidar a infraestrutura inicial do **ProtectKids**, promovendo a integração dos componentes desenvolvidos nas sprints anteriores e preparando o projeto para um fluxo de desenvolvimento mais robusto e automatizado.

Durante esta iteração, a equipe concentrou esforços na integração definitiva do backend com o banco de dados, na implementação do pipeline de extração de dados legislativos, na estabilização do ambiente de desenvolvimento e na adoção de práticas de integração contínua (CI) e testes automatizados. Além disso, foram realizadas correções arquiteturais para manter a documentação alinhada com a implementação do sistema.

---

## Entregas Realizadas

### Arquitetura e Organização do Projeto

* Correção e atualização da estrutura do repositório, incluindo a realocação do arquivo **.gitignore**;
* Revisão e ajustes finais no **Diagrama C4**, garantindo consistência entre a documentação arquitetural e a implementação do sistema.

### Backend e Banco de Dados

* Integração completa entre **FastAPI** e **PostgreSQL** utilizando **SQLModel** como camada de mapeamento objeto-relacional (ORM);
* Estruturação da comunicação entre API e banco de dados, permitindo persistência das informações.

### Pipeline de Extração de Dados

* Desenvolvimento do **Crawler** responsável pela coleta automática de proposições legislativas por meio da API da Câmara dos Deputados;
* Implementação da base do processo de extração que futuramente alimentará o banco de dados do ProtectKids.

### Frontend

* Correções nas configurações do **Vite** e do ambiente Docker;
* Estabilização da renderização inicial da aplicação em ambiente conteinerizado.

### DevOps e Qualidade de Software

* Configuração da pipeline de **Integração Contínua (CI)** utilizando **GitHub Actions**;
* Estruturação inicial do ambiente de **testes automatizados** para Backend e Frontend, preparando o projeto para futuras validações automáticas.

---

## Issues da Sprint

| Issue | Descrição                                                               | Responsável                          | Status      |
| ----- | ----------------------------------------------------------------------- | ------------------------------------ | ----------- |
| #29   | Correção do Diagrama C4                                                 | @augustogmedeiros                    | ✅ Concluído |
| #30   | Realocação e atualização do `.gitignore`                                | @augustogmedeiros                    | ✅ Concluído |
| #32   | Correções de Configuração do Vite, Docker e Renderização Inicial        | @Golira12 e @wandinhawright          | ✅ Concluído |
| #33   | Integração do FastAPI com PostgreSQL via SQLModel                       | @augustogmedeiros e @Danielly-Mendes | ✅ Concluído |
| #35   | Configuração da Pipeline de Integração Contínua (CI) com GitHub Actions | @VegasVvegas                         | ✅ Concluído |
| #36   | Configuração Base do Ambiente de Testes Automatizados                   | @marispmorais                        | ✅ Concluído |
| #37   | Crawler de Extração de Dados utilizando a API da Câmara dos Deputados   | @augustogmedeiros                    | ✅ Concluído |

> **Observação:** Durante esta sprint também foi integrado o FastAPI ao PostgreSQL por meio do SQLModel (PR #34), consolidando a comunicação entre a API e o banco de dados.

---

## Resultados Obtidos

Ao final da Sprint 04, foram alcançados os seguintes resultados:

* Arquitetura do projeto revisada e alinhada com a implementação;
* Backend totalmente integrado ao banco de dados PostgreSQL;
* Primeira versão do crawler para extração automática de dados legislativos implementada;
* Ambiente do frontend estabilizado para desenvolvimento;
* Pipeline de Integração Contínua (CI) configurada e operacional;
* Estrutura inicial de testes automatizados preparada para evolução do projeto.

---

## Conclusão

A Sprint 04 representou um avanço significativo na maturidade técnica do ProtectKids. Com a integração entre os principais componentes da aplicação, a automação dos processos de integração e o início da coleta de dados legislativos reais, o projeto passou a contar com uma infraestrutura sólida e preparada para a implementação das funcionalidades de negócio nas próximas sprints. Essa etapa reduziu riscos relacionados à integração, aumentou a confiabilidade do desenvolvimento e estabeleceu práticas importantes de qualidade de software.

# Ata da Sprint 4 - Backend, banco e primeiras rotas

## Pauta
* Avançar no backend.
* Estruturar banco de dados.
* Criar primeiras rotas úteis para consulta.

## O que foi conversado
* Foi conversado que o backend precisava sair da fase de estrutura e começar a entregar rotas consultáveis.
* Augusto atuou nas correções e na liderança técnica da implementação.
* Mariana discutiu dados, testes e validação das respostas.
* Ryan e Wanda apontaram quais campos seriam necessários para as telas.
* Yara acompanhou problemas de execução local, banco e Docker.
* Carlos verificou andamento das tarefas e pendências.
* Danielly registrou decisões para documentação.

## Deliberações
* Foi decidido priorizar rotas de proposições e estrutura de banco.
* O grupo deliberou que a listagem deveria evitar dados pesados quando possível.
* Foi decidido validar as rotas pelo Swagger antes de passar para o frontend.

## Encaminhamentos
* Backend continuaria evoluindo listagem e detalhes.
* Dados e testes validariam retorno e consistência.
* Frontend aguardaria contrato mais estável da API.
* Infraestrutura manteria ambiente funcional para testes locais.