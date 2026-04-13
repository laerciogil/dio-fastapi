import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL)
""")

data = ("João", "joao@email.com")
cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
conexao.commit()
conexao.close()