Segue no mesmo padrão das demais sprints.

# Sprint 09 - Monitoramento de Tramitações e Expansão Analítica

## Objetivo

A Sprint 09 teve como principal objetivo ampliar as capacidades analíticas do **ProtectKids** por meio da implementação do monitoramento do ciclo de vida das proposições legislativas. Nesta iteração, a execução técnica das principais funcionalidades ficou concentrada em **Augusto**, que atuou na liderança, implementação, correções e validação das entregas relacionadas ao backend, ao pipeline de extração de dados e aos novos endpoints analíticos.

Enquanto isso, os demais membros da equipe permaneceram em processo de estudo, acompanhamento e compreensão das evoluções técnicas realizadas. A sprint foi utilizada pelo grupo como um momento de aprendizado sobre o funcionamento das tramitações legislativas, estruturação de dados, integração entre backend e banco de dados, contrato da API e possibilidades de uso dessas informações pelo frontend e pela documentação.

Durante essa etapa, foram desenvolvidas funcionalidades importantes para o projeto, como a modelagem do histórico de tramitações, o pipeline de coleta dessas informações, a criação de endpoints específicos para consulta e análise, além da implementação da rota analítica utilizada para a **Nuvem de Palavras**. Também foram realizados ajustes no controle de extração dos dados, buscando reduzir sobrecarga nas APIs externas e tornar o processo de ingestão mais controlado.

A atuação de Augusto como liderança técnica foi essencial para validar os caminhos adotados e garantir que as decisões estivessem alinhadas à arquitetura do sistema. A equipe, por sua vez, acompanhou os avanços, estudou os impactos das mudanças e se preparou para contribuir de forma mais consistente nas próximas etapas do projeto.

Além da implementação técnica, a sprint também teve como objetivo manter a documentação mais próxima do estado real da aplicação, especialmente em relação ao contrato da API, aos requisitos, ao Story Map e às novas funcionalidades relacionadas ao monitoramento das tramitações legislativas.

---

## Entregas Realizadas

### Backend e Pipeline de Extração de Dados

* Modelagem do banco de dados para armazenamento do histórico de tramitações das proposições;
* Desenvolvimento do pipeline ETL responsável pela coleta e atualização das tramitações legislativas;
* Implementação de um extrator específico para o histórico de tramitações;
* Configuração de um workflow automatizado para atualização quinzenal das informações via CI/CD;
* Implementação de um limite dinâmico de extração para controlar a quantidade de dados processados e reduzir a sobrecarga sobre as APIs governamentais.

### API e Recursos Analíticos

* Criação do endpoint responsável pela consulta do histórico de tramitações;
* Implementação do cálculo do tempo de tramitação das proposições;
* Desenvolvimento da rota analítica utilizada para alimentar o componente de **Nuvem de Palavras** do dashboard;
* Correções de nomenclaturas e variáveis no backend para melhorar a consistência do código.

### Arquitetura, Documentação e Requisitos

* Documentação e formalização do contrato da API, padronizando a comunicação entre frontend e backend;
* Atualização do Story Map para contemplar as novas funcionalidades relacionadas às tramitações legislativas;
* Revisão da documentação dos requisitos, refletindo a evolução funcional do sistema.

---

## Issues da Sprint

| Issue | Descrição                                   | Responsável       | Status      |
| ----- | ------------------------------------------- | ----------------- | ----------- |
| #93   | ETL e Modelagem do Histórico de Tramitações | @augustogmedeiros | ✅ Concluído |
| #97   | Rota da API para Histórico de Tramitações   | @augustogmedeiros | ✅ Concluído |
| #101  | Rota Analítica para Nuvem de Palavras       | @augustogmedeiros | ✅ Concluído |
| #102  | Configuração de Limite Dinâmico de Extração | @augustogmedeiros | ✅ Concluído |

### Pull Requests Relacionadas

* PR #94 — Implementação do extrator de tramitações e workflow quinzenal;
* PR #95 — Implementação das funcionalidades de tramitação;
* PR #98 — Adição do cálculo do tempo de tramitação;
* PR #99 — Ajustes e evolução das funcionalidades de tramitação;
* PR-#100 — Implementação do endpoint para Nuvem de Palavras;
* PR-#103 — Documentação do contrato da API;
* PR-#104 — Correção de variáveis e nomenclaturas no backend;
* PR-#105 — Atualização do Story Map e da documentação de requisitos.

---

## Resultados Obtidos

Ao final da Sprint 09, foram alcançados os seguintes resultados:

