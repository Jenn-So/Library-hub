from flask import Flask, render_template, request, redirect, url_for, session
from usuarios import cadastrar_usuario, login_usuario
import sqlite3

app = Flask(__name__)
app.secret_key = "biblioteca_secreta"

# Rota para a pagina inicial (tela principal)
@app.route("/")
def home():
    return render_template("index.html")

# Rota para a pagina de cadastro
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

# Rota para a pagina de login
@app.route("/login", methods=["GET", "POST"])
def login():
    sucesso = False
    erro = False

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        resultado = login_usuario(email, senha)

        if resultado:
            session["email"] = email  # salva o usuário na sessão
            return redirect(url_for("catalogo"))
        else:
            erro = True

    return render_template("login.html", sucesso=sucesso, erro=erro)

# Rota para logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Rota para a pagina do catálogo de livros
@app.route("/catalogo")
def catalogo():
    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_livro, titulo, autor, ano, quantidade_estoque, ISBN
        FROM livros
    """)

    rows = cursor.fetchall()
    conn.close()

    livros = []
    for row in rows:
        livros.append({
            "id_livro": row[0],
            "titulo": row[1],
            "autor": row[2],
            "ano": row[3],
            "quantidade_estoque": row[4],
            "ISBN": row[5]
        })

    return render_template("catalogo.html", livros=livros)

# Rota para a pagina de detalhes do livro
@app.route("/livro/<int:id_livro>")
def livro(id_livro):
    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_livro, titulo, autor, ano, quantidade_estoque, ISBN
        FROM livros
        WHERE id_livro = ?
    """, (id_livro,))

    row = cursor.fetchone()

    if not row:
        conn.close()
        return "Livro não encontrado"

    livro = {
        "id_livro": row[0],
        "titulo": row[1],
        "autor": row[2],
        "ano": row[3],
        "quantidade_estoque": row[4],
        "ISBN": row[5]
    }

    # Verifica se o usuário já tem esse livro emprestado
    cursor.execute("""
        SELECT id FROM emprestimos
        WHERE id_usuario = (SELECT id FROM usuarios WHERE email = ?)
        AND id_livro = ? AND devolvido = 0
    """, (session["email"], id_livro))

    ja_emprestado = cursor.fetchone() is not None

    conn.close()

    msg = request.args.get("msg")

    return render_template("livro.html", livro=livro, msg=msg, ja_emprestado=ja_emprestado)

# Rota para realizar o empréstimo do livro
@app.route("/emprestimo/<int:id>", methods=["POST"])
def emprestimo(id):
    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (session["email"],))
    usuario = cursor.fetchone()

    if not usuario:
        conn.close()
        return "Usuário não encontrado"

    id_usuario = usuario[0]

    cursor.execute("""
        SELECT id FROM emprestimos
        WHERE id_usuario = ? AND id_livro = ? AND devolvido = 0
    """, (id_usuario, id))

    emprestimo_ativo = cursor.fetchone()

    if emprestimo_ativo:
        conn.close()
        return redirect(f"/livro/{id}?msg=ja_emprestado")

    cursor.execute("SELECT quantidade_estoque FROM livros WHERE id_livro = ?", (id,))
    livro = cursor.fetchone()

    if not livro:
        conn.close()
        return "Livro não encontrado"

    if livro[0] <= 0:
        conn.close()
        return redirect(f"/livro/{id}?msg=sem_estoque")

    cursor.execute("""
        UPDATE livros
        SET quantidade_estoque = quantidade_estoque - 1
        WHERE id_livro = ?
    """, (id,))

    cursor.execute("""
        INSERT INTO emprestimos (id_usuario, id_livro)
        VALUES (?, ?)
    """, (id_usuario, id))

    conn.commit()
    conn.close()

    return redirect(f"/livro/{id}")

# Rota para a pagina de empréstimos do usuário
@app.route("/meus_emprestimos")
def meus_emprestimos():
    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    # Busca o id do usuário logado
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (session["email"],))
    usuario = cursor.fetchone()

    if not usuario:
        conn.close()
        return "Usuário não encontrado"

    id_usuario = usuario[0]

    # Busca os empréstimos ativos do usuário
    cursor.execute("""
        SELECT e.id, l.titulo, l.autor, e.data_emprestimo
        FROM emprestimos e
        JOIN livros l ON e.id_livro = l.id_livro
        WHERE e.id_usuario = ? AND e.devolvido = 0
    """, (id_usuario,))

    rows = cursor.fetchall()
    conn.close()

    emprestimos = []
    for row in rows:
        emprestimos.append({
            "id": row[0],
            "titulo": row[1],
            "autor": row[2],
            "data_emprestimo": row[3]
        })

    return render_template("meus_emprestimos.html", emprestimos=emprestimos)

# Rota para devolver um livro
@app.route("/devolucao/<int:id>", methods=["POST"])
def devolucao(id):
    if "email" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    # Verifica se o empréstimo existe e não foi devolvido
    cursor.execute("""
        SELECT id_livro FROM emprestimos
        WHERE id = ? AND devolvido = 0 
    """, (id,))

    emprestimo = cursor.fetchone()

    if not emprestimo:
        conn.close()
        return "Empréstimo não encontrado"

    id_livro = emprestimo[0]

    # Marca como devolvido
    cursor.execute("""
        UPDATE emprestimos
        SET devolvido = 1
        WHERE id = ?
    """, (id,))

    # Aumenta o estoque
    cursor.execute("""
        UPDATE livros
        SET quantidade_estoque = quantidade_estoque + 1
        WHERE id_livro = ?
    """, (id_livro,))

    conn.commit()
    conn.close()

    return redirect(url_for("meus_emprestimos"))

if __name__ == "__main__":
    app.run(debug=True)