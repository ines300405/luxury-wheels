import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controllers.cliente.cliente_servico import listar_clientes
from controllers.veiculos.veiculos_servico import obter_veiculos_servico
from controllers.reservas.reservas_servico import obter_reservas_servico
from controllers.pagamentos.pagamento_servico import obter_pagamentos
from controllers.dashboard.dashboard_servico import obter_reservas_agrupadas_por_mes


class AplicacaoDashboard(ttk.Frame):
    """
    Interface gráfica do Dashboard da Luxury Wheels.

    Exibe indicadores-chave da frota e reservas:
        - Total de clientes
        - Veículos disponíveis
        - Reservas ativas
        - Receita total
    Além de um gráfico de barras mostrando reservas agrupadas por mês.
    """

    def __init__(self, mestre: tk.Tk):
        """
        Inicializa a interface do dashboard.

        Args:
            mestre (tk.Tk): Janela principal do Tkinter.
        """
        super().__init__(mestre, padding=10)
        mestre.title("Dashboard - Luxury Wheels")
        mestre.geometry("800x500")
        mestre.columnconfigure(0, weight=1)
        mestre.rowconfigure(1, weight=1)

        self._etiqueta_erro: ttk.Label | None = None

        self._criar_widgets()
        self._dispor_widgets()
        self._inicializar_grafico()
        self.atualizar()

    def _criar_widgets(self) -> None:
        """Cria widgets do dashboard: indicadores, botão de atualização e gráfico."""
        self.quadro_indicadores = ttk.Frame(self)
        self.etq_clientes = ttk.Label(
            self.quadro_indicadores, text="Clientes: —", anchor="center", font=("Segoe UI", 10, "bold")
        )
        self.etq_veiculos = ttk.Label(
            self.quadro_indicadores, text="Veículos Disp.: —", anchor="center", font=("Segoe UI", 10, "bold")
        )
        self.etq_reservas = ttk.Label(
            self.quadro_indicadores, text="Reservas Ativas: —", anchor="center", font=("Segoe UI", 10, "bold")
        )
        self.etq_receita = ttk.Label(
            self.quadro_indicadores, text="Receita Total: —", anchor="center", font=("Segoe UI", 10, "bold")
        )
        self.btn_atualizar = ttk.Button(self.quadro_indicadores, text="Atualizar", command=self.atualizar)

        self.quadro_grafico = ttk.Frame(self)
        self.figura = plt.Figure(figsize=(6, 3), tight_layout=True)
        self.eixo = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.quadro_grafico)

    def _dispor_widgets(self) -> None:
        """Organiza os widgets na interface usando o layout grid."""
        self.quadro_indicadores.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        for idx, widget in enumerate((
            self.etq_clientes,
            self.etq_veiculos,
            self.etq_reservas,
            self.etq_receita,
            self.btn_atualizar
        )):
            widget.grid(row=0, column=idx, padx=5, sticky="nsew")
            self.quadro_indicadores.columnconfigure(idx, weight=1)

        self.quadro_grafico.grid(row=1, column=0, sticky="nsew")
        self.quadro_grafico.rowconfigure(0, weight=1)
        self.quadro_grafico.columnconfigure(0, weight=1)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.grid(sticky="nsew")

    def _inicializar_grafico(self) -> None:
        """Configura os eixos, título e labels do gráfico de reservas por mês."""
        self.eixo.set_title("Reservas por Mês")
        self.eixo.set_xlabel("Mês")
        self.eixo.set_ylabel("Total de Reservas")
        self.eixo.tick_params(axis="x", rotation=45)

    def _atualizar_grafico(self) -> None:
        """Atualiza o gráfico de barras com os dados de reservas agrupadas por mês."""
        dados = obter_reservas_agrupadas_por_mes()
        if dados:
            meses = [str(d["mes"]) for d in dados]
            totais = [d["total"] for d in dados]
        else:
            meses, totais = [], []

        self.eixo.clear()
        self._inicializar_grafico()
        self.eixo.bar(meses, totais, color="skyblue")
        self.canvas.draw()

    def atualizar(self) -> None:
        """
        Atualiza todos os indicadores do dashboard e o gráfico.

        Captura possíveis exceções e exibe mensagem de erro na interface.
        """
        if self._etiqueta_erro:
            self._etiqueta_erro.destroy()
            self._etiqueta_erro = None

        try:
            # Total de clientes
            total_clientes = len(listar_clientes())

            # Total de veículos disponíveis
            veiculos = obter_veiculos_servico()
            total_veiculos = len([v for v in veiculos if v.get("estado") == "disponível"])

            # Total de reservas ativas
            reservas = obter_reservas_servico()
            total_reservas = len([r for r in reservas if r.get("estado") in ("Confirmada", "Pendente")])

            # Receita total
            pagamentos = obter_pagamentos()
            receita_total = sum(float(p.get("valor", 0.0)) for p in pagamentos) if pagamentos else 0.0

            # Atualizar labels
            self.etq_clientes.config(text=f"Clientes: {total_clientes}")
            self.etq_veiculos.config(text=f"Veículos Disp.: {total_veiculos}")
            self.etq_reservas.config(text=f"Reservas Ativas: {total_reservas}")
            self.etq_receita.config(text=f"Receita Total: € {receita_total:,.2f}")

            # Atualizar gráfico
            self._atualizar_grafico()

        except Exception as e:
            import traceback
            traceback.print_exc()
            self._etiqueta_erro = ttk.Label(
                self, text=f"Erro ao atualizar dashboard: {e}", foreground="red"
            )
            self._etiqueta_erro.grid(row=2, column=0, pady=10)


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoDashboard(raiz)
    raiz.mainloop()
