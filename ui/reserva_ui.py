import tkinter as tk
from tkinter import ttk, messagebox
from utils.tooltip import DicaFerramenta
from controllers.reservas.reservas_servico import (
    adicionar_reserva_servico,
    atualizar_reserva_servico,
    excluir_reserva_servico,
    exportar_reservas_para_csv,
    obter_reservas_servico
)
from controllers.reservas.reservas_validacoes import validar_periodo, validar_ids

FORMATO_DATA = "%Y-%m-%d"


class AplicacaoReserva(ttk.Frame):
    """
    Interface gráfica para gestão de reservas de veículos.

    Funcionalidades:
        - Adicionar reservas
        - Atualizar reservas existentes
        - Remover reservas
        - Listar reservas
        - Exportar reservas para CSV
    """

    def __init__(self, mestre: tk.Tk):
        """
        Inicializa a interface gráfica de reservas.

        Args:
            mestre (tk.Tk): Janela principal do Tkinter.
        """
        super().__init__(mestre, padding=10)
        mestre.title("🗓️ Gestão de Reservas")
        mestre.geometry("650x500")
        mestre.resizable(True, True)
        self.pack(fill=tk.BOTH, expand=True)

        self._construir_formulario()
        self._construir_botoes()
        self._construir_lista()
        self._carregar_lista()

    def _construir_formulario(self):
        """Cria os campos de entrada para dados da reserva."""
        quadro = ttk.LabelFrame(self, text="Dados da Reserva", padding=10)
        quadro.pack(fill=tk.X, pady=5)

        campos = [
            ("ID Reserva", False),
            ("ID Cliente", True),
            ("ID Veículo", True),
            ("Data Início", True),
            ("Data Fim", True),
        ]
        self.campostexto = {}
        for i, (rotulo, editavel) in enumerate(campos):
            ttk.Label(quadro, text=f"{rotulo}:").grid(row=i, column=0, sticky=tk.E, padx=5, pady=4)
            entrada = ttk.Entry(quadro, width=30)
            entrada.grid(row=i, column=1, sticky=tk.W, padx=5, pady=4)
            if not editavel:
                entrada.state(["readonly"])
            else:
                DicaFerramenta(entrada, rotulo)
            self.campostexto[rotulo] = entrada

    def _construir_botoes(self):
        """Cria os botões de ação da interface."""
        quadro_botoes = ttk.Frame(self)
        quadro_botoes.pack(fill=tk.X, pady=5)
        ttk.Button(quadro_botoes, text="Adicionar", command=self.adicionar_reserva).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Atualizar", command=self.atualizar_reserva).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Remover", command=self.remover_reserva).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Limpar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Exportar CSV", command=self.exportar_reservas).pack(side=tk.RIGHT, padx=5)

    def _construir_lista(self):
        """Cria a Treeview para exibir a lista de reservas cadastradas."""
        quadro_lista = ttk.Frame(self)
        quadro_lista.pack(fill=tk.BOTH, expand=True, pady=5)
        colunas = ("ID", "Cliente", "Veículo", "Início", "Fim")
        self.lista = ttk.Treeview(quadro_lista, columns=colunas, show="headings", selectmode="browse")
        for coluna in colunas:
            self.lista.heading(coluna, text=coluna)
            self.lista.column(coluna, width=100, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(quadro_lista, orient="vertical", command=self.lista.yview)
        self.lista.configure(yscroll=scroll.set)
        self.lista.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        quadro_lista.rowconfigure(0, weight=1)
        quadro_lista.columnconfigure(0, weight=1)
        self.lista.bind("<<TreeviewSelect>>", self._selecionar_reserva)

    def _carregar_lista(self):
        """Atualiza a Treeview exibindo todas as reservas."""
        self.lista.delete(*self.lista.get_children())
        for reserva in obter_reservas_servico():
            valores = (
                reserva["id"],
                reserva["id_cliente"],
                reserva["id_veiculo"],
                reserva["data_inicio"],
                reserva["data_fim"]
            )
            self.lista.insert("", tk.END, values=valores)

    def _selecionar_reserva(self, _):
        """Popula os campos do formulário ao selecionar uma reserva na lista."""
        selecionado = self.lista.selection()
        if not selecionado:
            return
        valores = self.lista.item(selecionado[0], "values")
        for i, campo in enumerate(["ID Reserva", "ID Cliente", "ID Veículo", "Data Início", "Data Fim"]):
            entrada = self.campostexto[campo]
            entrada.state(["!readonly"])
            entrada.delete(0, tk.END)
            entrada.insert(0, valores[i])
            if campo == "ID Reserva":
                entrada.state(["readonly"])

    def limpar_formulario(self):
        """Limpa todos os campos do formulário de reserva."""
        for campo, entrada in self.campostexto.items():
            entrada.state(["!readonly"])
            entrada.delete(0, tk.END)
            if campo == "ID Reserva":
                entrada.state(["readonly"])

    def _validar_campos_reserva(self, incluir_id=False) -> dict | None:
        """
        Valida os dados informados no formulário de reserva.

        Args:
            incluir_id (bool): Se True, inclui o ID da reserva na validação.

        Returns:
            dict | None: Dicionário com dados da reserva válidos ou None se houver erro.
        """
        try:
            cliente_id = int(self.campostexto["ID Cliente"].get())
            veiculo_id = int(self.campostexto["ID Veículo"].get())
            data_inicio = self.campostexto["Data Início"].get().strip()
            data_fim = self.campostexto["Data Fim"].get().strip()
        except ValueError:
            messagebox.showerror("Erro", "Todos os campos numéricos devem conter valores válidos.")
            return None

        if not data_inicio or not data_fim:
            messagebox.showwarning("Aviso", "Preencha as datas de início e fim.")
            return None

        if not validar_periodo(data_inicio, data_fim):
            messagebox.showerror("Erro", "As datas estão inválidas ou fora de ordem.")
            return None

        ids_para_validar = (cliente_id, veiculo_id)
        reserva_id = None
        if incluir_id:
            reserva_id = int(self.campostexto["ID Reserva"].get())
            ids_para_validar = (reserva_id, cliente_id, veiculo_id)

        if not validar_ids(*ids_para_validar):
            messagebox.showerror("Erro", "IDs devem ser inteiros positivos.")
            return None

        return {
            "reserva_id": reserva_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "status": "Reservado",
            "valor_total": 0.0
        }

    def adicionar_reserva(self):
        """Adiciona uma nova reserva à base de dados."""
        dados = self._validar_campos_reserva()
        if not dados:
            return

        reservas = obter_reservas_servico()
        ids_existentes = [r["id"] for r in reservas if r.get("id")]
        novo_id = 1
        while novo_id in ids_existentes:
            novo_id += 1
        dados["reserva_id"] = novo_id

        if adicionar_reserva_servico(
            cliente_id=dados["cliente_id"],
            veiculo_id=dados["veiculo_id"],
            data_inicio=dados["data_inicio"],
            data_fim=dados["data_fim"],
            status=dados["status"],
            valor_total=dados["valor_total"]
        ):
            messagebox.showinfo("Sucesso", f"Reserva adicionada com sucesso (ID {novo_id}).")
            self.limpar_formulario()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar a reserva.")

    def atualizar_reserva(self):
        """Atualiza uma reserva existente."""
        dados = self._validar_campos_reserva(incluir_id=True)
        if not dados:
            return
        sucesso = atualizar_reserva_servico(
            reserva_id=dados["reserva_id"],
            data_inicio=dados["data_inicio"],
            data_fim=dados["data_fim"],
            cliente_id=dados["cliente_id"],
            veiculo_id=dados["veiculo_id"],
            status=dados["status"],
            valor_total=dados["valor_total"]
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "Reserva atualizada com sucesso.")
            self.limpar_formulario()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar a reserva.")

    def remover_reserva(self):
        """Remove a reserva selecionada da base de dados."""
        id_reserva = self.campostexto["ID Reserva"].get()
        if not id_reserva or not id_reserva.isdigit():
            messagebox.showerror("Erro", "Selecione uma reserva válida para remover.")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta reserva?"):
            if excluir_reserva_servico(int(id_reserva)):
                messagebox.showinfo("Sucesso", "Reserva removida com sucesso.")
                self.limpar_formulario()
                self._carregar_lista()
            else:
                messagebox.showerror("Erro", "Falha ao remover a reserva.")

    def exportar_reservas(self):
        """Exporta todas as reservas para um arquivo CSV."""
        if exportar_reservas_para_csv():
            messagebox.showinfo("Sucesso", "Reservas exportadas com sucesso.")
        else:
            messagebox.showerror("Erro", "Falha ao exportar as reservas.")


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoReserva(raiz)
    raiz.mainloop()
