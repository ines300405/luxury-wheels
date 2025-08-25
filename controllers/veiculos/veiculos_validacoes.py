from datetime import datetime


def validar_texto(texto: str, minimo: int = 1) -> bool:
    """
    Verifica se o valor fornecido é uma string não vazia com tamanho mínimo.

    Parâmetros:
        texto (str): O texto a validar.
        minimo (int): O comprimento mínimo do texto (padrão=1).

    Retorna:
        bool: True se for texto válido, False caso contrário.
    """
    return isinstance(texto, str) and len(texto.strip()) >= minimo


def validar_inteiro(valor, minimo: int = 0) -> bool:
    """
    Valida se o valor fornecido é um número inteiro maior ou igual a um mínimo.

    Parâmetros:
        valor: O valor a validar (pode ser int, str, etc.).
        minimo (int): Valor mínimo permitido (padrão=0).

    Retorna:
        bool: True se for inteiro ≥ mínimo, False caso contrário.
    """
    try:
        return int(valor) >= minimo
    except (ValueError, TypeError):
        return False


def validar_decimal(valor, minimo: float = 0.0) -> bool:
    """
    Valida se o valor fornecido é um número decimal maior ou igual a um mínimo.

    Parâmetros:
        valor: O valor a validar (pode ser float, int, str, etc.).
        minimo (float): Valor mínimo permitido (padrão=0.0).

    Retorna:
        bool: True se for decimal ≥ mínimo, False caso contrário.
    """
    try:
        return float(valor) >= minimo
    except (ValueError, TypeError):
        return False


def validar_data(data_str: str, formato: str = "%Y-%m-%d") -> bool:
    """
    Valida se a string fornecida representa uma data válida no formato especificado.

    Parâmetros:
        data_str (str): A data em formato de string.
        formato (str): O formato esperado da data (padrão="%Y-%m-%d").

    Retorna:
        bool: True se a data for válida no formato especificado, False caso contrário.
    """
    try:
        datetime.strptime(data_str, formato)
        return True
    except (ValueError, TypeError):
        return False
