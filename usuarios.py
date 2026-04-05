import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def cadastrar_usuario(nome, email, senha):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )''')

    senha_hash = generate_password_hash(senha)

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def login_usuario(email, senha):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM usuarios WHERE email = ?',
        (email,)
    )

    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario[3], senha):
        print(f"Login bem-sucedido! Bem-vindo, {usuario[1]}!")
        return True
    else:
        print("Email ou senha incorretos.")
        return False