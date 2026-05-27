# 🛡️ ProtectKids

Plataforma de transparência e monitoramento legislativo baseada em Inteligência Artificial.
## 🔎 Visão Geral

O *ProtectKids* é uma plataforma desenvolvida para centralizar, monitorar e analisar proposições legislativas (Projetos de Lei) em tramitação na Câmara dos Deputados. O foco do sistema está em monitorar pautas voltadas para a proteção infantil, segurança digital de menores e o combate ao cyberbullying.

Utilizando técnicas de Processamento de Linguagem Natural (NLP), o sistema classifica automaticamente os temas das ementas extraídas, gerando indicadores inteligentes em um painel analítico para facilitar o acompanhamento dessas legislações.

---

# 🎨 Protótipo no Figma

Acesse o design e a prototipação da interface do projeto:

[Link do Projeto no Figma](https://www.figma.com/board/KBZc1R8RPPHBiZ1eoiRzFM/ProtectKids-mds?node-id=0-1&t=rHYhSFDUosKKo5mr-0)

[Link do protótipo do frontend](https://www.figma.com/design/OYd8YVckfiX0JiuJWmijDg/Prototipo-Site-MDS-squad-10?node-id=0-1&p=f&t=uiEuDatc96qDLOEM-0)

---

# 🛠️ Tecnologias Utilizadas

### Backend
- *Python* (FastAPI)
- *SQLModel* / *SQLAlchemy*
- *PostgreSQL*
- *spaCy* (NLP)

### Frontend
- *React* (Vite + JavaScript)
- *Tailwind CSS*

### Infraestrutura & DevOps
- *Docker* & *Docker Compose*
- *GitHub Actions* (CI/CD)

---

# 🚀 Como Rodar o Projeto (Quickstart)

Certifique-se de ter o *Git* e o *Docker Desktop* instalados e ativos em sua máquina antes de prosseguir.

### 1. Clonar o repositório
```bash
git clone "https://github.com/unb-mds/2026-1-ProtectKids"
cd 2026-1-ProtectKids
```

### 2. Subir os contêineres
```bash
docker-compose up -d --build
```

### 3. Popular o banco de dados
```bash
docker-compose exec backend python crawler/camara_api.py
```

### 4. Acessar a aplicação
```bash
Interface Web (Frontend): http://localhost:5173
API Rest (Backend): http://localhost:8000
Documentação Swagger: http://localhost:8000/docs 
```

## 📖 Documentação Completa (MkDocs)

Para detalhes profundos sobre a arquitetura de microsserviços, diagramas UML, modelagem do banco de dados PostgreSQL e guias de contribuição, consulte a nossa documentação oficial integrada.
https://unb-mds.github.io/2026-1-ProtectKids/

## 👥 Equipe
| Nome | GitHub |
|---|---|
| Augusto Garcia | [@augustogmedeiros](https://github.com/augustogmedeiros) |
| Carlos Gabriel | [@cgbriel28](https://github.com/cgbriel28) |
| Danielly Mendes | [@DaniellyMendes](https://github.com/DaniellyMendes) |
| Mariana Soares | [@marispmorais](https://github.com/marispmorais) |
| Ryan Lira | [@Golira12](https://github.com/Golira12) |
| Wanda Maria | [@Wandinhawright](https://github.com/Wandinhawright) |
| Yara Xavier | [@VegasVegas](https://github.com/VegasVegas) |
## 📄 Licença

Este projeto é destinado estritamente para fins acadêmicos e de pesquisa.
