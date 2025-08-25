"""
Funções de validação dos dados de reservas.

Valida datas, valores, IDs, status e períodos de reserva.
Inclui logging de erros para auxiliar na depuração.
"""

from datetime import datetime
from typing import Any
from math import isfinite
import logging

logger = logging.getLogger(__name__)

def validar_data(data_str: str, formato: str = "%Y-%m-%d") -> bool:
    """
    Verifica se a data fornecida está no formato esperado.

    Args:
        data_str (str): Data a validar
        formato (str): Formato da data (default: "%Y-%m-%d")

    Returns:
        bool: True se a data for válida, False caso contrário
    """
    try:
        datetime.strptime(data_str, formato)
        return True
    except Exception:
        logger.error("Data inválida: %s", data_str)
        return False

def validar_valor(valor: Any) -> bool:
    """
    Valida se o valor é numérico, finito e não-negativo.

    Args:
        valor (Any): Valor a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    try:
        v = float(valor)
        if v >= 0 and isfinite(v):
            return True
    except Exception:
        pass
    logger.error("Valor inválido: %s", valor)
    return False

def validar_ids(*ids: Any) -> bool:
    """
    Valida se todos os IDs fornecidos são inteiros positivos.

    Args:
        *ids (Any): Um ou mais IDs a validar

    Returns:
        bool: True se todos os IDs forem válidos, False caso contrário
    """
    valido = all(isinstance(i, int) and i > 0 for i in ids)
    if not valido:
        logger.error("IDs inválidos: %s", ids)
    return valido

def validar_status(status: str) -> bool:
    """
    Valida se o status é uma string não vazia.

    Args:
        status (str): Status a validar

    Returns:
        bool: True se válido, False caso contrário
    """
    if isinstance(status, str) and status.strip():
        return True
    logger.error("Status inválido: '%s'", status)
    return False

def validar_periodo(data_inicio: str, data_fim: str) -> bool:
    """
    Valida se o período é coerente: datas válidas e data_fim >= data_inicio.

    Args:
        data_inicio (str): Data de início
        data_fim (str): Data de fim

    Returns:
        bool: True se o período for válido, False caso contrário
    """
    if not (validar_data(data_inicio) and validar_data(data_fim)):
        return False
    if datetime.strptime(data_fim, "%Y-%m-%d") < datetime.strptime(data_inicio, "%Y-%m-%d"):
        logger.error("Data fim é anterior à data início.")
        return False
    return True
