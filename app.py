from flask import Flask, render_template, request, redirect, url_for, session
from usuarios import cadastrar_usuario, login_usuario
from livro import listar_livros, emprestar_livro, criar_tabelas, devolver_livro, listar_emprestimos

app = Flask(__name__)
app.secret_key = "minha_chave_secreta"

criar_tabelas()

@app.route("/devolver/<int:emprestimo_id>")
def devolver(emprestimo_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    devolver_livro(emprestimo_id)
    return redirect(url_for("meus_emprestimos"))

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = None

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
    mensagem = None

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if login_usuario(email, senha):
            session["usuario"] = email
            return redirect(url_for("dashboard"))
        else:
            mensagem = "erro"

    return render_template("login.html", mensagem=mensagem)

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)