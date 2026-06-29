# Sprint 08 - Expansão das Fontes de Dados e Evolução da Infraestrutura

## Objetivo

A Sprint 08 teve como principal objetivo ampliar as capacidades do **ProtectKids** por meio da integração de uma nova fonte oficial de dados legislativos: o **Senado Federal**. Além da expansão do pipeline de coleta, esta iteração concentrou esforços na otimização da infraestrutura da aplicação, no aprimoramento do desempenho do processamento de documentos e na adoção definitiva de **Pull Requests (PRs)** como fluxo padrão de desenvolvimento.

Outro destaque da sprint foi a implementação de melhorias na esteira de Integração e Entrega Contínua (CI/CD), utilizando o **GitHub Container Registry (GHCR)** para o gerenciamento automatizado das imagens Docker da aplicação.

---

## Entregas Realizadas

### Metodologia e Controle de Versão

* Adoção oficial de **Pull Requests (PRs)** como fluxo obrigatório para integração de código;
* Padronização do processo de revisão por pares (Code Review);
* Maior rastreabilidade das alterações antes da integração à branch principal.

### Backend e Extração de Dados

* Implementação completa do pipeline de extração das proposições legislativas do **Senado Federal**;
* Normalização dos dados coletados para integração ao banco de dados da aplicação;
* Desenvolvimento de um extrator JSON recursivo para melhorar a leitura das respostas da API do Senado;
* Correções na comunicação com a API do Senado Federal;
* Correção da inicialização do script responsável pela coleta da Câmara dos Deputados;
* Desenvolvimento de filtros de ruídos específicos para melhorar o desempenho do pipeline de Processamento de Linguagem Natural (NLP).

### Arquitetura e Performance

* Substituição do mecanismo de processamento de PDFs por uma solução mais eficiente;
* Otimização estrutural do banco de dados para suportar simultaneamente os dados provenientes da Câmara dos Deputados e do Senado Federal.

### DevOps e Infraestrutura

* Otimização do **Dockerfile** da aplicação;
* Implementação da esteira de **CI/CD** integrada ao **GitHub Container Registry (GHCR)**;
* Configuração do **healthcheck** do PostgreSQL para garantir a disponibilidade do banco de dados antes da inicialização da API.

### Documentação e Gestão de Produto

* Refatoração e atualização do **Story Map** do projeto;
* Atualização da documentação de requisitos para contemplar oficialmente a integração com o Senado Federal.

### Frontend

* Ajustes na paleta de cores da aplicação;
* Desenvolvimento de uma nova versão da página inicial (Index);
* Estudos relacionados à ampliação da estratégia de testes de software.

---

## Issues da Sprint

| Issue | Descrição                                 | Responsável       | Status      |
| ----- | ----------------------------------------- | ----------------- | ----------- |
| #76   | Ajuste da paleta de cores                 | @wandinhawright   | ✅ Concluído |
| #77   | Nova página inicial (Index)               | @wandinhawright   | ✅ Concluído |
| #78   | Estudo sobre testes de software           | @marispmorais     | ✅ Concluído |
| #79   | Integração de Dados do Senado Federal     | @augustogmedeiros | ✅ Concluído |
| #80   | Otimização do Dockerfile e CI/CD com GHCR | @VegasVvegas      | ✅ Concluído |
| #88   | Refatoração e complementação do Story Map | @Danielly-Mendes  | ✅ Concluído |
| #89   | Otimização do processamento de PDFs       | @augustogmedeiros | ✅ Concluído |
| #90   | Filtro de ruídos para o NLP do Senado     | @augustogmedeiros | ✅ Concluído |

### Pull Requests Relacionadas

* PR #82 — Implementação do pipeline do Senado Federal;
* PR #83 — Correção da inicialização do `camara_api`;
* PR #84 — Atualização do extrator JSON recursivo do Senado;
* PR #85 — Correções finais na API do Senado;
* PR #86 — Healthcheck do PostgreSQL;
* PR #87 — Atualização da documentação de requisitos;
* PR #91 — Otimização do banco de dados;
* PR #92 — Melhorias na infraestrutura e documentação;
* PR #96 — Inclusão oficial da integração com o Senado Federal no escopo do projeto.

> **Observação:** A PR **#81**, relacionada à configuração inicial da esteira de CI/CD, foi descontinuada após ser substituída por uma implementação mais completa.

---

## Resultados Obtidos

Ao final da Sprint 08, foram alcançados os seguintes resultados:

* Integração completa da API do Senado Federal ao ProtectKids;
* Expansão da cobertura de dados legislativos da plataforma;
* Pipeline de extração mais robusto e preparado para múltiplas fontes de dados;
* Melhor desempenho na leitura de documentos PDF e na execução das consultas ao banco de dados;
* Processo de desenvolvimento mais seguro com adoção obrigatória de Pull Requests;
* Pipeline de CI/CD modernizada utilizando GitHub Container Registry (GHCR);
* Documentação e requisitos atualizados para refletir a evolução do sistema.

---

## Conclusão

A Sprint 08 representou um importante avanço na escalabilidade e maturidade do ProtectKids. A integração do Senado Federal ampliou significativamente o alcance da plataforma, permitindo o monitoramento de proposições provenientes das duas principais casas legislativas do Congresso Nacional.

Além da expansão funcional, a equipe fortaleceu sua infraestrutura de desenvolvimento por meio da adoção de Pull Requests, melhorias no pipeline de CI/CD, otimizações de desempenho e refinamentos na documentação. Essas evoluções aumentam a confiabilidade do sistema e estabelecem uma base sólida para a continuidade da **Release 2** e das próximas etapas do projeto.
