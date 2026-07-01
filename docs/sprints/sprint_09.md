Segue no mesmo padrão das demais sprints.

# Sprint 09 - Monitoramento de Tramitações e Expansão Analítica

## Objetivo

A Sprint 09 teve como principal objetivo ampliar as capacidades analíticas do **ProtectKids** por meio da implementação do monitoramento do ciclo de vida das proposições legislativas. Nesta iteração, a equipe concentrou seus esforços na modelagem e extração do histórico de tramitações, na criação de novos endpoints para análise de dados e na evolução da infraestrutura responsável pelo processo de ingestão de informações legislativas.

Além disso, foram realizadas melhorias na documentação da API e nos artefatos de requisitos, garantindo maior alinhamento entre backend, frontend e documentação técnica.

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

A Sprint 09 representou uma evolução importante na capacidade analítica do ProtectKids. Com a implementação do histórico de tramitações, a plataforma deixou de apresentar apenas informações estáticas das proposições e passou a acompanhar sua evolução ao longo do processo legislativo, permitindo análises mais completas sobre o comportamento das matérias no Congresso Nacional.

Além disso, as melhorias na infraestrutura de extração de dados, a criação de novos endpoints analíticos e a formalização do contrato da API fortaleceram a integração entre os componentes do sistema e prepararam a plataforma para novas funcionalidades de visualização e análise previstas para as próximas etapas do projeto.

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

## Encaminhamentos
* Danielly e Yara ajustariam documentação conforme suas frentes.
* Augusto e Mariana revisariam backend, dados e testes.
* Wanda verificaria interface.
* Carlos consolidaria pendências finais.
