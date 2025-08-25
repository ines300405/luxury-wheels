"""
Módulo de acesso à base de dados para formas de pagamento.

Responsável por operações CRUD (Create, Read, Update, Delete) na tabela
`FormasPagamento`. Também garante a criação da tabela caso não exista.
"""

import logging
from typing import List, Optional, Dict
from controllers.utils_bd import obter_cursor

logger = logging.getLogger(__name__)


def criar_tabela_formas_pagamento() -> None:
    """
    Cria a tabela `FormasPagamento` se não existir.

    Estrutura:
        - id (INTEGER, PK, AUTOINCREMENT)
        - metodo (TEXT, NOT NULL)
    """
    query = """
    CREATE TABLE IF NOT EXISTS FormasPagamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metodo TEXT NOT NULL
    )
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(query)
    except Exception:
        logger.exception("Erro ao criar tabela FormasPagamento")


def adicionar_forma_pagamento_bd(metodo: str) -> bool:
    """
    Insere uma nova forma de pagamento.

    Args:
        metodo (str): Nome do método de pagamento.

    Returns:
        bool: True se a inserção for bem-sucedida, False caso contrário.
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO FormasPagamento (metodo) VALUES (?)",
                (metodo.strip(),)
            )
        return True
    except Exception:
        logger.exception("Erro ao adicionar forma de pagamento")
        return False


def listar_formas_pagamento_bd() -> List[Dict]:
    """
    Retorna todas as formas de pagamento existentes.

    Returns:
        List[Dict]: Lista de dicionários com as chaves:
            - id (int): Identificador da forma de pagamento
            - metodo (str): Nome do método de pagamento
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute("SELECT id, metodo FROM FormasPagamento")
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    except Exception:
        logger.exception("Erro ao listar formas de pagamento")
        return []


def atualizar_forma_pagamento_bd(id_pagamento: int, novo_nome: str) -> bool:
    """
    Atualiza o nome de uma forma de pagamento.

    Args:
        id_pagamento (int): ID da forma de pagamento a ser atualizada.
        novo_nome (str): Novo nome do método.

    Returns:
        bool: True se a atualização for bem-sucedida, False caso contrário.
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE FormasPagamento SET metodo = ? WHERE id = ?",
                (novo_nome.strip(), id_pagamento)
            )
            return cursor.rowcount > 0
    except Exception:
        logger.exception("Erro ao atualizar forma de pagamento")
        return False


def remover_forma_pagamento_bd(id_pagamento: int) -> bool:
    """
    Remove uma forma de pagamento pelo ID.

    Args:
        id_pagamento (int): ID da forma de pagamento a ser removida.

    Returns:
        bool: True se a remoção for bem-sucedida, False caso contrário.
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(
                "DELETE FROM FormasPagamento WHERE id = ?",
                (id_pagamento,)
            )
            return cursor.rowcount > 0
    except Exception:
        logger.exception("Erro ao remover forma de pagamento")
        return False


def buscar_forma_pagamento_por_id(id_pagamento: int) -> Optional[Dict]:
    """
    Busca uma forma de pagamento pelo ID.

    Args:
        id_pagamento (int): Identificador da forma de pagamento.

    Returns:
        Optional[Dict]: Dicionário com os campos `id` e `metodo`,
        ou None se não for encontrado.
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute("SELECT id, metodo FROM FormasPagamento WHERE id = ?", (id_pagamento,))
            resultado = cursor.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            return None
    except Exception:
        logger.exception("Erro ao buscar forma de pagamento por ID")
        return None
