from db.conexao import conectar_base_dados

"""
Script de teste da conexão com a base de dados SQLite.

Verifica:
    - Se a conexão pode ser estabelecida.
    - Qual é o caminho do banco de dados em uso.
"""

# Estabelece conexão com a base de dados
conn = conectar_base_dados()

# Exibe objeto de conexão (útil para depuração)
print(conn)

# Exibe informações sobre os bancos de dados anexados, incluindo o caminho
print("Usando banco em:", conn.execute("PRAGMA database_list").fetchall())

# Fecha a conexão para liberar recursos
conn.close()
