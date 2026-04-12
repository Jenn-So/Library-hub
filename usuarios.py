import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def cadastrar_usuario(nome, email, senha):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

<<<<<<< HEAD
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )''')

    senha_hash = generate_password_hash(senha)

=======
>>>>>>> 503f32009591ae1f763b0db5de5bae5e715c19b2
    try:
        senha_hash = generate_password_hash(senha)
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )

        conn.commit()
<<<<<<< HEAD
        conn.close()
=======
>>>>>>> 503f32009591ae1f763b0db5de5bae5e715c19b2
        return True

    except sqlite3.IntegrityError:
        return False

<<<<<<< HEAD
=======
    finally:
        conn.close()
>>>>>>> 503f32009591ae1f763b0db5de5bae5e715c19b2

def login_usuario(email, senha):
    
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute(
<<<<<<< HEAD
        'SELECT * FROM usuarios WHERE email = ?',
        (email,)
=======
    'SELECT * FROM usuarios WHERE email = ?',
    (email,)
>>>>>>> 503f32009591ae1f763b0db5de5bae5e715c19b2
    )

    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario[3], senha):
<<<<<<< HEAD
        print(f"Login bem-sucedido! Bem-vindo, {usuario[1]}!")
        return True
    else:
        print("Email ou senha incorretos.")
        return False
=======
        return True
    else:
        return False

>>>>>>> 503f32009591ae1f763b0db5de5bae5e715c19b2
