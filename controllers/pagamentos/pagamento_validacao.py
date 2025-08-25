"""
Funções de validação dos dados de pagamentos.

Este módulo fornece funções para validar datas, valores monetários e IDs
utilizados nos pagamentos. Todas as funções retornam booleanos indicando
se o dado é válido ou não.
"""

from datetime import datetime
from typing import Any
from math import isfinite

def data_valida(data_str: str, formato: str = "%Y-%m-%d") -> bool:
    """
    Verifica se a data fornecida está no formato esperado.

    Args:
        data_str (str): Data a validar.
        formato (str): Formato da data (padrão "%Y-%m-%d").

    Returns:
        bool: True se a data for válida, False caso contrário.

    Exemplo:
        >>> data_valida("2025-08-25")
        True
        >>> data_valida("25/08/2025")
        False
    """
    try:
        datetime.strptime(data_str, formato)
        return True
    except (ValueError, TypeError):
        return False

def valor_valido(valor: Any) -> bool:
    """
    Valida se o valor é numérico, finito e positivo.

    Args:
        valor (Any): Valor a validar.

    Returns:
        bool: True se o valor for válido, False caso contrário.

    Exemplo:
        >>> valor_valido(100.50)
        True
        >>> valor_valido(-10)
        False
    """
    try:
        v = float(valor)
        return v > 0 and isfinite(v)
    except (ValueError, TypeError):
        return False

def ids_validos(*ids: Any) -> bool:
    """
    Verifica se todos os IDs fornecidos são inteiros positivos.
    Aceita também strings numéricas.

    Args:
        *ids (Any): Lista de IDs a validar.

    Returns:
        bool: True se todos os IDs forem válidos, False caso contrário.

    Exemplo:
        >>> ids_validos(1, "2", 3)
        True
        >>> ids_validos(1, -2, 3)
        False
    """
    try:
        return all(int(i) > 0 for i in ids)
    except (ValueError, TypeError):
        return False
