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

    try:
        senha_hash = generate_password_hash(senha)

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


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
        return True
    else:
        return False