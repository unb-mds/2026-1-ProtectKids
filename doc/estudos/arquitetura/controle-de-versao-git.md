## Git e GitHub

### O que é o Git?

O **Git** é um sistema de controle de versão distribuído que permite registrar alterações no código ao longo do tempo.

Ele é utilizado para:
- Controlar versões de arquivos
- Trabalhar em equipe sem sobrescrever código
- Recuperar versões anteriores
- Organizar o desenvolvimento de software

---

### Como o Git funciona?

O Git trabalha com três áreas principais:

* **Working Directory**  
  Onde os arquivos são editados

* **Staging Area**  
  Onde as alterações são preparadas antes do commit

* **Repository**  
  Onde os commits ficam armazenados

---

### Fluxo básico do Git

O funcionamento do Git segue o seguinte fluxo:

* `git add` → prepara as alterações  
* `git commit` → salva uma versão  
* `git push` → envia para o repositório remoto  

---

### Principais comandos

* **git init**  
  Inicializa um repositório

* **git status**  
  Mostra o estado dos arquivos

* **git add .**  
  Adiciona arquivos para staging

* **git commit -m "mensagem"**  
  Cria um commit

* **git push**  
  Envia para o GitHub

* **git pull**  
  Atualiza o projeto

---

### Branches

Branches são ramificações do projeto que permitem desenvolver funcionalidades sem alterar a versão principal.

---

### Para que servem?

* Separar funcionalidades
* Evitar conflitos diretos
* Organizar o trabalho em equipe

---

### Exemplo

* `main` → versão principal  
* `feat/login` → nova funcionalidade  

---

### Comandos de branch

* Criar branch:

* Juntar alterações:

---

### Conflitos

Conflitos acontecem quando duas alterações modificam a mesma parte do código.

---

### Exemplo de conflito

---

### Como resolver

1. Editar manualmente o código  
2. Salvar o arquivo  
3. Executar:

---

## GitHub

### O que é?

O **GitHub** é uma plataforma de hospedagem de código que utiliza o Git para controle de versão e colaboração.

---

### Principais funcionalidades

* **Pull Requests**
  Revisão de código antes de integrar

* **Issues**
  Organização de tarefas, bugs e melhorias

* **Projects**
  Organização visual (Kanban)

---

### Fluxo de trabalho com GitHub

---

## Commits Convencionais

### O que são?

Um padrão para escrever mensagens de commit de forma clara e organizada.

---

### Estrutura

---

### Tipos mais comuns

* **feat** → nova funcionalidade  
* **fix** → correção de bug  
* **docs** → documentação  
* **refactor** → melhoria no código  

---

### Exemplos

* feat: adiciona tela de login  
* fix: corrige erro de autenticação  
* docs: atualiza documentação  

---

## Padrão de Branches

### Convenção utilizada

* feat/nome-da-feature  
* fix/nome-do-bug  
* docs/descricao  

---

## Boas práticas

* Fazer commits pequenos e frequentes  
* Escrever mensagens claras  
* Utilizar branches  
* Evitar commits diretos na main  

---

## Material de apoio

* https://git-scm.com/docs  
* https://git-scm.com/book/pt-br/v2  
* https://docs.github.com/pt  
* https://www.atlassian.com/git/tutorials  
* https://learngitbranching.js.org/
