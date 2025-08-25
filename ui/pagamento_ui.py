import tkinter as tk
from tkinter import ttk, messagebox
from utils.tooltip import DicaFerramenta
from controllers.pagamentos.pagamento_servico import (
    adicionar_pagamento,
    editar_pagamento,
    excluir_pagamento,
    exportar_pagamentos_para_csv,
    obter_pagamentos
)

class AplicacaoPagamentos(ttk.Frame):
    """
    Aplicação Tkinter para gestão de pagamentos.

    Permite adicionar, atualizar, remover, listar e exportar pagamentos,
    utilizando uma interface gráfica com formulário e tabela.
    """

    def __init__(self, master: tk.Tk):
        """
        Inicializa a aplicação de pagamentos.

        Args:
            master (tk.Tk): Janela principal da aplicação.
        """
        super().__init__(master, padding=10)
        master.title("Gestão de Pagamentos")
        master.geometry("700x560")
        master.resizable(True, True)
        self.pack(fill=tk.BOTH, expand=True)

        self.campos_entrada = {}
        self._definir_estilo()
        ttk.Label(self, text="Gestão de Pagamentos", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
        self._construir_formulario()
        self._construir_botoes()
        self._construir_lista()
        self._carregar_lista()

    def _definir_estilo(self):
        """
        Define o estilo dos widgets ttk, incluindo botões e cabeçalhos da Treeview.
        """
        estilo = ttk.Style()
        estilo.configure("TButton", padding=6)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.map("Treeview", background=[("selected", "#ececec")])

    def _construir_formulario(self):
        """
        Constrói o formulário de entrada de dados dos pagamentos.
        Cria campos de ID Pagamento, ID Reserva, ID Forma de Pagamento, Valor e Data.
        """
        form_frame = ttk.LabelFrame(self, text="Dados do Pagamento", padding=10)
        form_frame.pack(fill=tk.X, pady=5)

        campos = [
            ("ID Pagamento", False),
            ("ID Reserva", True),
            ("ID Forma de Pagamento", True),
            ("Valor (€)", True),
            ("Data Pagamento", True),
        ]

        for i, (rotulo, editavel) in enumerate(campos):
            col = i % 2
            row = i // 2
            ttk.Label(form_frame, text=f"{rotulo}:").grid(row=row, column=col * 2, sticky=tk.E, padx=5, pady=4)
            entrada = ttk.Entry(form_frame, width=30)
            entrada.grid(row=row, column=col * 2 + 1, sticky=tk.W, padx=5, pady=4)

            if not editavel:
                entrada.state(["readonly"])
            else:
                DicaFerramenta(entrada, rotulo)

            self.campos_entrada[rotulo] = entrada

        for i in range(4):
            form_frame.columnconfigure(i, weight=1)

    def _construir_botoes(self):
        """
        Cria os botões de ação: Adicionar, Atualizar, Remover, Limpar e Exportar CSV.
        """
        botoes = ttk.Frame(self)
        botoes.pack(fill=tk.X, pady=5)

        ttk.Button(botoes, text="Adicionar", command=self._acao_adicionar).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Atualizar", command=self._acao_atualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Remover", command=self._acao_remover).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Limpar", command=self._limpar_formulario).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes, text="Exportar CSV", command=self._acao_exportar_csv).pack(side=tk.RIGHT, padx=5)

    def _construir_lista(self):
        """
        Constrói a tabela (Treeview) que lista todos os pagamentos registrados.
        """
        frame_lista = ttk.LabelFrame(self, text="Pagamentos Registrados", padding=5)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        colunas = ("id", "reserva", "forma", "valor", "data")
        self.arvore = ttk.Treeview(frame_lista, columns=colunas, show="headings")

        cabecalhos = {
            "id": "ID Pagamento",
            "reserva": "ID Reserva",
            "forma": "ID Forma de Pagamento",
            "valor": "Valor (€)",
            "data": "Data Pagamento"
        }

        for coluna in colunas:
            self.arvore.heading(coluna, text=cabecalhos[coluna])
            self.arvore.column(coluna, anchor=tk.CENTER, width=130)

        self.arvore.tag_configure("linha_par", background="#f2f2f2")
        self.arvore.tag_configure("linha_impar", background="#ffffff")

        scroll = ttk.Scrollbar(frame_lista, orient="vertical", command=self.arvore.yview)
        self.arvore.configure(yscroll=scroll.set)

        self.arvore.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        frame_lista.rowconfigure(0, weight=1)
        frame_lista.columnconfigure(0, weight=1)

        self.arvore.bind("<<TreeviewSelect>>", self._preencher_formulario)

    def _preencher_formulario(self, _):
        """
        Preenche o formulário com os dados do pagamento selecionado na Treeview.

        Args:
            _ : Evento da seleção (não utilizado).
        """
        selecionado = self.arvore.selection()
        if not selecionado:
            return
        valores = self.arvore.item(selecionado[0], "values")
        for i, campo in enumerate(self.campos_entrada):
            entrada = self.campos_entrada[campo]
            entrada.state(["!readonly"])
            entrada.delete(0, tk.END)
            entrada.insert(0, valores[i])
            if campo == "ID Pagamento":
                entrada.state(["readonly"])

    def _obter_dados_formulario(self):
        """
        Obtém os dados preenchidos no formulário.

        Returns:
            dict: Dicionário contendo os dados do pagamento.
        """
        return {
            "id_pagamento": self.campos_entrada["ID Pagamento"].get().strip(),
            "id_reserva": self.campos_entrada["ID Reserva"].get().strip(),
            "id_forma_pagamento": self.campos_entrada["ID Forma de Pagamento"].get().strip(),
            "valor": self.campos_entrada["Valor (€)"].get().strip(),
            "data_pagamento": self.campos_entrada["Data Pagamento"].get().strip(),
        }

    def _acao_adicionar(self):
        """
        Adiciona um novo pagamento utilizando os dados do formulário.
        Exibe mensagens de sucesso ou erro.
        """
        dados = self._obter_dados_formulario()
        sucesso, msg = adicionar_pagamento(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self._limpar_formulario()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def _acao_atualizar(self):
        """
        Atualiza um pagamento existente utilizando os dados do formulário.
        Exibe mensagens de sucesso ou erro.
        """
        dados = self._obter_dados_formulario()
        sucesso, msg = editar_pagamento(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self._limpar_formulario()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def _acao_remover(self):
        """
        Remove o pagamento selecionado na Treeview após confirmação do usuário.
        """
        id_pagamento = self.campos_entrada["ID Pagamento"].get().strip()
        if not id_pagamento.isdigit():
            messagebox.showerror("Erro", "Selecione um ID válido para remover.")
            return
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este pagamento?"):
            if excluir_pagamento(int(id_pagamento)):
                messagebox.showinfo("Sucesso", "Pagamento removido com sucesso.")
                self._limpar_formulario()
                self._carregar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao remover pagamento.")

    def _carregar_lista(self):
        """
        Carrega a lista de pagamentos na Treeview.
        """
        self.arvore.delete(*self.arvore.get_children())
        for i, pagamento in enumerate(obter_pagamentos()):
            valores = (
                pagamento["id"],
                pagamento["id_reserva"],
                pagamento["id_forma_pagamento"],
                pagamento["valor"],
                pagamento["data_pagamento"],
            )
            tag = "linha_par" if i % 2 == 0 else "linha_impar"
            self.arvore.insert("", tk.END, values=valores, tags=(tag,))

    def _limpar_formulario(self):
        """
        Limpa todos os campos do formulário e redefine o campo de ID como readonly.
        """
        for campo, entrada in self.campos_entrada.items():
            entrada.state(["!readonly"])
            entrada.delete(0, tk.END)
            if campo == "ID Pagamento":
                entrada.state(["readonly"])

    def _acao_exportar_csv(self):
        """
        Exporta os pagamentos para um arquivo CSV e exibe mensagem de sucesso ou erro.
        """
        if exportar_pagamentos_para_csv():
            messagebox.showinfo("Sucesso", "Pagamentos exportados com sucesso.")
        else:
            messagebox.showerror("Erro", "Falha ao exportar pagamentos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoPagamentos(root)
    root.mainloop()