* Implementação completa do monitoramento do histórico de tramitações das proposições legislativas;
* Banco de dados atualizado para armazenar e consultar o ciclo de vida das matérias legislativas;
* Disponibilização do cálculo do tempo de tramitação por meio da API;
* Criação da rota analítica para alimentar a visualização de Nuvem de Palavras no dashboard;
* Maior controle do processo de extração de dados por meio do limite dinâmico de ingestão;
* Formalização do contrato da API, facilitando a integração entre frontend e backend;
* Atualização da documentação e do Story Map de acordo com as novas funcionalidades implementadas.

---

## Conclusão

A Sprint 09 representou uma evolução importante na capacidade analítica do **ProtectKids**, especialmente pela implementação do histórico de tramitações das proposições legislativas. Com essa funcionalidade, a plataforma deixou de apresentar apenas informações estáticas sobre as proposições e passou a considerar também sua movimentação ao longo do processo legislativo, permitindo análises mais completas sobre o ciclo de vida das matérias acompanhadas.

Nesta sprint, a maior parte da implementação técnica foi realizada por **Augusto**, que assumiu a liderança das entregas, validou decisões, corrigiu pontos do backend e conduziu a evolução dos recursos relacionados ao ETL, banco de dados e endpoints analíticos. Sua atuação foi central para garantir que as funcionalidades fossem implementadas de forma consistente e alinhada à arquitetura do projeto.

Os demais membros da equipe, por sua vez, permaneceram em uma etapa de estudo, acompanhamento e entendimento das mudanças realizadas. Esse processo foi importante para que o grupo compreendesse melhor a complexidade das tramitações legislativas, o funcionamento do pipeline de dados, a estrutura dos novos endpoints e os impactos dessas alterações nas próximas fases do frontend, da documentação e dos testes.

Além da expansão funcional, a formalização do contrato da API, os ajustes na documentação e a atualização dos artefatos do projeto contribuíram para organizar melhor as entregas e preparar a equipe para as próximas etapas. Assim, a Sprint 09 consolidou uma base analítica mais robusta para o ProtectKids, ao mesmo tempo em que evidenciou a necessidade de ampliar gradualmente a participação técnica dos demais membros nas próximas sprints.

Além das entregas técnicas, a Sprint 09 também marcou uma mudança na organização interna da equipe. O grupo passou a adotar uma lógica de revisão cruzada, em que um membro revisa o trabalho do outro antes da finalização. Essa prática foi definida para melhorar a qualidade das entregas, reduzir inconsistências e fortalecer a colaboração entre documentação, testes, interface, backend e infraestrutura.

# Ata da Sprint 9 - Documentação, testes e revisão

## Pauta
* Revisar documentação técnica.
* Validar o que estava funcionando.
* Organizar pendências para entrega final.

## O que foi conversado
* Foi conversado que a documentação precisava explicar o projeto de forma objetiva e compatível com o que estava implementado.
* Augusto revisou correções técnicas e backend.
* Mariana contribuiu com testes, dados e validação das funcionalidades.
* Wanda revisou interface e coerência visual.
* Yara documentou pontos de infraestrutura, Docker e variáveis de ambiente.
* Carlos organizou pendências e acompanhamento Scrum.
* Danielly apoiou revisão de requisitos, arquitetura e registros.

## Deliberações
* Foi decidido revisar páginas de requisitos, arquitetura, endpoints, infraestrutura e execução local.
* O grupo deliberou que a documentação deveria evitar prometer funcionalidades não concluídas.
* Foi decidido validar endpoints e telas antes de fechar a entrega.
* Foi decidido que Augusto ficaria responsável pela implementação principal, revisão geral das entregas, revisão do Figma e encaminhamentos relacionados ao deploy.
* Ficou definido que Yara revisaria a documentação produzida por Carlos.
* Ficou definido que Carlos continuaria apoiando os registros, organização das reuniões e acompanhamento Scrum.
* Foi definido que Mariana ficaria responsável pela organização e revisão da frente de testes.
* Foi definido que Danielly auxiliaria na verificação dos testes, dados e retornos da API.
* O grupo deliberou que as entregas passariam por revisão cruzada, para que um membro pudesse conferir, corrigir e melhorar o trabalho do outro.
* Foi decidido que essa dinâmica seria adotada para aumentar a qualidade das entregas e reduzir inconsistências entre documentação, testes, interface e implementação.

## Encaminhamentos
* Danielly e Yara ajustariam documentação conforme suas frentes.
* Augusto e Mariana revisariam backend, dados e testes.
* Wanda verificaria interface.
* Carlos consolidaria pendências finais.
