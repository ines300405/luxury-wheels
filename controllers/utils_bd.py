import logging
from typing import Any, Optional
from contextlib import contextmanager
from db.conexao import conectar_base_dados
import sqlite3

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

@contextmanager
def obter_cursor(commit: bool = False):
    """
    Context manager para obter um cursor da base de dados SQLite.

    Este cursor retorna resultados como dicionários (sqlite3.Row).
    Fecha automaticamente o cursor e a conexão no final do bloco.
    Faz commit se commit=True, ou rollback em caso de erro.

    Parâmetros:
        commit (bool): Se True, aplica commit no final do bloco (padrão=False).

    Yields:
        sqlite3.Cursor: Cursor da base de dados pronto para executar queries.

    Exceções:
        ConnectionError: Se a conexão ao banco de dados falhar.
        Repropaga qualquer exceção ocorrida durante a execução do bloco.
    """
    conexao = conectar_base_dados()
    if conexao is None:
        logger.error("Não foi possível conectar ao banco de dados.")
        raise ConnectionError("Falha na conexão com o banco de dados.")

    # Define o row_factory para devolver dicionários
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()
    try:
        yield cursor
        if commit:
            conexao.commit()  # só comita se commit=True
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()


def executar_query_valor_unico(query: str, parametros: Optional[tuple] = None) -> Any:
    """
    Executa uma query que retorna um único valor (ex: COUNT, SUM, MAX).

    Parâmetros:
        query (str): A query SQL a ser executada.
        parametros (tuple, opcional): Parâmetros para a query (padrão=None).

    Retorna:
        Any: O valor escalar retornado pela query, ou None se não houver resultados ou ocorrer erro.

    Log:
        Gera um log de exceção em caso de erro durante a execução da query.
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute(query, parametros or ())
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception:
        logger.exception("Erro ao executar query escalar: %s", query)
        return None
