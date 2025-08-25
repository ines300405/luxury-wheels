"""
Camada de serviço para a lógica de negócio dos veículos.

Valida os dados e interage com o repositório.
"""

import logging
from controllers.veiculos import veiculos_validacoes, veiculos_repositorio

logger = logging.getLogger(__name__)


# -------------------- Serviços Públicos --------------------

def obter_veiculos_servico() -> list:
    """
    Retorna todos os veículos cadastrados.

    Returns:
        list: Lista de dicionários com os veículos
    """
    return veiculos_repositorio.listar_veiculos_bd()


def adicionar_veiculo_servico(**dados) -> int | None:
    """
    Valida e insere um veículo na base de dados.

    Args:
        **dados: Campos do veículo

    Returns:
        int | None: ID do veículo inserido ou None em caso de erro
    """
    if not _validar_veiculo(dados, incluir_id=False):
        logger.error("Falha na validação ao adicionar veículo: %s", dados)
        return None

    # Define km_atual e estado padrão se não vierem
    dados.setdefault("km_atual", 0)
    dados.setdefault("estado", "disponível")
    veiculo_id = veiculos_repositorio.inserir_veiculo_bd(dados)
    logger.info("Veículo inserido com ID %s", veiculo_id)
    return veiculo_id


def atualizar_veiculo_servico(veiculo_id: int, **dados) -> bool:
    """
    Valida e atualiza um veículo existente.

    Args:
        veiculo_id (int): ID do veículo
        **dados: Campos atualizados do veículo

    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    if not veiculos_validacoes.validar_inteiro(veiculo_id, 1):
        logger.error("ID inválido para atualização.")
        return False

    dados_atualizados = dados.copy()
    dados_atualizados.setdefault("km_atual", 0)
    dados_atualizados.setdefault("estado", "disponível")
    dados_atualizados["id"] = veiculo_id

    if not _validar_veiculo(dados_atualizados, incluir_id=True):
        logger.error("Falha na validação dos dados para atualização: %s", dados_atualizados)
        return False

    return veiculos_repositorio.atualizar_veiculo_bd(dados_atualizados)


def remover_veiculo_servico(veiculo_id: int) -> bool:
    """
    Remove um veículo pelo ID.

    Args:
        veiculo_id (int): ID do veículo

    Returns:
        bool: True se removido com sucesso
    """
    if not veiculos_validacoes.validar_inteiro(veiculo_id, 1):
        return False
    return veiculos_repositorio.remover_veiculo_bd(veiculo_id)


def marcar_veiculo_manutencao_servico(veiculo_id: int) -> bool:
    """
    Marca um veículo como em manutenção.

    Args:
        veiculo_id (int): ID do veículo

    Returns:
        bool: True se marcado com sucesso
    """
    if not veiculos_validacoes.validar_inteiro(veiculo_id, 1):
        return False
    return veiculos_repositorio.marcar_veiculo_manutencao_bd(veiculo_id)


def exportar_veiculos_servico(caminho: str = "veiculos_export.csv") -> bool:
    """
    Exporta todos os veículos para um ficheiro CSV.

    Args:
        caminho (str): Caminho do ficheiro CSV

    Returns:
        bool: True se exportado com sucesso
    """
    return veiculos_repositorio.exportar_veiculos_para_csv(caminho)


# -------------------- Métodos Auxiliares --------------------

def _validar_veiculo(d: dict, incluir_id=False) -> bool:
    """
    Valida os campos do veículo.

    Args:
        d (dict): Dados do veículo
        incluir_id (bool): Se True, valida também o ID

    Returns:
        bool: True se todos os campos forem válidos
    """
    validacoes = [
        veiculos_validacoes.validar_texto(d.get("marca")),
        veiculos_validacoes.validar_texto(d.get("modelo")),
        veiculos_validacoes.validar_texto(d.get("matricula")),
        veiculos_validacoes.validar_inteiro(d.get("ano"), 1900),
        veiculos_validacoes.validar_texto(d.get("categoria")),
        veiculos_validacoes.validar_texto(d.get("transmissao")),
        veiculos_validacoes.validar_texto(d.get("tipo")),
        veiculos_validacoes.validar_inteiro(d.get("lugares"), 1),
        veiculos_validacoes.validar_texto(d.get("imagem")),
        veiculos_validacoes.validar_decimal(d.get("diaria"), 0),
        veiculos_validacoes.validar_data(d.get("data_ultima_revisao")),
        veiculos_validacoes.validar_data(d.get("data_proxima_revisao")),
        veiculos_validacoes.validar_data(d.get("data_ultima_inspecao")),
        veiculos_validacoes.validar_data(d.get("data_proxima_inspecao")),
    ]
    if incluir_id:
        validacoes.append(veiculos_validacoes.validar_inteiro(d.get("id"), 1))

    return all(validacoes)


def _preparar_valores_para_insercao(d: dict) -> tuple:
    """Prepara os valores do veículo para inserção no banco de dados."""
    return (
        d["marca"].strip(), d["modelo"].strip(), d["matricula"].strip(),
        int(d["ano"]), d.get("km_atual", 0),
        d["data_ultima_revisao"], d["data_proxima_revisao"],
        d["categoria"].strip(), d["transmissao"].strip(), d["tipo"].strip(),
        int(d["lugares"]), d["imagem"].strip(), float(d["diaria"]),
        d["data_ultima_inspecao"], d["data_proxima_inspecao"],
        "disponível"
    )


def _preparar_valores_para_atualizacao(veiculo_id: int, d: dict) -> tuple:
    """Prepara os valores do veículo para atualização no banco de dados."""
    return (
        d["marca"].strip(), d["modelo"].strip(), d["matricula"].strip(),
        int(d["ano"]), d.get("km_atual", 0),
        d["data_ultima_revisao"], d["data_proxima_revisao"],
        d["categoria"].strip(), d["transmissao"].strip(), d["tipo"].strip(),
        int(d["lugares"]), d["imagem"].strip(), float(d["diaria"]),
        d["data_ultima_inspecao"], d["data_proxima_inspecao"],
        int(veiculo_id)
    )
