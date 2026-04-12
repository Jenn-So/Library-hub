import sqlite3

conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

cursor.execute("""
INSERT INTO livros (titulo, autor, ano, estoque)
VALUES 
('Dom Casmurro', 'Machado de Assis', 1899, 3),
('1984', 'George Orwell', 1949, 5),
('O Hobbit', 'J.R.R. Tolkien', 1937, 2),
('A Revolução dos Bichos', 'George Orwell', 1945, 4)
""")

conn.commit()
conn.close()

print("Livros inseridos com sucesso!")
