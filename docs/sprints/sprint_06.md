# Sprint 06 - Release 1 (R1)

## Objetivo

A Sprint 06 marcou o encerramento do ciclo de desenvolvimento da **Release 1 (R1)** do **ProtectKids**. O principal objetivo desta iteração foi consolidar as funcionalidades essenciais do sistema, integrando o pipeline de Processamento de Linguagem Natural (NLP) ao processo de extração de dados, estruturando os recursos analíticos do backend e finalizando as principais interfaces do frontend.

Além da implementação das funcionalidades previstas, esta sprint concentrou esforços na estabilização da aplicação, realização de ajustes na arquitetura, fortalecimento dos processos de integração contínua e refinamento da documentação técnica, preparando o projeto para sua primeira entrega oficial.

---

## Entregas Realizadas

### Backend, Banco de Dados e Processamento de Linguagem Natural

* Integração da extração de arquivos PDF ao pipeline de classificação utilizando **Processamento de Linguagem Natural (NLP)**;
* Implementação do motor de classificação das proposições legislativas diretamente no crawler;
* Atualização da estrutura do banco de dados para suportar os novos atributos utilizados pelo NLP;
* Correção de inconsistências nas tabelas e ajustes na variável `id_proposicao` e na lógica de agrupamento dos dados;
* Criação das rotas analíticas para geração dos rankings de parlamentares;
* Implementação dos filtros utilizados pelo dashboard analítico;
* Atualização do arquivo `requirements.txt` com as novas dependências do projeto;
* Remoção de rotas de testes obsoletas do backend.

### Frontend

* Implementação do roteamento dinâmico da aplicação;
* Desenvolvimento das páginas **Sobre** e **Detalhes da Lei**;
* Integração dos filtros de pesquisa e das tabelas de rankings ao frontend;
* Ajustes na interface, incluindo:

  * atualização da paleta de cores conforme o protótipo do Figma;
  * implementação do rodapé da aplicação;
  * exibição do autor das proposições;
  * remoção de estilos globais que interferiam na renderização do site.

### DevOps e Documentação

* Configuração da execução automática dos testes utilizando **GitHub Actions**;
* Correções na documentação gerada pelo **MkDocs**;
* Inclusão do Diagrama C4 na documentação oficial;
* Ajustes no envio e renderização das imagens da arquitetura;
* Atualização do `.gitignore`, adicionando a pasta `venv` ao controle de exclusão de arquivos.

---

## Issues da Sprint

| Issue | Descrição | Responsável | Status |
|------|-----------|-------------|--------|
| #51 | Configuração do `.gitignore` e organização do ambiente de desenvolvimento | @augustogmedeiros | ✅ Concluído |
| #56 | Correção da estrutura e consistência do banco de dados | @augustogmedeiros | ✅ Concluído |
| #59 | Adequação do banco de dados para suporte ao processamento NLP | @augustogmedeiros | ✅ Concluído |
| #61 | Atualização das dependências do projeto (`requirements.txt`) | @augustogmedeiros | ✅ Concluído |
| #62 | Integração do processamento de Linguagem Natural (NLP) ao crawler | @augustogmedeiros | ✅ Concluído |
| #64 | Implementação de filtros analíticos para o dashboard | @augustogmedeiros | ✅ Concluído |
| #66 | Implementação da interface do Frontend | @Golira12 / @wandinhawright | ✅ Concluído |
| #188 | Atualização da documentação de arquitetura e visão geral do projeto | @cgbriel28 | ✅ Concluído |

### Pull Requests Relacionadas

