"""
Módulo de acesso à base de dados para reservas.

Fornece funções CRUD para a tabela 'Reservas', incluindo inserção,
listagem, atualização, remoção e busca por ID.
"""

import logging
from typing import List, Dict, Optional
from controllers.utils_bd import obter_cursor

logger = logging.getLogger(__name__)

def inserir_reserva_bd(dados: Dict) -> Optional[int]:
    """
    Insere uma nova reserva na base de dados.

    Args:
        dados (Dict): Dicionário com os campos:
            - data_inicio (str)
            - data_fim (str)
            - id_cliente (int)
            - id_veiculo (int)
            - estado (str)
            - valor_total (float)

    Returns:
        Optional[int]: ID da reserva inserida ou None em caso de erro.
    """
    sql = """
        INSERT INTO Reservas (data_inicio, data_fim, id_cliente, id_veiculo, estado, valor_total)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        with obter_cursor(commit=True) as cur:
            cur.execute(sql, (
                dados["data_inicio"],
                dados["data_fim"],
                int(dados["id_cliente"]),
                int(dados["id_veiculo"]),
                dados["estado"],
                float(dados["valor_total"])
            ))
            novo_id = cur.lastrowid
        logger.info("Reserva inserida: cliente=%d, veiculo=%d, id=%d",
                    dados["id_cliente"], dados["id_veiculo"], novo_id)
        return novo_id
    except Exception:
        logger.exception("Erro ao inserir reserva.")
        return None

def listar_reservas_bd() -> List[Dict]:
    """
    Retorna todas as reservas existentes na base de dados.

    Returns:
        List[Dict]: Lista de dicionários representando cada reserva.
    """
    sql = """
        SELECT id, id_cliente, id_veiculo, data_inicio, data_fim, estado, valor_total
        FROM Reservas ORDER BY data_inicio DESC
    """
    try:
        with obter_cursor() as cur:
            cur.execute(sql)
            colunas = [desc[0] for desc in cur.description]
            return [dict(zip(colunas, linha)) for linha in cur.fetchall()]
    except Exception:
        logger.exception("Erro ao listar reservas.")
        return []

def atualizar_reserva_bd(dados: Dict) -> bool:
    """
    Atualiza uma reserva existente na base de dados.

    Args:
        dados (Dict): Dicionário com os campos:
            - id (int)
            - data_inicio (str)
            - data_fim (str)
            - id_cliente (int)
            - id_veiculo (int)
            - estado (str)
            - valor_total (float)

    Returns:
        bool: True se a atualização ocorreu com sucesso, False caso contrário.
    """
    sql = """
        UPDATE Reservas
        SET data_inicio = ?, data_fim = ?, id_cliente = ?, id_veiculo = ?, estado = ?, valor_total = ?
        WHERE id = ?
    """
    try:
        with obter_cursor(commit=True) as cur:
            cur.execute(sql, (
                dados["data_inicio"],
                dados["data_fim"],
                int(dados["id_cliente"]),
                int(dados["id_veiculo"]),
                dados["estado"],
                float(dados["valor_total"]),
                int(dados["id"])
            ))
            return cur.rowcount > 0
    except Exception:
        logger.exception("Erro ao atualizar reserva.")
        return False

def remover_reserva_bd(reserva_id: int) -> bool:
    """
    Remove uma reserva da base de dados pelo ID.

    Args:
        reserva_id (int): ID da reserva a remover.

    Returns:
        bool: True se a remoção ocorreu com sucesso, False caso contrário.
    """
    sql = "DELETE FROM Reservas WHERE id = ?"
    try:
        with obter_cursor(commit=True) as cur:
            cur.execute(sql, (reserva_id,))
            return cur.rowcount > 0
    except Exception:
        logger.exception("Erro ao remover reserva.")
        return False

def buscar_reserva_por_id(reserva_id: int) -> Optional[Dict]:
    """
    Busca uma reserva pelo seu ID.

    Args:
        reserva_id (int): ID da reserva.

    Returns:
        Optional[Dict]: Dicionário com os dados da reserva ou None se não encontrada.
    """
    sql = """
        SELECT id, id_cliente AS cliente_id, id_veiculo AS veiculo_id, data_inicio, data_fim, estado AS status, valor_total
        FROM Reservas WHERE id = ?
    """
    try:
        with obter_cursor() as cur:
            cur.execute(sql, (reserva_id,))
            resultado = cur.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cur.description]
                return dict(zip(colunas, resultado))
            return None
    except Exception:
        logger.exception("Erro ao buscar reserva por ID.")
        return None
