import re

def nome_forma_pagamento_valido(nome: str) -> bool:
    """
    Verifica se o nome da forma de pagamento é válido.

    Regras:
        - String não vazia
        - Mínimo 3 caracteres
        - Máximo 50 caracteres
        - Apenas letras, números e espaços

    Args:
        nome (str): Nome a validar.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if not isinstance(nome, str):
        return False
    nome = nome.strip()
    if not (3 <= len(nome) <= 50):
        return False
    return bool(re.match(r"^[A-Za-zÀ-ÿ0-9 ]+$", nome))
