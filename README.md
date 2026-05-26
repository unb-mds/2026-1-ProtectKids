# 🛡️ ProtectKids
<p align="center">
  <img src="docs/logo.png" width="180"/>
</p>

<h1 align="center">ProtectKids</h1>

<p align="center">
  Plataforma inteligente de monitoramento e análise com IA
</p>

## Análise inteligente de conteúdos suspeitos com IA

O ProtectKids é uma plataforma de monitoramento e análise baseada em Inteligência Artificial voltada para identificação de conteúdos suspeitos relacionados à exploração infantil em ambientes digitais.  
O sistema utiliza Processamento de Linguagem Natural (NLP), análise semântica e automação de coleta de dados para auxiliar monitoramento, prevenção e análise investigativa.

---

# 🎨 Protótipo no Figma

Link do design e prototipação da interface:  
https://www.figma.com/board/KBZc1R8RPPHBiZ1eoiRzFM/ProtectKids-mds?node-id=0-1&t=rHYhSFDUosKKo5mr-0

---

# Dashboard de métricas

Link do Dashboard de monitoramento e analytics:  
https://SEU-LINK-AQUI.com

---

# Visão Geral

Com o crescimento das plataformas digitais, conteúdos ilegais e comportamentos suspeitos podem circular rapidamente e de forma difícil de rastrear.  
O ProtectKids busca solucionar esse problema utilizando IA para detectar padrões suspeitos, analisar linguagem textual e gerar indicadores inteligentes para apoio à análise de conteúdo digital.

O sistema analisa:

- Publicações textuais
- Comentários e mensagens suspeitas
- Padrões linguísticos via NLP
- Dados coletados por APIs
- Tendências e recorrência de termos

E responde:

> O conteúdo apresenta indícios de comportamento suspeito ou exploração infantil?

---

# Funcionalidades

- 🔎 Extração automática de dados via API
- 🧠 Análise semântica utilizando NLP
- 📊 Dashboard interativo com métricas
- 🚨 Sistema de alertas automáticos
- 🧾 Classificação de conteúdo suspeito
- 📈 Monitoramento de tendências
- 🐳 Deploy containerizado com Docker
- 🔐 API segura para integração externa
- 🗂️ Filtros por categoria e período
- ⚡ Processamento automatizado em tempo real

---

# Tecnologias Utilizadas

## Backend
- FastAPI
- Python
- spaCy
- PostgreSQL

## Frontend
- React
- TypeScript

## Infraestrutura
- Docker
- Docker Compose
- GitHub Actions

---

# Arquitetura do Projeto

```bash
protectkids/
│
├── backend/
│   ├── app/
│   ├── api/
│   ├── services/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   └── package.json
│
├── database/
│
├── docker-compose.yml
├── README.md
└── docs/
```

---

# Como Rodar (Quickstart)

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/protectkids.git
```

---

## 2. Entrar na pasta do projeto

```bash
cd protectkids
```

---

## 3. Subir os containers

```bash
docker-compose up -d
```

---

## 4. Verificar os containers

```bash
docker ps
```

---

## 5. Acessar aplicação

### Frontend
```bash
http://localhost:3000
```

### Backend
```bash
http://localhost:8000
```

### Documentação da API
```bash
http://localhost:8000/docs
```

---

# Exemplo de Fluxo da Aplicação

1. Coleta de dados via APIs
2. Processamento textual
3. Análise NLP
4. Classificação semântica
5. Geração de métricas
6. Exibição no dashboard
7. Emissão de alertas automáticos

---

# Objetivos do Projeto

O ProtectKids foi desenvolvido com foco em:

- prevenção digital;
- monitoramento inteligente;
- apoio investigativo;
- automação de análise textual;
- proteção de crianças e adolescentes;
- identificação de padrões suspeitos.

---

# Diferenciais

- Uso de Inteligência Artificial aplicada à segurança digital
- Pipeline automatizado de análise textual
- Dashboard analítico em tempo real
- Estrutura escalável com microsserviços
- API preparada para integração externa

---

# Segurança

O sistema foi projetado com foco em:

- autenticação segura;
- isolamento via containers;
- proteção de endpoints;
- controle de acesso;
- processamento seguro de dados.

---

# Roadmap

- [ ] Sistema de autenticação JWT
- [ ] Monitoramento em tempo real
- [ ] Painel administrativo
- [ ] Treinamento de modelos personalizados
- [ ] Integração com novas APIs
- [ ] Sistema avançado de alertas
- [ ] Deploy em cloud

---

# Equipe

Projeto desenvolvido por estudantes da Universidade de Brasília (UnB).

---

# Licença

Este projeto é destinado para fins acadêmicos e de pesquisa.
