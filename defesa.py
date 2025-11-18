"""
defesa.py
Correções das vulnerabilidades demostradas em ataque.py
Código seguro
"""

from flask import Flask, request
from markupsafe import escape
import os
import threading

app = Flask(__name__)

# ==========================================================
# 1) DEFESA CONTRA XSS
# ==========================================================

@app.post("/comentario")
def comentario():
    texto = request.form["texto"]

    # Escapa HTML ANTES de renderizar
    texto_seguro = escape(texto)

    return f"Comentário recebido com segurança: {texto_seguro}"


# ==========================================================
# 2) DEFESA CONTRA PATH TRAVERSAL
# ==========================================================

BASE_PATH = "arquivos"

@app.get("/abrir")
def abrir():
    nome = request.args.get("arquivo")

    # bloqueia tentativa de subir diretórios
    if ".." in nome or "/" in nome or "\\" in nome:
        return "Arquivo inválido.", 400

    caminho = os.path.join(BASE_PATH, nome)

    if not os.path.exists(caminho):
        return "Arquivo não encontrado.", 404

    with open(caminho, "r") as f:
        return f.read()


# ==========================================================
# 3) HARDCODED SECRETS – SOLUÇÃO
# ==========================================================

# ERRO: API_KEY = "123456-SECRETA"

# Correção: pegar de variável de ambiente
API_KEY = os.getenv("API_KEY", "NO_KEY_FOUND")


# ==========================================================
# 4) DEFESA CONTRA RACE CONDITION
# ==========================================================

LOCK = threading.Lock()
CONTADOR_PATH = "contador.txt"

@app.get("/escrever")
def escrever():
    with LOCK:  # garante exclusão mútua
        atual = 0
        if os.path.exists(CONTADOR_PATH):
            with open(CONTADOR_PATH, "r") as f:
                atual = int(f.read().strip() or 0)

        novo = atual + 1
        with open(CONTADOR_PATH, "w") as f:
            f.write(str(novo))

    return f"Valor atualizado com segurança: {novo}"


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)
