## Docker e Docker Compose

### O que é conteinerização?

A **conteinerização** é uma forma de empacotar uma aplicação junto com tudo o que ela precisa para funcionar, como dependências, bibliotecas e configurações.

Isso garante que o sistema rode de forma semelhante em diferentes máquinas, reduzindo problemas de ambiente e incompatibilidade.

---

### Objetivo no projeto

O objetivo da conteinerização no projeto é **padronizar o ambiente de desenvolvimento do grupo**, facilitando a execução local, a configuração do banco de dados e o onboarding de novos integrantes.

Com isso, todos conseguem subir o ambiente com menos esforço e menor risco de erro.

---

### Containers vs. Máquinas Virtuais

#### O que são containers?

Containers são ambientes isolados que compartilham o kernel do sistema operacional hospedeiro.

Eles são mais leves, rápidos de iniciar e consomem menos recursos.

#### O que são máquinas virtuais?

Máquinas virtuais simulam um computador inteiro, incluindo sistema operacional próprio.

Elas são mais pesadas, consomem mais memória e geralmente têm inicialização mais lenta.

---

### Diferença entre containers e máquinas virtuais

| Containers                        | Máquinas Virtuais                     |
| --------------------------------- | ------------------------------------- |
| Mais leves                        | Mais pesadas                          |
| Inicialização rápida              | Inicialização mais lenta              |
| Compartilham o kernel do host     | Cada VM possui seu próprio sistema    |
| Menor consumo de recursos         | Maior consumo de recursos             |
| Ideais para desenvolvimento ágil  | Mais comuns em isolamento completo    |

---

## Docker

### O que é?

O **Docker** é uma plataforma que permite criar, executar e gerenciar containers.

Ele facilita o empacotamento do ambiente da aplicação, tornando a configuração mais previsível e reproduzível.

---

### Principais conceitos

* **Imagem**  
  É o modelo usado para criar um container

* **Container**  
  É a instância em execução de uma imagem

* **Volume**  
  É um mecanismo para persistir dados fora do ciclo de vida do container

* **Rede**  
  Permite a comunicação entre containers e com a máquina local

---

## Docker Compose

### O que é?

O **Docker Compose** é uma ferramenta que permite definir e executar vários serviços em conjunto por meio de um arquivo `docker-compose.yml`.

Ele é útil quando o projeto precisa de mais de um serviço, como por exemplo:

* aplicação backend
* banco de dados PostgreSQL
* ferramentas auxiliares

---

### Vantagens no projeto

* Padroniza o ambiente da equipe
* Facilita a instalação para novos membros
* Reduz erros de configuração
* Ajuda em testes de integração
* Prepara melhor o projeto para CI no futuro

---

## PostgreSQL com Docker Compose

### Objetivo

Configurar o serviço do **PostgreSQL 15+** com Docker Compose para uso no ambiente de desenvolvimento do projeto.

---

### O que deve ser configurado?

* imagem do PostgreSQL
* nome do serviço
* portas
* variáveis de ambiente
* volume para persistência
* política de reinicialização, se necessário

---

### Exemplo de configuração esperada

```yaml
services:
  postgres:
    image: postgres:15
    container_name: projeto-postgres
    environment:
      POSTGRES_DB: monitor_legislativo
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: senha_segura
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
