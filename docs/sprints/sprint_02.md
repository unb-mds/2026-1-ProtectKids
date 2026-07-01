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

A Sprint 02 representou um marco importante para o projeto, pois consolidou os fundamentos arquiteturais e de infraestrutura que serviriam como base para o desenvolvimento do ProtectKids nas próximas iterações. Com a arquitetura documentada e o ambiente conteinerizado, a equipe conseguiu reduzir problemas de configuração, facilitar a colaboração entre os integrantes e estabelecer uma estrutura mais consistente para a evolução do sistema.

Durante essa sprint, também foram definidos ajustes na organização interna do grupo. Ficou acordado que Yara auxiliaria Carlos nas anotações das reuniões, contribuindo para que os registros e relatórios pós-reunião fossem revisados com mais atenção e mantidos atualizados. Além disso, Augusto assumiu responsabilidades de liderança técnica e organizacional, ficando responsável por revisar e autorizar os principais passos do projeto antes de sua execução ou finalização.

Também foi definido que Augusto manteria um acompanhamento mais próximo com os membros do grupo, realizando alinhamentos individuais sempre que necessário. Essa organização teve como objetivo melhorar a comunicação interna, evitar retrabalho e garantir que as decisões tomadas nas reuniões fossem acompanhadas de forma mais clara ao longo da sprint.

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
