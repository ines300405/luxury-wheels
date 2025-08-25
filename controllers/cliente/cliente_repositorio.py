"""
Módulo de gestão de clientes.

Este módulo fornece funções para adicionar, listar, atualizar, remover e
exportar clientes da base de dados. Também inclui a função de busca por email.

Funções principais:
- adicionar_cliente: insere novo cliente (se o email ainda não existir).
- listar_clientes: devolve lista de todos os clientes registados.
- atualizar_cliente: atualiza dados de um cliente existente.
- remover_cliente: elimina cliente da base de dados.
- buscar_cliente_por_email: pesquisa cliente pelo email.
- exportar_clientes_para_csv: exporta lista de clientes para um ficheiro CSV.
"""

import csv
import logging
from typing import List, Optional, Dict
from controllers.utils_bd import obter_cursor

logger = logging.getLogger(__name__)


def adicionar_cliente(nome: str, email: str, telefone: str, nif: str) -> bool:
    """
    Adiciona um novo cliente à base de dados se o email não existir ainda.

    Args:
        nome (str): Nome do cliente.
        email (str): Email do cliente (único).
        telefone (str): Número de telefone do cliente.
        nif (str): Número de identificação fiscal.

    Returns:
        bool: True se o cliente foi adicionado, False caso contrário.
    """
    try:
        # Verifica se o cliente com o mesmo email já existe
        existente = buscar_cliente_por_email(email)
        if existente:
            logger.warning("Cliente com email '%s' já existe (ID %s).", email, existente["id"])
            return False

        with obter_cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO Clientes (nome, email, telefone, nif) VALUES (?, ?, ?, ?)",
                (nome.strip(), email.strip(), telefone.strip(), nif.strip())
            )
        return True
    except Exception:
        logger.exception("Erro ao adicionar cliente")
        return False


def listar_clientes() -> List[Dict]:
    """
    Lista todos os clientes registados na base de dados.

    Returns:
        List[Dict]: Lista de dicionários com os dados dos clientes.
    """
    query = "SELECT id, nome, email, telefone, nif, data_registo FROM clientes ORDER BY id"
    try:
        with obter_cursor() as cursor:
            cursor.execute(query)
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]  # cada linha já é tipo dict
    except Exception as e:
        logger.exception("Erro ao listar clientes: %s", e)
        return []


def atualizar_cliente(id_cliente: int, nome: str, email: str, telefone: str, nif: str) -> bool:
    """
    Atualiza os dados de um cliente existente.

    Args:
        id_cliente (int): ID do cliente a atualizar.
        nome (str): Novo nome do cliente.
        email (str): Novo email do cliente.
        telefone (str): Novo telefone do cliente.
        nif (str): Novo número de identificação fiscal.

    Returns:
        bool: True se o cliente foi atualizado, False caso contrário.
    """
    query = """
        UPDATE clientes SET nome = ?, email = ?, telefone = ?, nif = ? WHERE id = ?
    """
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(query, (nome.strip(), email.strip(), telefone.strip(), nif.strip(), id_cliente))
            atualizado = cursor.rowcount > 0
            logger.info("Cliente ID %s atualizado: %s", id_cliente, atualizado)
            return atualizado
    except Exception as e:
        logger.exception("Erro ao atualizar cliente ID %s: %s", id_cliente, e)
        return False


def remover_cliente(id_cliente: int) -> bool:
    """
    Remove um cliente da base de dados.

    Args:
        id_cliente (int): ID do cliente a remover.

    Returns:
        bool: True se o cliente foi removido, False caso contrário.
    """
    try:
        with obter_cursor() as cursor:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
            removido = cursor.rowcount > 0
            logger.info("Cliente ID %s removido: %s", id_cliente, removido)
            return removido
    except Exception as e:
        logger.exception("Erro ao apagar cliente ID %s: %s", id_cliente, e)
        return False


def buscar_cliente_por_email(email: str) -> Optional[Dict]:
    """
    Procura um cliente pelo seu email.

    Args:
        email (str): Email do cliente a procurar.

    Returns:
        Optional[Dict]: Dicionário com os dados do cliente ou None se não encontrado.
    """
    try:
        with obter_cursor() as cur:
            cur.execute("SELECT id, nome, email, telefone, nif FROM Clientes WHERE email = ?", (email.strip(),))
            resultado = cur.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cur.description]
                return dict(zip(colunas, resultado))
            return None
    except Exception:
        logger.exception("Erro ao buscar cliente por email")
        return None


def exportar_clientes_para_csv(caminho: str = "clientes_export.csv") -> bool:
    """
    Exporta todos os clientes para um ficheiro CSV.

    Args:
        caminho (str, optional): Caminho do ficheiro CSV a gerar.
                                 Por defeito 'clientes_export.csv'.

    Returns:
        bool: True se a exportação foi realizada com sucesso, False caso contrário.
    """
    clientes = listar_clientes()
    if not clientes:
        logger.warning("Nenhum cliente para exportar")
        return False

    try:
        with open(caminho, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=["id", "nome", "email", "telefone", "nif", "data_registo"])
            escritor.writeheader()
            escritor.writerows(clientes)
        logger.info("Clientes exportados com sucesso para %s", caminho)
        return True
    except Exception as e:
        logger.exception("Erro ao exportar CSV: %s", e)
        return False
