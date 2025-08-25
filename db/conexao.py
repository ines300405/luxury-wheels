import sqlite3
import os

def conectar_base_dados() -> sqlite3.Connection:
    """
    Estabelece uma conexão com a base de dados SQLite.

    A base de dados é localizada no mesmo diretório deste script e
    o ficheiro deve ser chamado 'luxury_wheels.db'.

    Returns:
        sqlite3.Connection: Objeto de conexão com a base de dados.

    Exceções:
        sqlite3.Error: Lança exceção se houver erro ao tentar conectar.
    """
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_base_dados = os.path.join(diretorio_base, "luxury_wheels.db")
    return sqlite3.connect(caminho_base_dados)
