"""
Módulo de serviços para gestão de clientes.

Este módulo implementa a lógica de negócio (camada de serviços),
fazendo a ponte entre a interface/controladores e o repositório
de clientes no banco de dados.

Funções principais:
- criar_cliente: valida e insere novo cliente.
- editar_cliente: atualiza dados de cliente existente.
- excluir_cliente: remove cliente pelo ID.
- listar_clientes: retorna lista de clientes cadastrados.
- procurar_cliente_por_email: busca cliente específico.
- salvar_clientes_csv: exporta dados para CSV.
"""

import logging
from typing import Tuple, List, Optional, Dict
from controllers.cliente.cliente_validacoes import validar_dados_cliente
from controllers.cliente import cliente_repositorio

logger = logging.getLogger(__name__)

# -------------------- Serviços Públicos --------------------

def criar_cliente(nome: str, email: str, telefone: str, nif: str) -> Tuple[bool, str]:
    """
    Valida e cria um novo cliente.

    Args:
        nome (str): Nome completo do cliente.
        email (str): Email único do cliente.
        telefone (str): Telefone de contato.
        nif (str): Número de identificação fiscal.

    Returns:
        Tuple[bool, str]: Sucesso da operação e mensagem explicativa.
    """
    valido, msg = validar_dados_cliente(nome, email, telefone, nif)
    if not valido:
        logger.warning("Validação falhou ao criar cliente: %s", msg)
        return False, msg

    sucesso = cliente_repositorio.adicionar_cliente(nome, email, telefone, nif)
    if sucesso:
        logger.info("Cliente '%s' adicionado com sucesso.", nome)
        return True, "Cliente adicionado com sucesso."
    logger.warning("Cliente '%s' não pôde ser adicionado (email já existente ou erro).", nome)
    return False, "Cliente não pôde ser adicionado: email já existe ou erro no BD."


def editar_cliente(id_cliente: int, nome: str, email: str, telefone: str, nif: str) -> Tuple[bool, str]:
    """
    Valida e atualiza um cliente existente.

    Args:
        id_cliente (int): ID do cliente a ser atualizado.
        nome (str): Novo nome.
        email (str): Novo email.
        telefone (str): Novo telefone.
        nif (str): Novo NIF.

    Returns:
        Tuple[bool, str]: Sucesso da operação e mensagem explicativa.
    """
    if not isinstance(id_cliente, int) or id_cliente <= 0:
        return False, "ID de cliente inválido."

    valido, msg = validar_dados_cliente(nome, email, telefone, nif)
    if not valido:
        logger.warning("Validação falhou ao editar cliente ID %s: %s", id_cliente, msg)
        return False, msg

    sucesso = cliente_repositorio.atualizar_cliente(id_cliente, nome, email, telefone, nif)
    if sucesso:
        logger.info("Cliente ID %s atualizado com sucesso.", id_cliente)
        return True, "Cliente atualizado com sucesso."
    logger.warning("Cliente ID %s não encontrado ou erro ao atualizar.", id_cliente)
    return False, "Erro ao atualizar ou cliente não encontrado."


def excluir_cliente(id_cliente: int) -> Tuple[bool, str]:
    """
    Remove um cliente existente pelo ID.

    Args:
        id_cliente (int): Identificador único do cliente.

    Returns:
        Tuple[bool, str]: Sucesso da operação e mensagem.
    """
    if not isinstance(id_cliente, int) or id_cliente <= 0:
        return False, "ID inválido para exclusão."

    sucesso = cliente_repositorio.remover_cliente(id_cliente)
    if sucesso:
        logger.info("Cliente ID %s removido com sucesso.", id_cliente)
        return True, "Cliente removido com sucesso."
    logger.warning("Erro ao remover cliente ID %s ou cliente não encontrado.", id_cliente)
    return False, "Erro ao remover cliente ou cliente não encontrado."


def listar_clientes() -> List[Dict]:
    """
    Lista todos os clientes cadastrados.

    Returns:
        List[Dict]: Lista de dicionários com dados dos clientes.
    """
    clientes = cliente_repositorio.listar_clientes()
    logger.debug("Listando %d clientes.", len(clientes))
    return clientes


def procurar_cliente_por_email(email: str) -> Optional[Dict]:
    """
    Procura cliente através do email.

    Args:
        email (str): Email do cliente.

    Returns:
        Optional[Dict]: Dados do cliente, caso encontrado.
    """
    if not isinstance(email, str) or not email.strip():
        logger.warning("Email inválido para procura")
        return None
    cliente = cliente_repositorio.buscar_cliente_por_email(email)
    if cliente:
        logger.debug("Cliente encontrado por email '%s'.", email)
    else:
        logger.debug("Nenhum cliente encontrado por email '%s'.", email)
    return cliente


def salvar_clientes_csv(caminho: str = "clientes_export.csv") -> bool:
    """
    Exporta todos os clientes para um ficheiro CSV.

    Args:
        caminho (str, optional): Caminho de saída do ficheiro CSV.
            Por defeito, "clientes_export.csv".

    Returns:
        bool: True se exportação for bem-sucedida, False caso contrário.
    """
    sucesso = cliente_repositorio.exportar_clientes_para_csv(caminho)
    if sucesso:
        logger.info("Clientes exportados com sucesso para CSV: %s", caminho)
    else:
        logger.warning("Falha ao exportar clientes para CSV: %s", caminho)
    return sucesso
