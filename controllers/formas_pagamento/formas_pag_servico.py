"""
Módulo de controle para Formas de Pagamento.

Responsável por:
- Inicialização da tabela na base de dados
- Operações CRUD com validação
- Exportação de dados para CSV
"""

import logging
import csv
from typing import List, Dict, Tuple
from controllers.formas_pagamento.formas_pag_validacao import nome_forma_pagamento_valido
from controllers.formas_pagamento.formas_pag_repositorio import (
    criar_tabela_formas_pagamento,
    adicionar_forma_pagamento_bd,
    listar_formas_pagamento_bd,
    atualizar_forma_pagamento_bd,
    remover_forma_pagamento_bd,
    buscar_forma_pagamento_por_id
)

logger = logging.getLogger(__name__)


def inicializar_formas_pagamento() -> None:
    """
    Cria a tabela `FormasPagamento` caso não exista.

    Logs:
        - INFO: se a tabela for criada ou já existir
        - EXCEPTION: em caso de falha
    """
    try:
        criar_tabela_formas_pagamento()
        logger.info("Tabela 'FormasPagamento' criada ou já existente.")
    except Exception:
        logger.exception("Erro ao criar a tabela 'FormasPagamento'.")


def adicionar_forma_pagamento(metodo: str) -> bool:
    """
    Adiciona uma nova forma de pagamento, após validação.

    Args:
        metodo (str): Nome do método de pagamento.

    Returns:
        bool: True se for adicionado com sucesso, False caso contrário.
    """
    if not nome_forma_pagamento_valido(metodo):
        logger.warning("Método inválido: '%s'", metodo)
        return False
    return adicionar_forma_pagamento_bd(metodo)


def editar_forma_pagamento(id_pagamento: int, novo_nome: str) -> bool:
    """
    Atualiza o nome de uma forma de pagamento.

    Args:
        id_pagamento (int): ID da forma de pagamento a editar.
        novo_nome (str): Novo nome do método.

    Returns:
        bool: True se atualizado com sucesso, False caso contrário.
    """
    if not nome_forma_pagamento_valido(novo_nome):
        logger.warning("Novo nome inválido.")
        return False
    return atualizar_forma_pagamento_bd(id_pagamento, novo_nome)


def excluir_forma_pagamento(id_pagamento: int) -> bool:
    """
    Remove uma forma de pagamento da base de dados.

    Args:
        id_pagamento (int): ID da forma de pagamento.

    Returns:
        bool: True se removido com sucesso, False caso contrário.
    """
    return remover_forma_pagamento_bd(id_pagamento)


def obter_formas_pagamento() -> List[Tuple[int, str]]:
    """
    Lista todas as formas de pagamento existentes.

    Returns:
        List[Tuple[int, str]]: Lista de tuplos no formato (id, metodo).
    """
    resultados = listar_formas_pagamento_bd()
    return [(fp["id"], fp["metodo"]) for fp in resultados]


def buscar_forma_pagamento(id_pagamento: int) -> Dict:
    """
    Busca uma forma de pagamento pelo ID.

    Args:
        id_pagamento (int): ID da forma de pagamento.

    Returns:
        Dict: Dicionário com os campos da forma de pagamento,
        ou {} se não encontrado.
    """
    return buscar_forma_pagamento_por_id(id_pagamento)


def exportar_formas_pagamento_para_csv(nome_arquivo: str = "formas_pagamento_export.csv") -> bool:
    """
    Exporta as formas de pagamento para um ficheiro CSV.

    Args:
        nome_arquivo (str, opcional): Nome do arquivo destino.
        Default = "formas_pagamento_export.csv".

    Returns:
        bool: True se exportado com sucesso, False caso contrário.
    """
    formas = obter_formas_pagamento()
    if not formas:
        logger.warning("Nenhuma forma de pagamento para exportar.")
        return False
    try:
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nome"])
            writer.writerows(formas)
        return True
    except Exception:
        logger.exception("Erro ao exportar formas de pagamento")
        return False
