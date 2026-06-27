# Funcionalidades

O **ProtectKids** reúne funcionalidades voltadas ao monitoramento, organização e análise de proposições legislativas relacionadas à proteção de crianças e adolescentes.

## Coleta Automatizada

Realiza a busca automática de proposições legislativas em fontes oficiais da **Câmara dos Deputados** e do **Senado Federal**.

## Processamento do Inteiro Teor

Efetua a leitura e extração de textos de documentos legislativos em formato PDF utilizando ferramentas automatizadas.

## Classificação Temática

Organiza as proposições em categorias relacionadas à proteção infantojuvenil por meio de técnicas de **Processamento de Linguagem Natural (PLN)** e regras heurísticas.

## Consulta de Proposições

Disponibiliza informações detalhadas sobre cada proposição, incluindo:

-  Título;
-  Ementa;
-  Origem legislativa;
-  Autor;
-  Partido;
-  Unidade Federativa (UF);
-  Data de apresentação;
-  Link para o inteiro teor.

## Histórico de Tramitações

Permite acompanhar todas as movimentações legislativas associadas às proposições monitoradas.

## Dashboard Analítico

Apresenta indicadores e informações consolidadas para facilitar a interpretação do cenário legislativo.

## Ranking de Parlamentares

Exibe a atuação de parlamentares com proposições relacionadas à proteção de crianças e adolescentes.

## Ranking de Partidos

Apresenta a participação dos partidos políticos nas proposições monitoradas.

---

# Objetivos

O ProtectKids busca:

- Centralizar informações legislativas sobre proteção de crianças e adolescentes;
- Facilitar a consulta e análise de proposições da Câmara dos Deputados e do Senado Federal;
- Apoiar a identificação de padrões e tendências legislativas;
- Organizar proposições por categorias temáticas;
- Disponibilizar uma base de dados útil para pesquisa, acompanhamento social e transparência pública;
- Auxiliar organizações, pesquisadores e cidadãos interessados na proteção infantojuvenil.

---

# Tecnologias Utilizadas

O ProtectKids utiliza uma arquitetura baseada em serviços conteinerizados, promovendo a separação entre **backend**, **frontend** e **banco de dados**.

| Camada | Tecnologia |
|---------|------------|
| **Backend** | Python, FastAPI e SQLModel |
| **Banco de Dados** | PostgreSQL |
| **Frontend** | React + Vite |
| **Processamento de PDFs** | PyMuPDF |
| **Processamento de Linguagem Natural** | spaCy (modelo para português) |
| **Infraestrutura** | Docker, Docker Compose e GitHub Actions |

---

# Fontes de Dados

As informações disponibilizadas pelo ProtectKids são obtidas a partir de fontes oficiais do Poder Legislativo Federal:

-  Câmara dos Deputados;
-  Senado Federal.

Essas fontes fornecem dados sobre:

- Proposições legislativas;
- Autores;
- Ementas;
- Textos integrais;
- Tramitações.

---

# Público-Alvo

O ProtectKids foi desenvolvido para atender diferentes perfis de usuários interessados no acompanhamento legislativo da proteção infantojuvenil, tais como:

-  Pesquisadores;
-  Estudantes;
-  Jornalistas;
-  Organizações da sociedade civil;
-  Gestores públicos;
-  Profissionais da área jurídica;
-  Cidadãos interessados em transparência legislativa.