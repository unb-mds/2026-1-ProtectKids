# Sprint 02 - Arquitetura e Infraestrutura

## Objetivo

A Sprint 02 foi dedicada à consolidação da base técnica do **ProtectKids**. O principal objetivo desta iteração foi transformar o planejamento inicial em uma estrutura sólida de desenvolvimento, definindo tanto a arquitetura do sistema quanto o ambiente em que a aplicação seria executada.

Nesta etapa, a equipe trabalhou na padronização da infraestrutura do projeto, garantindo que todos os integrantes utilizassem um ambiente de desenvolvimento consistente por meio da conteinerização com Docker. Paralelamente, foi elaborado o protótipo da arquitetura do sistema utilizando o **Modelo C4**, permitindo uma visão clara dos principais componentes da aplicação, seus relacionamentos e responsabilidades.

Ao final da sprint, o projeto passou a contar com uma base arquitetural bem definida e uma infraestrutura preparada para suportar o desenvolvimento das próximas funcionalidades.

---

## Issues da Sprint

| Issue | Descrição                                       | Responsável       | Status      |
| ----- | ----------------------------------------------- | ----------------- | ----------- |
| #19   | Implementação do Docker                         | @VegasVvegas      | ✅ Concluído |
| #21   | Protótipo da Arquitetura do Projeto (Modelo C4) | @augustogmedeiros | ✅ Concluído |

---

## Resultados Obtidos

Durante esta sprint foram alcançados os seguintes resultados:

* Definição da arquitetura inicial do ProtectKids por meio do Modelo C4;
* Estruturação do ambiente de desenvolvimento utilizando Docker;
* Padronização da infraestrutura entre todos os integrantes da equipe;
* Preparação da base técnica necessária para o desenvolvimento das funcionalidades do sistema.

---

## Conclusão

A Sprint 02 representou um importante marco para o projeto, estabelecendo os fundamentos arquiteturais e de infraestrutura que sustentariam o desenvolvimento do ProtectKids nas próximas iterações. Com a arquitetura documentada e o ambiente conteinerizado, a equipe reduziu problemas de configuração, facilitou a colaboração entre os membros e criou uma base consistente para a evolução do sistema.

# Ata da Sprint 2 - Requisitos e problema do sistema

## Pauta
* Entender quais dados o sistema deveria apresentar.
* Levantar requisitos básicos.
* Discutir como o usuário consultaria as proposições.

## O que foi conversado
* Foi conversado que o ProtectKids não deveria ser apenas uma listagem de dados, mas uma ferramenta de acompanhamento legislativo.
* Mariana e Augusto discutiram quais dados seriam necessários no backend: proposição, origem, autor, partido, tema, data e tramitações.
* Ryan e Wanda trouxeram a visão de como esses dados poderiam aparecer na interface.
* Yara apontou que a estrutura teria que rodar de forma previsível para todos os membros.
* Carlos acompanhou as tarefas e organizou as pendências.
* Danielly registrou requisitos e decisões discutidas.

## Deliberações
* Ficou decidido que as proposições seriam o eixo principal do sistema.
* O grupo decidiu prever filtros e consulta por detalhes.
* Foi deliberado que a documentação de requisitos deveria registrar o objetivo, usuários e dados principais.

## Encaminhamentos
* Backend começaria a pensar modelos e endpoints.
* Frontend seguiria estudando telas para exibir lista e detalhes.
* Infraestrutura verificaria como manter banco e serviços integrados.