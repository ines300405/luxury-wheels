"""
Módulo de validações dos dados dos clientes.

Contém funções para verificar se os campos fornecidos pelo utilizador
(nome, email, telefone, NIF) obedecem aos padrões definidos.

Funções principais:
- nome_valido: valida nomes (mínimo 3 caracteres, apenas letras e espaços).
- email_valido: valida formato de email.
- nif_valido: valida NIF com 9 dígitos.
- telefone_valido: valida telefone (números e símbolos + - ( )).
- validar_dados_cliente: executa todas as validações em conjunto.
"""

import re
from typing import Tuple

# -------------------- Padrões de validação --------------------
PADRAO_EMAIL = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PADRAO_NIF = re.compile(r"^\d{9}$")
PADRAO_TELEFONE = re.compile(r"^[\d\s\+\-\(\)]{6,20}$")
PADRAO_NOME = re.compile(r"^[A-Za-zÀ-ÿ\s]{3,}$")

# -------------------- Funções de Validação --------------------

def nome_valido(nome: str) -> Tuple[bool, str]:
    """
    Verifica se o nome é válido.

    Args:
        nome (str): Nome do cliente.

    Returns:
        Tuple[bool, str]:
            - True, "" se for válido.
            - False, mensagem de erro caso contrário.
    """
    if not nome or not nome.strip():
        return False, "Nome é obrigatório."
    if not PADRAO_NOME.match(nome.strip()):
        return False, "Nome inválido: use letras e espaços, mínimo 3 caracteres."
    return True, ""


def email_valido(email: str) -> Tuple[bool, str]:
    """
    Verifica se o email é válido.

    Args:
        email (str): Endereço de email.

    Returns:
        Tuple[bool, str]:
            - True, "" se for válido.
            - False, mensagem de erro caso contrário.
    """
    if not email or not email.strip():
        return False, "Email é obrigatório."
    if not PADRAO_EMAIL.match(email.strip()):
        return False, "Email inválido."
    return True, ""


def nif_valido(nif: str) -> Tuple[bool, str]:
    """
    Verifica se o NIF (Número de Identificação Fiscal) é válido.

    Args:
        nif (str): Número do NIF.

    Returns:
        Tuple[bool, str]:
            - True, "" se for válido.
            - False, mensagem de erro caso contrário.
    """
    if not nif or not nif.strip():
        return False, "NIF é obrigatório."
    if not PADRAO_NIF.match(nif.strip()):
        return False, "NIF deve conter exatamente 9 dígitos numéricos."
    return True, ""


def telefone_valido(telefone: str) -> Tuple[bool, str]:
    """
    Verifica se o telefone é válido.

    Args:
        telefone (str): Número de telefone.

    Returns:
        Tuple[bool, str]:
            - True, "" se for válido.
            - False, mensagem de erro caso contrário.
    """
    if not telefone or not telefone.strip():
        return False, "Telefone é obrigatório."
    if not PADRAO_TELEFONE.match(telefone.strip()):
        return False, "Telefone inválido. Use números e caracteres + - ( )"
    return True, ""


def validar_dados_cliente(nome: str, email: str, telefone: str, nif: str) -> Tuple[bool, str]:
    """
    Executa a validação completa dos dados do cliente.

    Args:
        nome (str): Nome do cliente.
        email (str): Email único do cliente.
        telefone (str): Número de telefone.
        nif (str): Número de Identificação Fiscal.

    Returns:
        Tuple[bool, str]:
            - True, "" se todos os campos forem válidos.
            - False, mensagem de erro do primeiro campo inválido.
    """
    for func in (nome_valido, email_valido, telefone_valido, nif_valido):
        valido, msg = func(locals()[func.__name__.split('_')[0]])
        if not valido:
            return False, msg
    return True, ""
