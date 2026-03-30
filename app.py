from flask import Flask, render_template, request, redirect, url_for
from usuarios import cadastrar_usuario, login_usuario
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    sucesso = False
    erro = False

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        resultado = cadastrar_usuario(nome, email, senha)

        if resultado:
            sucesso = True
        else:
            erro = True

    return render_template("cadastro.html", sucesso=sucesso, erro=erro)

@app.route("/login", methods=["GET", "POST"])
def login():
    sucesso = False
    erro = False

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        resultado = login_usuario(email, senha)

        if resultado:
            return redirect(url_for("catalogo"))
        else:
            erro = True

    return render_template("login.html", sucesso=sucesso, erro=erro)

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