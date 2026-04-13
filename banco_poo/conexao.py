import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cursor = conexao.cursor()

def criar_tabela(conexao, cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL)
    """)

def inserir_cliente(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", data)
    conexao.commit()

def atualizar_cliente(conexao, cursor, cliente_id, nome, email):
    data = (nome, email, cliente_id)
    cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", data)
    conexao.commit()

def excluir_cliente(conexao, cursor, cliente_id):
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conexao.commit()

def inserir_clientes_em_lote(conexao, cursor, clientes):
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?)", clientes)
    conexao.commit()


# data = ("João", "joao@email.com")
# inserir_cliente(conexao, cursor, *data)
# atualizar_cliente(conexao, cursor, 1, "João Silva", "joao.silva@email.com")
# excluir_cliente(conexao, cursor, 1)
clientes = [("Maria", "maria@email.com"), ("Pedro", "pedro@email.com"), ("Ana", "ana@email.com")]
inserir_clientes_em_lote(conexao, cursor, clientes)
conexao.close()