 ## Visão Geral do Projeto

O **ProtectKids** é uma plataforma desenvolvida com o objetivo de auxiliar no monitoramento, análise e organização de informações relacionadas à proteção infantil no contexto legislativo brasileiro. O sistema realiza a coleta automatizada de dados públicos, processa essas informações utilizando técnicas de análise textual e disponibiliza os resultados de forma acessível para consulta e acompanhamento.

A proposta do projeto surgiu da necessidade de centralizar informações que, apesar de públicas, encontram-se dispersas em diferentes fontes e formatos, dificultando o acompanhamento por cidadãos, pesquisadores e organizações interessadas no tema.

A arquitetura da solução foi projetada para garantir modularidade, escalabilidade e facilidade de manutenção. Para isso, o sistema utiliza uma infraestrutura baseada em contêineres Docker, permitindo a separação clara entre os componentes responsáveis pela interface do usuário, processamento de dados, análise textual e persistência das informações.

O funcionamento da plataforma ocorre em etapas principais:

1. **Coleta de Dados**
   O sistema consome informações provenientes de fontes públicas, como a API de Dados Abertos da Câmara dos Deputados.

2. **Processamento e Análise**
   Os dados coletados passam por etapas de tratamento e análise textual utilizando técnicas de NLP (*Natural Language Processing*), permitindo identificar conteúdos relevantes para o contexto do projeto.

3. **Armazenamento**
   Após o processamento, as informações são armazenadas em banco de dados para garantir persistência e rapidez no acesso.

4. **Disponibilização ao Usuário**
   Os dados processados são exibidos em uma interface web intuitiva, permitindo consultas e acompanhamento das informações de maneira organizada.

Além do desenvolvimento técnico, o projeto também prioriza aspectos de documentação e organização arquitetural, utilizando o Modelo C4 para representar visualmente a estrutura do sistema e facilitar a comunicação entre os membros da equipe.

Dessa forma, o ProtectKids busca unir tecnologia, automação e análise de dados para contribuir com a transparência e o acompanhamento de informações relevantes à proteção infantil.
