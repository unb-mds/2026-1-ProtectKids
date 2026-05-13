import subprocess
import json
import os
import requests
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES
# ==========================================
# Substitua com os dados do repositório de vocês no GitHub
REPO_OWNER = "augustogmedeiros" 
REPO_NAME = "ProtectKids"

# Caminho onde o arquivo JSON será salvo
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'data.json')

# ==========================================
# 1. COLETOR DE COMMITS (Git Log Local)
# ==========================================
def get_git_metrics():
    print("Extraindo métricas de commits do git local...")
    # Formato: Hash | Data | Mensagem \n e na linha seguinte as estatísticas (numstat)
    cmd = ['git', 'log', '--pretty=format:%H|%aI|%s', '--numstat']
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True, encoding='utf-8')
    except subprocess.CalledProcessError:
        print("Erro: Certifique-se de rodar este script dentro de um repositório git.")
        return []

    lines = result.stdout.split('\n')
    commits = []
    current_commit = None
    
    for line in lines:
        if not line.strip():
            continue
            
        # Se a linha tem os separadores, é o cabeçalho de um commit novo
        if '|' in line and len(line.split('|', 2)) == 3:
            parts = line.split('|', 2)
            current_commit = {
                "hash": parts[0],
                "date": parts[1],
                "message": parts[2],
                "insertions": 0,
                "deletions": 0,
                "total_diff": 0
            }
            commits.append(current_commit)
        else:
            # É a linha de estatística do arquivo modificado (Adições \t Deleções \t Arquivo)
            stats = line.split('\t')
            if len(stats) >= 2 and current_commit is not None:
                try:
                    # Soma as inserções e deleções (ignora arquivos binários que retornam '-')
                    ins = int(stats[0])
                    dels = int(stats[1])
                    current_commit["insertions"] += ins
                    current_commit["deletions"] += dels
                    current_commit["total_diff"] += (ins + dels)
                except ValueError:
                    pass 
                    
    return commits

# ==========================================
# 2. COLETOR DE ISSUES (GitHub API)
# ==========================================
def get_issue_metrics(owner, repo):
    print(f"Buscando issues na API do GitHub ({owner}/{repo})...")
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Se rodar via GitHub Actions, ele usa o token para não tomar block de limite de requisição
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Aviso: Não foi possível buscar issues (Status {response.status_code}).")
        print("Certifique-se de que o nome do repositório está correto.")
        return []
        
    issues_data = response.json()
    issues = []
    
    for issue in issues_data:
        # A API retorna Pull Requests junto com issues. Vamos ignorar os PRs.
        if "pull_request" in issue:
            continue
            
        # Qualidade: Quantidade de caracteres na descrição da Issue
        body_text = issue.get("body") or ""
        char_count = len(body_text)
        
        # Issue/Tempo: Cálculo do tempo de resolução
        created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        resolution_time_hours = None
        
        if issue["closed_at"]:
            closed_at = datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
            # Calcula a diferença em horas
            resolution_time_hours = round((closed_at - created_at).total_seconds() / 3600, 2)
            
        issues.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "created_at": issue["created_at"],
            "closed_at": issue["closed_at"],
            "resolution_time_hours": resolution_time_hours,
            "char_count": char_count
        })
        
    return issues

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # 1. Garante que a pasta dashboard existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 2. Coleta os dados
    commit_data = get_git_metrics()
    issue_data = get_issue_metrics(REPO_OWNER, REPO_NAME)
    
    # 3. Empacota e salva o JSON
    final_data = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "commits": commit_data,
        "issues": issue_data
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Sucesso! Dados de métricas salvos em: {OUTPUT_FILE}")