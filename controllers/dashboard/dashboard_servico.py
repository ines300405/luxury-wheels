"""
Serviço de Dashboard.

Fornece funções de alto nível para acesso às estatísticas do sistema,
baseadas em consultas do módulo `dashboard_repositorio`.

As funções retornam contagens de clientes, veículos, reservas e receita,
bem como relatórios agregados de reservas por mês.
"""

from typing import List, Dict
from controllers.dashboard.dashboard_repositorio import (
    contar_clientes,
    contar_veiculos_disponiveis,
    contar_reservas_ativas,
    somar_valor_pagamentos,
    reservas_agrupadas_por_mes
)


def obter_total_clientes() -> int:
    """
    Obtém o número total de clientes.

    Returns:
        int: Quantidade total de clientes registados.
    """
    return contar_clientes().get("total_clientes", 0)


def obter_total_veiculos_disponiveis() -> int:
    """
    Obtém o número de veículos disponíveis.

    Returns:
        int: Quantidade de veículos atualmente disponíveis.
    """
    return contar_veiculos_disponiveis().get("total_veiculos_disponiveis", 0)


def obter_total_reservas_ativas() -> int:
    """
    Obtém o número de reservas ativas (Confirmadas ou Pendentes).

    Returns:
        int: Quantidade de reservas ativas.
    """
    return contar_reservas_ativas().get("total_reservas_ativas", 0)


def calcular_receita_total_pagamentos() -> float:
    """
    Obtém o valor total recebido em pagamentos.

    Returns:
        float: Receita total acumulada.
    """
    return somar_valor_pagamentos().get("receita_total", 0.0)


def obter_reservas_agrupadas_por_mes() -> List[Dict[str, int]]:
    """
    Obtém a lista de reservas agrupadas por mês.

    Returns:
        List[Dict[str, int]]: Lista de dicionários no formato:
            [{"mes": "2025-01", "total": 5}, {"mes": "2025-02", "total": 8}]
    """
    return reservas_agrupadas_por_mes()
