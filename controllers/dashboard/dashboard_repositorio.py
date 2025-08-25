"""
Módulo de estatísticas e relatórios do sistema.

Fornece funções para obter métricas a partir da base de dados,
tais como contagem de clientes, veículos disponíveis, reservas ativas
e cálculo de receita total.

Também inclui consultas agrupadas (ex.: reservas por mês) para
uso em dashboards ou relatórios.
"""

from typing import List, Dict
from controllers.utils_bd import executar_query_valor_unico, obter_cursor
import logging

logger = logging.getLogger(__name__)


def contar_clientes() -> Dict[str, int]:
    """
    Conta o número total de clientes registados.

    Returns:
        Dict[str, int]: Dicionário com a chave "total_clientes" e respetivo valor.
    """
    try:
        total = executar_query_valor_unico("SELECT COUNT(*) FROM Clientes") or 0
        return {"total_clientes": int(total)}
    except Exception:
        logger.exception("Erro ao contar clientes")
        return {"total_clientes": 0}


def contar_veiculos_disponiveis() -> Dict[str, int]:
    """
    Conta o número de veículos disponíveis.

    Returns:
        Dict[str, int]: Dicionário com a chave "total_veiculos_disponiveis" e respetivo valor.
    """
    try:
        total = executar_query_valor_unico(
            "SELECT COUNT(*) FROM Veiculos WHERE estado = ?", ("disponível",)
        ) or 0
        return {"total_veiculos_disponiveis": int(total)}
    except Exception:
        logger.exception("Erro ao contar veículos disponíveis")
        return {"total_veiculos_disponiveis": 0}


def contar_reservas_ativas() -> Dict[str, int]:
    """
    Conta o número de reservas ativas (Confirmadas ou Pendentes).

    Returns:
        Dict[str, int]: Dicionário com a chave "total_reservas_ativas" e respetivo valor.
    """
    try:
        total = executar_query_valor_unico(
            "SELECT COUNT(*) FROM Reservas WHERE estado IN (?, ?)", ("Confirmada", "Pendente")
        ) or 0
        return {"total_reservas_ativas": int(total)}
    except Exception:
        logger.exception("Erro ao contar reservas ativas")
        return {"total_reservas_ativas": 0}


def somar_valor_pagamentos() -> Dict[str, float]:
    """
    Calcula o valor total recebido em pagamentos.

    Returns:
        Dict[str, float]: Dicionário com a chave "receita_total" e respetivo valor.
    """
    try:
        total = executar_query_valor_unico("SELECT SUM(valor) FROM Pagamentos") or 0.0
        return {"receita_total": float(total)}
    except Exception:
        logger.exception("Erro ao somar valor dos pagamentos")
        return {"receita_total": 0.0}


def reservas_agrupadas_por_mes() -> List[Dict[str, int]]:
    """
    Retorna uma lista com o total de reservas agrupadas por mês.

    Returns:
        List[Dict[str, int]]: Lista de dicionários no formato:
            [{"mes": "2025-01", "total": 5}, {"mes": "2025-02", "total": 8}]
    """
    query = """
        SELECT strftime('%Y-%m', data_inicio) AS mes, COUNT(*) AS total
        FROM Reservas
        GROUP BY mes
        ORDER BY mes;
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute(query)
            resultados = cursor.fetchall()
            return [{"mes": mes, "total": total} for mes, total in resultados]
    except Exception:
        logger.exception("Erro ao obter reservas agrupadas por mês")
        return []
