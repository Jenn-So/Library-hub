from flask import Flask, render_template, request, redirect, url_for
from usuarios import cadastrar_usuario, login_usuario

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
            return redirect(url_for("dashboard"))
        else:
            erro = True

    return render_template("login.html", sucesso=sucesso, erro=erro)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)