* PR #53 — Atualização do `.gitignore` e organização da documentação;
* PR #54 — Rotas de ranking dos parlamentares;
* PR #55 — Remoção de rotas de teste do banco de dados;
* PR #57 — Correção da lógica de agrupamento e `id_proposicao`;
* PR #58 — Configuração dos testes automatizados via GitHub Actions;
* PR #60 — Correções estruturais no banco de dados;
* PR #63 — Integração da extração de PDFs e classificação por NLP;
* PR #65 — Finalização das requisições do pipeline de NLP;
* PR #67 — Implementação das páginas "Sobre", "Detalhes da Lei" e roteamento dinâmico;
* PR #68 — Integração dos filtros e rankings ao frontend;
* PR #69 — Ajustes visuais da interface, footer e exibição dos autores;
* PR #70 — Correções na documentação do MkDocs;
* PR #71 — Remoção do background global do CSS;
* PR #72 — Aplicação da paleta de cores baseada no protótipo do Figma;
* PR #73 — Inclusão do Diagrama C4 na documentação;
* PR #74 — Correção da renderização da imagem do Diagrama C4.

---

## Resultados Obtidos

Ao final da Sprint 06, foram alcançados os seguintes resultados:

* Pipeline completo de extração e classificação das proposições legislativas utilizando NLP;
* Banco de dados atualizado para suportar as novas funcionalidades analíticas;
* Backend preparado para disponibilizar rankings e filtros utilizados pelo dashboard;
* Frontend estruturado com as principais páginas da aplicação e navegação dinâmica;
* Interface alinhada ao protótipo de alta fidelidade desenvolvido no Figma;
* Processo de testes automatizados configurado via GitHub Actions;
* Documentação técnica revisada e atualizada;
* Primeira versão funcional (**Release 1**) concluída.

---

## Conclusão

A Sprint 06 representou o encerramento da primeira grande etapa de desenvolvimento do ProtectKids. A integração entre backend, frontend, banco de dados e processamento de linguagem natural resultou em uma versão funcional capaz de coletar, processar, classificar e apresentar informações legislativas relacionadas à proteção infantojuvenil.

Além da consolidação das funcionalidades essenciais da plataforma, a equipe fortaleceu a infraestrutura do projeto com testes automatizados, documentação atualizada e melhorias na experiência do usuário, entregando uma **Release 1** consistente e preparada para servir de base para as próximas evoluções do sistema.

---
## Adendo
Durante a Sprint 06, um dos integrantes da equipe precisou se desligar da disciplina, o que reduziu a capacidade de desenvolvimento disponível para as atividades de frontend. Como consequência, houve uma redistribuição das responsabilidades entre os demais membros, que assumiram as tarefas pendentes para assegurar a entrega da Release 1. Apesar da sobrecarga ocasionada, os objetivos planejados para a sprint foram concluídos com sucesso.

# Ata da Sprint 6 - Fechamento da R1 e saída do Ryan

## Pauta
* Consolidar o que estava evoluído na R1.
* Revisar backend, dados, frontend e documentação.
* Registrar a mudança de participação do Ryan.

## O que foi conversado
* Foi conversado que a R1 já tinha uma base funcional, mas ainda precisava de ajustes para avançar com segurança.
* Augusto revisou pontos do backend, fez correções e orientou prioridades técnicas.
* Mariana discutiu testes, dados e validação do que já estava implementado.
* Ryan participou até esta etapa nas discussões de frontend.
* Wanda permaneceu na frente de Figma e interface.
* Yara acompanhou infraestrutura, Docker e execução local.
* Carlos organizou as pendências e registrou o andamento da sprint.
* Danielly apoiou documentação e revisão dos registros.

## Deliberações
* Foi decidido fechar a R1 com foco no que já estava funcional.
* O grupo deliberou que, a partir da próxima sprint, seriam feitas modificações sobre o que já havia evoluído na R1.
* Foi registrado que Ryan deixaria de participar a partir da Sprint 7.
* Foi decidido manter Wanda como referência de Figma e interface junto aos ajustes do frontend.

## Encaminhamentos
* Augusto e Mariana revisariam backend, dados e testes.
* Yara verificaria infraestrutura para continuidade após a R1.
* Wanda continuaria com interface e Figma.
* Carlos atualizaria o acompanhamento das tarefas considerando a saída do Ryan.
* Danielly ajustaria documentação da evolução da R1.
