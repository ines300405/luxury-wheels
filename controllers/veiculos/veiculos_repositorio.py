"""
Módulo de acesso à base de dados para veículos.

Inclui funções CRUD, marcação de manutenção e exportação para CSV.
"""

import logging
import csv
from typing import List, Dict, Optional
from db.conexao import conectar_base_dados
from controllers.utils_bd import obter_cursor

logger = logging.getLogger(__name__)

def listar_veiculos_bd() -> List[Dict]:
    """
    Retorna todos os veículos cadastrados na base de dados.

    Returns:
        List[Dict]: Lista de dicionários contendo os veículos
    """
    sql = "SELECT * FROM Veiculos ORDER BY id"
    try:
        with obter_cursor() as cursor:
            cursor.execute(sql)
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    except Exception:
        logger.exception("Erro ao buscar veículos.")
        return []

def buscar_veiculo_por_id(veiculo_id: int) -> Optional[Dict]:
    """
    Busca um veículo pelo ID.

    Args:
        veiculo_id (int): ID do veículo

    Returns:
        Optional[Dict]: Dicionário com os dados do veículo ou None se não encontrado
    """
    sql = "SELECT * FROM Veiculos WHERE id = ?"
    try:
        with obter_cursor() as cursor:
            cursor.execute(sql, (veiculo_id,))
            resultado = cursor.fetchone()
            if resultado:
                colunas = [desc[0] for desc in cursor.description]
                return dict(zip(colunas, resultado))
            return None
    except Exception:
        logger.exception("Erro ao buscar veículo por ID.")
        return None

def inserir_veiculo_bd(dados: dict) -> Optional[int]:
    """
    Insere um novo veículo na base de dados.

    Args:
        dados (dict): Dicionário com os dados do veículo

    Returns:
        Optional[int]: ID do veículo inserido ou None em caso de erro
    """
    sql = """
    INSERT INTO Veiculos (marca, modelo, matricula, ano, km_atual,
                          data_ultima_revisao, data_proxima_revisao, categoria,
                          transmissao, tipo, lugares, imagem, diaria,
                          data_ultima_inspecao, data_proxima_inspecao, estado)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with obter_cursor(commit=True) as cur:
            cur.execute(sql, (
                dados["marca"].strip(),
                dados["modelo"].strip(),
                dados["matricula"].strip(),
                int(dados["ano"]),
                dados.get("km_atual", 0),
                dados["data_ultima_revisao"],
                dados["data_proxima_revisao"],
                dados["categoria"].strip(),
                dados["transmissao"].strip(),
                dados["tipo"].strip(),
                int(dados["lugares"]),
                dados["imagem"].strip(),
                float(dados["diaria"]),
                dados["data_ultima_inspecao"],
                dados["data_proxima_inspecao"],
                dados.get("estado", "disponível")
            ))
            return cur.lastrowid
    except Exception:
        logger.exception("Erro ao inserir veículo")
        return None

def atualizar_veiculo_bd(dados: dict) -> bool:
    """
    Atualiza os dados de um veículo existente.

    Args:
        dados (dict): Dicionário com os dados atualizados (deve conter 'id')

    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    conn = conectar_base_dados()
    cur = conn.cursor()
    try:
        sql = """
        UPDATE Veiculos
        SET marca = ?, modelo = ?, matricula = ?, ano = ?, km_atual = ?,
            data_ultima_revisao = ?, data_proxima_revisao = ?, categoria = ?,
            transmissao = ?, tipo = ?, lugares = ?, imagem = ?, diaria = ?,
            data_ultima_inspecao = ?, data_proxima_inspecao = ?, estado = ?
        WHERE id = ?
        """
        parametros = (
            dados["marca"].strip(),
            dados["modelo"].strip(),
            dados["matricula"].strip(),
            int(dados["ano"]),
            dados.get("km_atual", 0),
            dados["data_ultima_revisao"],
            dados["data_proxima_revisao"],
            dados["categoria"].strip(),
            dados["transmissao"].strip(),
            dados["tipo"].strip(),
            int(dados["lugares"]),
            dados["imagem"].strip(),
            float(dados["diaria"]),
            dados["data_ultima_inspecao"],
            dados["data_proxima_inspecao"],
            dados.get("estado", "disponível"),
            int(dados["id"])
        )

        logger.debug("UPDATE veículo ID %s com dados: %s", dados.get("id"), dados)
        cur.execute(sql, parametros)
        conn.commit()
        logger.debug("Linhas afetadas pelo UPDATE: %s", cur.rowcount)

        return cur.rowcount > 0
    except Exception as e:
        logger.error(f"Erro ao atualizar veículo: {e}")
        return False
    finally:
        conn.close()

def remover_veiculo_bd(veiculo_id: int) -> bool:
    """
    Remove um veículo pelo ID.

    Args:
        veiculo_id (int): ID do veículo a remover

    Returns:
        bool: True se removido com sucesso, False caso contrário
    """
    sql = "DELETE FROM Veiculos WHERE id=?"
    try:
        with obter_cursor(commit=True) as cursor:
            cursor.execute(sql, (veiculo_id,))
        return cursor.rowcount > 0
    except Exception:
        logger.exception("Erro ao remover veículo.")
        return False

def marcar_veiculo_manutencao_bd(veiculo_id: int) -> bool:
    """
    Marca um veículo como 'em manutenção'.

    Args:
        veiculo_id (int): ID do veículo

    Returns:
        bool: True se marcado com sucesso, False caso contrário
    """
    try:
        conexao = conectar_base_dados()
        if conexao is None:
            logger.error("Não foi possível conectar ao banco de dados.")
            return False

        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE Veiculos SET estado = 'Manutenção' WHERE id = ?",
            (veiculo_id,)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        logger.info("Veículo ID %s marcado como em manutenção.", veiculo_id)
        return True
    except Exception:
        logger.exception("Erro ao marcar manutenção para veículo ID %s.", veiculo_id)
        return False

def exportar_veiculos_para_csv(caminho: str = "veiculos_export.csv") -> bool:
    """
    Exporta todos os veículos para um ficheiro CSV.

    Args:
        caminho (str): Caminho do ficheiro CSV

    Returns:
        bool: True se exportado com sucesso, False caso contrário
    """
    lista = listar_veiculos_bd()
    if not lista:
        return False
    try:
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=lista[0].keys())
            escritor.writeheader()
            escritor.writerows(lista)
        return True
    except Exception:
        logger.exception("Erro ao exportar veículos.")
        return False
