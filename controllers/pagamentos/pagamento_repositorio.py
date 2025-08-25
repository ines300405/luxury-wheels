"""
Módulo de acesso à base de dados para os pagamentos.

Contém funções CRUD para a tabela 'Pagamentos', incluindo inserção, listagem,
atualização, remoção e busca por ID.
"""

import logging
from typing import List, Optional, Dict
from controllers.utils_bd import obter_cursor

logger = logging.getLogger(__name__)


def inserir_pagamento_bd(dados: Dict) -> bool:
    """
    Insere um novo pagamento na base de dados.

    Args:
        dados (Dict): Dicionário com os campos necessários:
            - data_pagamento (str): Data do pagamento.
            - valor (float): Valor do pagamento.
            - id_forma_pagamento (int): ID da forma de pagamento utilizada.
            - id_reserva (int): ID da reserva associada.

    Returns:
        bool: True se inserido com sucesso, False em caso de erro.
    """
    query = """
        INSERT INTO Pagamentos (data_pagamento, valor, id_forma_pagamento, id_reserva)
        VALUES (?, ?, ?, ?)
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(query, (
                dados["data_pagamento"],
                float(dados["valor"]),
                int(dados["id_forma_pagamento"]),
                int(dados["id_reserva"])
            ))
        logger.info("Pagamento inserido com sucesso.")
        return True
    except Exception:
        logger.exception("Erro ao inserir pagamento.")
        return False


def listar_pagamentos_bd() -> List[Dict]:
    """
    Lista todos os pagamentos registados na base de dados.

    Returns:
        List[Dict]: Lista de dicionários, cada um representando um pagamento
        com os campos: id, id_reserva, id_forma_pagamento, valor, data_pagamento.
    """
    query = """
        SELECT id, id_reserva, id_forma_pagamento, valor, data_pagamento
        FROM Pagamentos
        ORDER BY data_pagamento DESC
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute(query)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    except Exception:
        logger.exception("Erro ao buscar pagamentos.")
        return []


def atualizar_pagamento_bd(dados: Dict) -> bool:
    """
    Atualiza os dados de um pagamento existente.

    Args:
        dados (Dict): Dicionário com os campos necessários:
            - id_pagamento (int): ID do pagamento a ser atualizado.
            - data_pagamento (str): Nova data do pagamento.
            - valor (float): Novo valor.
            - id_forma_pagamento (int): Nova forma de pagamento.
            - id_reserva (int): Nova reserva associada.

    Returns:
        bool: True se atualizado com sucesso, False caso contrário.
    """
    query = """
        UPDATE Pagamentos
        SET data_pagamento = ?, valor = ?, id_forma_pagamento = ?, id_reserva = ?
        WHERE id = ?
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(query, (
                dados["data_pagamento"],
                float(dados["valor"]),
                int(dados["id_forma_pagamento"]),
                int(dados["id_reserva"]),
                int(dados["id_pagamento"])
            ))
            return cursor.rowcount > 0
    except Exception:
        logger.exception("Erro ao atualizar pagamento.")
        return False


def remover_pagamento_bd(pagamento_id: int) -> bool:
    """
    Remove um pagamento da base de dados pelo ID.

    Args:
        pagamento_id (int): ID do pagamento a ser removido.

    Returns:
        bool: True se removido com sucesso, False caso contrário.
    """
    query = "DELETE FROM Pagamentos WHERE id = ?"
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(query, (pagamento_id,))
            return cursor.rowcount > 0
    except Exception:
        logger.exception("Erro ao remover pagamento.")
        return False


def buscar_pagamento_por_id(pagamento_id: int) -> Optional[Dict]:
    """
    Busca um pagamento específico pelo ID.

    Args:
        pagamento_id (int): ID do pagamento a ser buscado.

    Returns:
        Optional[Dict]: Dicionário com os dados do pagamento, ou None se não encontrado.
    """
    query = """
        SELECT id, id_reserva, id_forma_pagamento, valor, data_pagamento
        FROM Pagamentos
        WHERE id = ?
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute(query, (pagamento_id,))
            resultado = cursor.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            return None
    except Exception:
        logger.exception("Erro ao buscar pagamento por ID.")
        return None
