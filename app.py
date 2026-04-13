from flask import Flask, render_template, request, redirect, url_for, session
from usuarios import cadastrar_usuario, login_usuario
from livro import listar_livros, emprestar_livro, criar_tabelas, devolver_livro, listar_emprestimos

app = Flask(__name__)
app.secret_key = "minha_chave_secreta"

criar_tabelas()

@app.route("/meus_emprestimos")
def meus_emprestimos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    lista = listar_emprestimos()
    return render_template("emprestimos.html", emprestimos=lista)

@app.route("/emprestar/<int:livro_id>")
def emprestar(livro_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario = session["usuario"]

    sucesso = emprestar_livro(livro_id, usuario)

    return redirect(url_for("livros"))

@app.route("/livros")
def livros():
    lista = listar_livros()
    return render_template("livros.html", livros=lista)
import sqlite3
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    mensagem = None
    sucesso = False
    erro = False

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if cadastrar_usuario(nome, email, senha):
            mensagem = "sucesso"
        else:
            mensagem = "erro"

    return render_template("cadastro.html", mensagem=mensagem)

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = False

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]


        if login_usuario(email, senha):
            session["usuario"] = email
            return redirect(url_for("dashboard"))
        resultado = login_usuario(email, senha)

        if resultado:  
            session["usuario"] = email
            return redirect(url_for("dashboard"))
        else: mensagem = "erro"

        if resultado:
            return redirect(url_for("catalogo"))
        else:
            erro = True

    return render_template("login.html", erro=erro)

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")
# Rota para logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Rota para a pagina do catálogo de livros
@app.route("/catalogo")
def catalogo():
    with open("livros.json", "r", encoding="utf-8") as f:
        livros = json.load(f)

    return render_template("catalogo.html", livros=livros)

@app.route("/livro/<int:id_livro>")
def livro(id_livro):

    with open("livros.json", "r", encoding="utf-8") as f:
        livros = json.load(f)

    livro_escolhido = None

    for livro in livros:
        if livro["id_livro"] == id_livro:
            livro_escolhido = livro
            break

    return render_template("livro.html", livro= livro_escolhido)

@app.route("/emprestimo/<int:id>", methods=["POST"])
def emprestimo(id):

    with open("livros.json", "r", encoding="utf-8") as f:
        livros = json.load(f)

    for livro in livros:
        if livro["id_livro"] == id:
            if livro["quantidade_estoque"] > 0:
                livro["quantidade_estoque"] -= 1
                livro_escolhido = livro

    with open("livros.json", "w", encoding="utf-8") as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)

    return render_template("livro.html", livro=livro_escolhido, msg="Empréstimo realizado com sucesso")

if __name__ == "__main__":
    app.run(debug=True)