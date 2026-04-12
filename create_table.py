import sqlite3

conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")

# tabela de livros
cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id_livro INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT,
    ano INTEGER,
    quantidade_estoque INTEGER,
    ISBN TEXT
)
""")

# tabela de empréstimos
cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    devolvido INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()