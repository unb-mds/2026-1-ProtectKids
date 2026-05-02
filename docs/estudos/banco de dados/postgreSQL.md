# Estudo sobre postgreSQL

## O que é PostgreSQL?

O PostgreSQL é um sistema de gerenciamento de banco de dados relacional (RDBMS) de código aberto. Ele é conhecido por sua confiabilidade, robustez e conformidade com os padrões SQL.

## Por que utilizar ele no projeto?

* **Confiabilidade:** Garante que todas as transações sejam processadas de forma segura (Atomicidade, Consistência, Isolamento e Durabilidade).

* **Extensibilidade:** Suporta tipos de dados complexos e consultas avançadas, ideal para o volume de dados de proposições legislativas.

* **Padrão de Mercado:** É uma das tecnologias mais exigidas no mercado de trabalho
 
* **Integração com Docker:** Para garantir a padronização do grupo no projeto, utilizamos o Docker para que todos tenham a mesma versão do banco de dados

## Pontos Chave da Configuração

* **Imagem Oficial:** Utilizamos a postgres:15 (ou versão superior).

* **Persistência (Volumes:** Como containers são efêmeros, utilizamos Volumes do Docker para que os dados não sejam apagados quando o container for parado ou removido.

* **Variáveis de Ambiente:** Configuramos POSTGRES_USER e POSTGRES_PASSWORD no docker-compose.yml para automatizar a criação do banco.

## Integração com Python (SQLModel)

Em vez de escrever SQL puro para tudo, utilizaremos o SQLModel (que usa SQLAlchemy por baixo).

ORM (Object-Relational Mapping): Transforma tabelas do banco em classes Python.

Sincronização: O SQLModel facilita a criação automática das tabelas (SQLModel.metadata.create_all(engine)) a partir das definições das nossas classes de dados.

## Modelagem Relacional (Esboço Inicial)

Nossa estrutura inicial seguirá o modelo:

Entidades Fortes: Proposicao, Parlamentar, Tema.
Relacionamentos: * Uma Proposicao pertence a um Tema.
Um Parlamentar pode ser autor de várias Proposicoes.

## Comandos Básicos de SQL

Caso precise acessar o banco via terminal (docker exec -it mds_postgres_db psql -U user_mds):

\l: Lista todos os bancos de dados.

\dt: Lista todas as tabelas do banco atual.

SELECT * FROM proposicao;: Consulta todos os dados da tabela de proposições.

\q: Sai do terminal do Postgres.

## Referências

PostgreSQL Official Documentation
SQLModel Documentation
Docker Hub - Postgres