"""
Camada de serviço para a lógica de negócio dos pagamentos.

Este módulo valida os dados de pagamentos e interage com o repositório (CRUD).
Fornece funções para adicionar, editar, excluir, listar e exportar pagamentos.
"""

import csv
import logging
from typing import List, Tuple, Dict, Union

from controllers.pagamentos.pagamento_validacao import data_valida, valor_valido, ids_validos
from controllers.pagamentos.pagamento_repositorio import (
    listar_pagamentos_bd,
    inserir_pagamento_bd,
    atualizar_pagamento_bd,
    remover_pagamento_bd,
)

logger = logging.getLogger(__name__)


def validar_dados_pagamento(dados: Dict[str, Union[str, int, float]]) -> Tuple[bool, str]:
    """
    Valida os dados fornecidos para um pagamento.

    Args:
        dados (Dict[str, Union[str, int, float]]): Dicionário contendo os campos:
            - data_pagamento (str)
            - valor (float)
            - id_forma_pagamento (int)
            - id_reserva (int)

    Returns:
        Tuple[bool, str]: True se válido, False e mensagem de erro caso contrário.
    """
    if not data_valida(dados.get("data_pagamento", "")):
        return False, "Data inválida. Formato esperado: AAAA-MM-DD"

    if not valor_valido(dados.get("valor", 0)):
        return False, "Valor deve ser numérico e maior que zero."

    if not ids_validos(dados.get("id_forma_pagamento"), dados.get("id_reserva")):
        return False, "IDs de forma de pagamento ou reserva inválidos ou ausentes."

    return True, ""


def adicionar_pagamento(dados: Dict[str, str]) -> Tuple[bool, str]:
    """
    Adiciona um novo pagamento após validação dos dados.

    Args:
        dados (Dict[str, str]): Dicionário com os campos do pagamento.

    Returns:
        Tuple[bool, str]: True e mensagem de sucesso, ou False e mensagem de erro.
    """
    valido, msg = validar_dados_pagamento(dados)
    if not valido:
        return False, msg

    # Conversão para tipos corretos
    dados_convertidos = {
        "id_reserva": int(dados["id_reserva"]),
        "id_forma_pagamento": int(dados["id_forma_pagamento"]),
        "valor": float(dados["valor"]),
        "data_pagamento": dados["data_pagamento"]
    }

    if inserir_pagamento_bd(dados_convertidos):
        return True, "Pagamento adicionado com sucesso."
    return False, "Erro ao adicionar pagamento."


def editar_pagamento(dados: Dict[str, str]) -> Tuple[bool, str]:
    """
    Atualiza um pagamento existente.

    Args:
        dados (Dict[str, str]): Dicionário com os campos do pagamento, incluindo id_pagamento.

    Returns:
        Tuple[bool, str]: True e mensagem de sucesso, ou False e mensagem de erro.
    """
    if not ids_validos(dados.get("id_pagamento")):
        return False, "ID do pagamento é obrigatório e deve ser válido."

    valido, msg = validar_dados_pagamento(dados)
    if not valido:
        return False, msg

    # Conversão para tipos corretos
    dados_convertidos = {
        "id_pagamento": int(dados["id_pagamento"]),
        "id_reserva": int(dados["id_reserva"]),
        "id_forma_pagamento": int(dados["id_forma_pagamento"]),
        "valor": float(dados["valor"]),
        "data_pagamento": dados["data_pagamento"]
    }

    if atualizar_pagamento_bd(dados_convertidos):
        return True, "Pagamento atualizado com sucesso."
    return False, "Erro ao atualizar pagamento."


def excluir_pagamento(pagamento_id: int) -> bool:
    """
    Remove um pagamento pelo ID.

    Args:
        pagamento_id (int): ID do pagamento a ser removido.

    Returns:
        bool: True se removido com sucesso, False caso contrário.
    """
    if not ids_validos(pagamento_id):
        logger.warning("ID inválido para remoção de pagamento.")
        return False
    return remover_pagamento_bd(pagamento_id)


def obter_pagamentos() -> List[Dict]:
    """
    Retorna todos os pagamentos registados na base de dados.

    Returns:
        List[Dict]: Lista de pagamentos como dicionários.
    """
    return listar_pagamentos_bd()


def exportar_pagamentos_para_csv(nome_arquivo: str = "pagamentos_export.csv") -> bool:
    """
    Exporta todos os pagamentos para um ficheiro CSV.

    Args:
        nome_arquivo (str): Nome do ficheiro CSV de destino.

    Returns:
        bool: True se exportado com sucesso, False caso contrário.
    """
    pagamentos = obter_pagamentos()
    if not pagamentos:
        logger.warning("Nenhum pagamento encontrado para exportar.")
        return False
    try:
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["ID Pagamento", "ID Reserva", "ID Forma de Pagamento", "Valor (€)", "Data Pagamento"])
            for pagamento in pagamentos:
                escritor.writerow([
                    pagamento["id"],
                    pagamento["id_reserva"],
                    pagamento["id_forma_pagamento"],
                    pagamento["valor"],
                    pagamento["data_pagamento"]
                ])
        logger.info("Pagamentos exportados com sucesso para %s", nome_arquivo)
        return True
    except Exception:
        logger.exception("Erro ao exportar pagamentos para CSV.")
        return False
