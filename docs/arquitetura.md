## Modelo Arquitetural

A arquitetura do **ProtectKids** foi documentada utilizando o **Modelo C4**, escolhido por sua abordagem hierárquica e pelo foco na clareza da comunicação. Esse modelo permite que tanto desenvolvedores quanto usuários compreendam o funcionamento do sistema sem a necessidade de conhecer padrões complexos de notação.

O Modelo C4 pode ser entendido como um sistema de *zoom arquitetural*, no qual cada nível apresenta uma visão diferente da plataforma.

### Nível 1 — Diagrama de Contexto

![Modelo C4 do ProtectKids](./assets/images/c4_container_nivel_1.png)

No primeiro nível, o sistema é tratado como uma caixa preta, abstraindo detalhes de implementação e código. O objetivo principal é responder às seguintes perguntas:

* Quem utiliza o sistema?
* Com quais sistemas externos ele se integra?

Essa visão permitiu mapear de forma clara o fluxo de interação entre os usuários do ProtectKids e serviços externos essenciais para o projeto, como a API de Dados Abertos da Câmara dos Deputados e do Senado Federal.

### Nível 2 — Diagrama de Contêineres

![Modelo C4 do ProtectKids](./assets/images/c4_container_nivel_2.png)

No segundo nível, é apresentada a macroarquitetura da aplicação, detalhando os principais componentes de software e suas responsabilidades.

Essa etapa é especialmente importante para o projeto, pois representa diretamente a infraestrutura conteinerizada baseada em Docker. Nela, são evidenciadas as interações entre:

* Frontend
* Backend
* Crawler de dados
* Modelo de NLP
* Banco de Dados

Além disso, o diagrama demonstra como esses componentes se comunicam entre si para realizar o processamento e a disponibilização das informações.


### Nível 3 - Diagrama de Componentes

![Modelo C4 do ProtectKids](./assets/images/c4_container_nivel_3.png)

No terceiro nível, o foco passa a ser a estrutura interna de um dos contêineres apresentados no nível anterior. No caso do ProtectKids, o detalhamento foi aplicado ao contêiner da API Application, implementada com FastAPI.
Esse nível permite compreender como o backend organiza suas responsabilidades internas para atender às requisições do frontend e consultar os dados armazenados no PostgreSQL.

No diagrama de componentes, a API é dividida em partes como:

Roteador principal da aplicação FastAPI
Endpoints de proposições
Endpoints de analytics
Endpoints de tramitações
Funções auxiliares de filtros e serialização
Integração com os modelos de domínio
Camada de acesso ao banco por meio do SQLModel
Geração da nuvem de palavras com apoio do processamento NLP

## Benefícios da Utilização do Modelo C4

### Comunicação Clara

A utilização de caixas e relacionamentos simplificados torna a arquitetura compreensível tanto para pessoas técnicas quanto não técnicas.

### Alinhamento da Equipe

Os diagramas funcionam como um mapa visual do projeto, permitindo que cada integrante compreenda onde sua contribuição se encaixa dentro da solução completa.

### Facilidade de Manutenção

Como a documentação descreve componentes de alto nível, pequenas alterações no código não exigem constantes reformulações dos diagramas arquiteturais.
