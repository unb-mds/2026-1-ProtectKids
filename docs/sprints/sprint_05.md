# Sprint 05 - Métricas, Automação e Consolidação do Design

## Objetivo

A Sprint 05 foi dedicada à implementação de mecanismos de monitoramento da produtividade da equipe, ao aprimoramento do pipeline de extração de dados legislativos e à consolidação da identidade visual do **ProtectKids**. O foco principal desta iteração foi automatizar a coleta de métricas do repositório, evoluir o processo de integração contínua, estabilizar o crawler responsável pela obtenção dos dados da Câmara dos Deputados e concluir o protótipo de alta fidelidade da interface da aplicação.

Ao término da sprint, o projeto passou a contar com indicadores automatizados de desenvolvimento, uma estratégia de monitoramento contínuo da equipe e um protótipo visual consolidado para orientar a implementação do frontend.

---

## Entregas Realizadas

### Métricas e Metodologia Ágil

* Desenvolvimento do coletor de métricas do repositório;
* Implementação do dashboard de métricas utilizando **D3.js**;
* Inclusão de indicadores de qualidade, como:

  * Gráfico de distribuição de commits por horário;
  * Métrica de contribuição por autor;
  * Padronização dos usernames da equipe para garantir consistência nas análises;
* Configuração da automação da coleta de métricas utilizando **GitHub Actions**, com atualização contínua do dashboard publicado no **GitHub Pages**.

### Backend e Extração de Dados

* Revisão e correção estrutural do crawler responsável pela extração de proposições legislativas;
* Integração das melhorias relacionadas ao consumo da API da Câmara dos Deputados, proporcionando maior estabilidade ao processo de coleta.

### Frontend e Design

* Conclusão do protótipo de alta fidelidade da aplicação no **Figma**;
* Definição da identidade visual e das diretrizes de usabilidade que servirão como base para o desenvolvimento das interfaces.

### Arquitetura e Organização do Repositório

* Correção do mapeamento dos diretórios de documentação;
* Atualização do arquivo **.gitignore**, adicionando a pasta `site` para evitar o versionamento de arquivos gerados durante o build da documentação.

---

## Issues da Sprint

| Issue | Descrição                                                               | Responsável                          | Status      |
| ----- | ----------------------------------------------------------------------- | ------------------------------------ | ----------- |
| #38   | Desenvolvimento do Coletor de Métricas e Dashboard (D3.js)              | @augustogmedeiros                    | ✅ Concluído |
| #40   | Automação do Coletor de Métricas com GitHub Actions                     | @VegasVvegas                         | ✅ Concluído |
| #41   | Correção do `.gitignore` e organização dos diretórios da documentação   | @cgbriel28                           | ✅ Concluído |
| #45   | Implementação de gráfico de commits por horário e métricas de qualidade | @augustogmedeiros                    | ✅ Concluído |
| #48   | Revisão e Correção do Crawler                                           | @augustogmedeiros e @Danielly-Mendes | ✅ Concluído |
| #49   | Protótipo de Alta Fidelidade no Figma                                   | Equipe Frontend                      | ✅ Concluído |

> **Observação:** Durante esta sprint também foram integradas melhorias ao dashboard de métricas e ao crawler por meio das Pull Requests **#39**, **#44**, **#46** e **#47**, consolidando a evolução do painel analítico e da extração de dados legislativos.

---

## Resultados Obtidos

Ao final da Sprint 05, foram alcançados os seguintes resultados:

* Dashboard de métricas da equipe implementado e automatizado;
* Pipeline de atualização contínua das métricas configurado com GitHub Actions;
* Indicadores de produtividade e qualidade disponíveis para acompanhamento do projeto;
* Processo de extração de dados legislativos revisado e estabilizado;
* Protótipo de alta fidelidade finalizado, servindo como referência para o desenvolvimento da interface;
* Organização do repositório aprimorada, facilitando a manutenção e evolução da documentação.

---

## Conclusão

A Sprint 05 representou um importante avanço na maturidade do ProtectKids ao incorporar mecanismos de monitoramento da produtividade da equipe e automação dos processos de desenvolvimento. Paralelamente, o refinamento do crawler e a conclusão do protótipo de alta fidelidade estabeleceram uma base sólida tanto para a evolução da coleta de dados legislativos quanto para a implementação das interfaces da aplicação. Dessa forma, o projeto passou a contar com ferramentas que fortalecem o acompanhamento do desenvolvimento, aumentam a qualidade do código e direcionam a construção das próximas funcionalidades.

# Ata da Sprint 5 - Dados, ETL e ajustes de API

## Pauta
* Discutir coleta e tratamento dos dados legislativos.
* Melhorar organização dos dados salvos.
* Ajustar API para ficar mais útil ao frontend.

## O que foi conversado
* Foi conversado que os dados precisavam ser confiáveis, sem duplicidade e com identificadores consistentes.
* Augusto corrigiu pontos do backend e ajudou a integrar as partes.
* Mariana trabalhou a visão de dados, testes e validação.
* Ryan e Wanda alinharam quais informações seriam usadas nas telas, assim como as cores.
* Yara acompanhou ambiente, banco e execução dos serviços.
* Carlos organizou as pendências de cada frente e ajudara o carlos nas conversas mais individuais da equipe.
* Danielly registrou o que precisava entrar na documentação.

## Deliberações
* O grupo deliberou que os dados coletados deveriam passar por tratamento antes de serem usados.
* Foi decidido manter identificadores internos e externos para facilitar busca e rastreabilidade.
* Foi decidido continuar ajustando os endpoints conforme as necessidades do frontend.

## Encaminhamentos
* Mariana e Augusto seguiriam em backend, dados e testes.
* Ryan e Wanda continuariam refinando a visão de telas.
* Yara verificaria possíveis gargalos de infraestrutura, assim como estudar sobre segurança.
* Carlos acompanharia o andamento e cobranças da sprint.
