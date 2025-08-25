"""
Camada de serviço para a lógica de negócio das reservas.

Valida os dados antes de interagir com o repositório e fornece funções
para adicionar, atualizar, remover, listar e exportar reservas.
"""

import logging
import csv
from controllers.reservas.reservas_validacoes import validar_periodo, validar_valor, validar_status, validar_ids
from controllers.reservas.reservas_repositorio import (
    inserir_reserva_bd,
    atualizar_reserva_bd,
    remover_reserva_bd,
    listar_reservas_bd
)

logger = logging.getLogger(__name__)

def adicionar_reserva_servico(data_inicio: str, data_fim: str, cliente_id: int,
                              veiculo_id: int, status: str, valor_total: float) -> bool:
    """
    Adiciona uma nova reserva após validação dos dados.

    Args:
        data_inicio (str): Data de início da reserva (formato AAAA-MM-DD)
        data_fim (str): Data de fim da reserva (formato AAAA-MM-DD)
        cliente_id (int): ID do cliente
        veiculo_id (int): ID do veículo
        status (str): Estado da reserva (ex: "Confirmada", "Pendente")
        valor_total (float): Valor total da reserva

    Returns:
        bool: True se a reserva foi adicionada com sucesso, False caso contrário
    """
    if not (validar_ids(cliente_id, veiculo_id) and validar_periodo(data_inicio, data_fim)
            and validar_status(status) and validar_valor(valor_total)):
        return False

    dados = {
        "id_cliente": cliente_id,
        "id_veiculo": veiculo_id,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "estado": status.strip(),
        "valor_total": valor_total
    }

    novo_id = inserir_reserva_bd(dados)
    return novo_id is not None

def obter_reservas_servico() -> list[dict]:
    """
    Retorna todas as reservas existentes.

    Returns:
        List[Dict]: Lista de dicionários representando cada reserva
    """
    return listar_reservas_bd()

def atualizar_reserva_servico(reserva_id: int, data_inicio: str, data_fim: str,
                              cliente_id: int, veiculo_id: int, status: str, valor_total: float) -> bool:
    """
    Atualiza uma reserva existente após validação dos dados.

    Args:
        reserva_id (int): ID da reserva
        data_inicio (str): Data de início da reserva
        data_fim (str): Data de fim da reserva
        cliente_id (int): ID do cliente
        veiculo_id (int): ID do veículo
        status (str): Estado da reserva
        valor_total (float): Valor total

    Returns:
        bool: True se a atualização ocorreu com sucesso, False caso contrário
    """
    if not (validar_ids(reserva_id, cliente_id, veiculo_id) and validar_periodo(data_inicio, data_fim)
            and validar_status(status) and validar_valor(valor_total)):
        return False

    dados = {
        "id": reserva_id,
        "id_cliente": cliente_id,
        "id_veiculo": veiculo_id,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "estado": status.strip(),
        "valor_total": valor_total
    }

    return atualizar_reserva_bd(dados)

def excluir_reserva_servico(reserva_id: int) -> bool:
    """
    Remove uma reserva pelo ID após validação.

    Args:
        reserva_id (int): ID da reserva a ser removida

    Returns:
        bool: True se a exclusão ocorreu com sucesso, False caso contrário
    """
    if not validar_ids(reserva_id):
        return False
    return remover_reserva_bd(reserva_id)

def exportar_reservas_para_csv(nome_arquivo: str = "reservas_export.csv") -> bool:
    """
    Exporta todas as reservas para um arquivo CSV.

    Args:
        nome_arquivo (str): Nome do arquivo de destino (default: "reservas_export.csv")

    Returns:
        bool: True se a exportação foi concluída com sucesso, False caso contrário
    """
    reservas = listar_reservas_bd()
    if not reservas:
        logger.warning("Nenhuma reserva para exportar")
        return False
    try:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Cliente", "Veículo", "Data Início", "Data Fim", "Estado", "Valor Total"])
            for r in reservas:
                writer.writerow([r["id"], r["id_cliente"], r["id_veiculo"],
                                 r["data_inicio"], r["data_fim"], r["estado"], r["valor_total"]])
        logger.info("Exportação concluída para %s", nome_arquivo)
        return True
    except Exception:
        logger.exception("Erro ao exportar reservas.")
        return False
