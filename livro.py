import sqlite3

def conectar():
    return sqlite3.connect('biblioteca.db')


# 📚 Criar tabelas
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano INTEGER,
        estoque INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livro_id INTEGER,
        usuario_email TEXT,
        devolvido INTEGER DEFAULT 0,
        FOREIGN KEY (livro_id) REFERENCES livros(id)
    )''')

    conn.commit()
    conn.close()


# 📘 Cadastrar livro
def cadastrar_livro(titulo, autor, ano, estoque):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO livros (titulo, autor, ano, estoque) VALUES (?, ?, ?, ?)",
        (titulo, autor, ano, estoque)
    )

    conn.commit()
    conn.close()


# 📚 Listar livros disponíveis
def listar_livros():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    conn.close()
    return livros


# 📦 Verificar estoque
def verificar_estoque(livro_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT estoque FROM livros WHERE id = ?", (livro_id,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]
    return 0


# 📥 Emprestar livro
def emprestar_livro(livro_id, usuario_email):
    conn = conectar()
    cursor = conn.cursor()

    estoque = verificar_estoque(livro_id)

    if estoque <= 0:
        conn.close()
        return False  # ❌ sem estoque

    # diminui estoque
    cursor.execute(
        "UPDATE livros SET estoque = estoque - 1 WHERE id = ?",
        (livro_id,)
    )

    # registra empréstimo
    cursor.execute(
        "INSERT INTO emprestimos (livro_id, usuario_email) VALUES (?, ?)",
        (livro_id, usuario_email)
    )

    conn.commit()
    conn.close()

    return True  # ✅ sucesso


# 📤 Devolver livro
def devolver_livro(emprestimo_id):
    conn = conectar()
    cursor = conn.cursor()

    # pega o livro do empréstimo
    cursor.execute(
        "SELECT livro_id FROM emprestimos WHERE id = ? AND devolvido = 0",
        (emprestimo_id,)
    )

    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return False

    livro_id = resultado[0]

    # marca como devolvido
    cursor.execute(
        "UPDATE emprestimos SET devolvido = 1 WHERE id = ?",
        (emprestimo_id,)
    )

    # aumenta estoque
    cursor.execute(
        "UPDATE livros SET estoque = estoque + 1 WHERE id = ?",
        (livro_id,)
    )

    conn.commit()
    conn.close()

    return True


# 📊 Listar empréstimos ativos
def listar_emprestimos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.id, l.titulo, e.usuario_email
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.id
        WHERE e.devolvido = 0
    ''')

    dados = cursor.fetchall()
    conn.close()
    return dados