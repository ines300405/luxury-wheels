import sqlite3
from datetime import datetime, timedelta
from tkinter import Tk, messagebox
import logging

from db.conexao import conectar_base_dados  # assume que conectar_base_dados() retorna uma conexão SQLite

logger = logging.getLogger(__name__)


def alertar_revisoes_proximas(dias_aviso: int = 5) -> None:
    """
    Verifica veículos cuja próxima revisão ocorre dentro dos próximos `dias_aviso` dias
    e exibe um alerta via messagebox caso existam veículos nessa condição.

    Args:
        dias_aviso (int): Número de dias para verificar a revisão futura. Default é 5 dias.

    Fluxo:
        1. Conecta à base de dados SQLite.
        2. Calcula a data limite com base no número de dias de aviso.
        3. Seleciona veículos cujo estado é 'disponível' e que possuem revisão dentro do período.
        4. Se houver veículos, constrói uma mensagem listando-os.
        5. Exibe um messagebox de alerta.
        6. Fecha a conexão com a base de dados.
    """
    conexao = conectar_base_dados()
    if conexao is None:
        logger.error("Falha na conexão à base de dados.")
        return

    try:
        conexao.row_factory = sqlite3.Row  # permite acesso por nome de coluna
        data_hoje = datetime.today().date()
        data_limite = data_hoje + timedelta(days=dias_aviso)

        consulta_sql = """
            SELECT id, marca, modelo, data_proxima_revisao
            FROM Veiculos
            WHERE data_proxima_revisao BETWEEN ? AND ?
              AND estado = 'disponível'
            ORDER BY data_proxima_revisao
        """

        cursor = conexao.cursor()
        cursor.execute(consulta_sql, (data_hoje.isoformat(), data_limite.isoformat()))
        veiculos_com_revisao_proxima = cursor.fetchall()

        if veiculos_com_revisao_proxima:
            linhas_veiculos = [
                f"- {veiculo['marca']} {veiculo['modelo']} (Revisão: {veiculo['data_proxima_revisao']})"
                for veiculo in veiculos_com_revisao_proxima
            ]
            mensagem_alerta = "Veículos com revisão próxima:\n" + "\n".join(linhas_veiculos)

            # Criar janela oculta para usar messagebox sem loop principal do Tkinter
            janela_raiz = Tk()
            janela_raiz.withdraw()
            messagebox.showwarning("Alerta de Revisão", mensagem_alerta, parent=janela_raiz)
            janela_raiz.destroy()

    except Exception:
        logger.exception("Erro ao verificar revisões próximas")
    finally:
        conexao.close()
