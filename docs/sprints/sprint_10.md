#  Sprint Review -- Sprint 10

##  Objetivo da Sprint
A **Sprint 10** marcou a fase final de estabilização da **Release 2** do **ProtectKids**, com foco absoluto na consolidação da arquitetura do sistema. Esta iteração não introduziu novas funcionalidades, mas sim garantiu a robustez, consistência, resiliência do pipeline de dados e a padronização de componentes críticos em produção.

---

##  Entregas Realizadas

###  Backend & Pipeline de Dados
* **Resiliência:** Implementação de mecanismos de *retry* em requisições HTTP do crawler e centralização de tratamento de erros na API (incluindo erro 404).
* **Consolidação do Crawler:** Estabilização do crawler do Senado Federal e correção de instabilidades em IDs de autores.
* **Otimização:** Filtros dinâmicos na listagem geral, adição de campo de "Título" nas proposições e limpeza segura de arquivos temporários de PDFs.

###  Inteligência Artificial (NLP)
* **Refinamento:** Otimização e correção do modelo de Processamento de Linguagem Natural utilizando a biblioteca **spaCy**, garantindo maior estabilidade na classificação textual.

###  DevOps & Infraestrutura
* **Ambiente Local:** Estabilização do ambiente local via Docker com build real da aplicação.
* **Orquestração:** Padronização do arquivo `docker-compose.yml` e inclusão de *healthcheck* do banco de dados antes da inicialização da API.
* **Padronização:** Uniformização das variáveis de ambiente do pipeline de ETL.

###  Frontend
* **Integração Total:** Conexão ponta a ponta dos endpoints do backend com a nova página principal.
* **Consistência Visual:** Refatoração de arquivos de estilo, aplicação do sistema de cores global e atualização da UI baseada no layout do Figma.

###  Documentação & Qualidade
* **Testes de Software:** Configuração de testes automatizados com **Pytest** e geração de relatórios de cobertura de código.
* **Alinhamento:** Atualização do Story Map, dos contratos de API e da documentação de requisitos.
* **Design Docs:** Atualização visual da documentação técnica via **MkDocs**.

---

##  Quadro de Issues da Sprint

| ID | Descrição da Issue | Responsável | Status |
| :--- | :--- | :--- | :---: |
| `#106` | Implementar retry nas requisições HTTP do crawler | @Danielly-Mendes | ✅ Concluído |
| `#107` | Otimização de payload e novos filtros na listagem geral | @augustogmedeiros | ✅ Concluído |
| `#108` | Flexibilização da busca por ID e tratamento de erro 404 | @augustogmedeiros | ✅ Concluído |
| `#109` | Adição do campo dinâmico "Título" nas proposições | @augustogmedeiros | ✅ Concluído |
| `#110` | Correção e otimização do modelo NLP (spaCy) | @augustogmedeiros | ✅ Concluído |
| `#111` | Estabilização do ambiente local (Docker + healthcheck DB) | @VegasVvegas | ✅ Concluído |
| `#112` | Padronização de variáveis de ambiente do ETL | @VegasVvegas | ✅ Concluído |
| `#118` | Correção de ID instável no crawler do Senado | @Danielly-Mendes | ✅ Concluído |
| `#119` | Melhorias na extração de PDF e limpeza de arquivos temporários | @augustogmedeiros | ✅ Concluído |
| `#120` | Atualização da documentação de requisitos e Story Map | @augustogmedeiros | ✅ Concluído |
| `#123` | Revisão e padronização do docker-compose.yml | @augustogmedeiros | ✅ Concluído |
| `#128` | Configuração de testes com Pytest e relatório de cobertura | @equipe | ✅ Concluído |
| `#133` | Atualização da página inicial (Figma + layout) | @wandinhawright | ✅ Concluído |
| `#134` | Refatoração de variáveis e sistema de cores | @wandinhawright | ✅ Concluído |
| `#135` | Estabilização e correções gerais do backend crawler | @augustogmedeiros | ✅ Concluído |
| `#136` | Aplicação de novo sistema de cores no frontend | @wandinhawright | ✅ Concluído |
| `#137` | Correções finais no backend crawler | @augustogmedeiros | ✅ Concluído |

### 🔗 Pull Requests Relacionadas
* **PR #113 & #114** — Correção e refatoração do backend crawler.
* **PR #121** — Fix e estabilização do crawler.
* **PR #122** — Revisão de contrato da API backend/frontend.
* **PR #123** — Padronização do docker-compose e infraestrutura.
* **PR #136** — Aplicação do novo sistema de cores no frontend.

---

##  Resultados Obtidos

> **Marco Alcançado:** O encerramento da Release 2 entrega o ProtectKids em seu estado mais seguro, integrado e previsível até o momento.

* **Confiabilidade Elevada:** Mecanismos de tolerância a falhas (*retries* e tratamentos HTTP) mitigarão significativamente quedas inesperadas de coleta.
* **Paridade de Ambientes:** Desenvolvedores e ambientes de produção passam a compartilhar a mesma consistência Docker.
* **Qualidade de Software:** Entrada oficial da cobertura de testes com Pytest, garantindo sustentabilidade para o código futuro.

---

##  Conclusão
A Sprint 10 consolidou com sucesso o ciclo de desenvolvimento da **Release 2**. Mitigamos riscos técnicos, unificamos os contratos de comunicação entre as frentes e blindamos a infraestrutura. O ProtectKids agora possui uma base sólida, estável e madura para as futuras expansões e evoluções do ecossistema.

# Ata da Sprint 10 - Deploy e consolidação final

## Pauta
* Consolidar entrega final.
* Discutir deploy e infraestrutura.
* Garantir integração entre frontend, backend e banco.

## O que foi conversado
* Foi conversado que a fase final exigia cuidado para não quebrar o que já estava funcionando.
* Yara conduziu discussões de infraestrutura, Docker, variáveis de ambiente, deploy e integração entre serviços.
* Augusto fez correções finais, apoiou backend e ajudou na integração geral.
* Mariana validou dados, testes e funcionamento das funcionalidades.
* Wanda acompanhou ajustes de interface e Figma.
* Carlos organizou as pendências finais da entrega.
* Danielly apoiou revisão final da documentação e dos registros.

## Deliberações
* Foi decidido preparar deploy com atenção a variáveis de ambiente e conexão com banco.
* O grupo deliberou que senhas e configurações sensíveis não deveriam ser expostas no repositório.
* Foi decidido revisar a integração entre serviços antes da entrega.
* A documentação final deveria refletir backend, frontend, dados, infraestrutura e deploy.

## Encaminhamentos
* Yara seguiria com infraestrutura e deploy.
* Augusto apoiaria correções finais e integração.
* Mariana validaria testes e dados.
* Wanda revisaria interface.
* Carlos e Danielly consolidariam organização e documentação final.