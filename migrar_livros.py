import json
import sqlite3

# abre o json
with open("livros.json", "r", encoding="utf-8") as file:
    livros = json.load(file)

# conecta no banco
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# garante tabela (só por segurança)
cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT,
    ano INTEGER,
    quantidade_estoque INTEGER,
    ISBN TEXT
)
""")

# insere livros
for livro in livros:
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano, quantidade_estoque, ISBN)
        VALUES (?, ?, ?, ?, ?)
    """, (
        livro["titulo"],
        livro["autor"],
        livro["ano"],
        livro["quantidade_estoque"],
        livro["ISBN"]
    ))

conn.commit()
conn.close()

print("Migração concluída com sucesso!")