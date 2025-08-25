import tkinter as tk
from tkinter import ttk, messagebox
from utils.tooltip import DicaFerramenta

from controllers.cliente.cliente_servico import (
    criar_cliente,
    listar_clientes,
    editar_cliente,
    excluir_cliente,
    procurar_cliente_por_email,
    salvar_clientes_csv
)


class AplicacaoClientes(tk.Frame):
    """
    Interface gráfica para gestão de clientes.

    Funcionalidades:
        - Adicionar clientes
        - Atualizar clientes existentes
        - Remover clientes
        - Listar clientes
        - Exportar clientes para CSV
    """

    def __init__(self, master=None):
        """
        Inicializa a interface gráfica de clientes.

        Args:
            master (tk.Tk, optional): Janela principal do Tkinter. Defaults to None.
        """
        super().__init__(master)
        self.master = master
        self.master.title("Gestão de Clientes")
        self.master.geometry("780x550")
        self.master.resizable(True, True)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._construir_formulario()
        self._construir_botoes()
        self._construir_lista()
        self._atualizar_lista()

    def _construir_formulario(self):
        """Constrói os campos de entrada do cliente no formulário."""
        formulario = ttk.Labelframe(self, text="Dados do Cliente")
        formulario.pack(fill=tk.X, pady=5)

        etiquetas = ["ID", "Nome", "Email", "Telefone", "NIF", "Data Registo"]
        self.campos_texto = {}

        for i, etiqueta in enumerate(etiquetas):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(row=i, column=0, sticky=tk.E, padx=5, pady=2)
            campo = ttk.Entry(formulario)
            campo.grid(row=i, column=1, sticky=tk.W + tk.E, padx=5, pady=2)

            # Campos que não podem ser editados
            if etiqueta in ("ID", "Data Registo"):
                campo.config(state="readonly")
            else:
                DicaFerramenta(campo, f"Informe o {etiqueta.lower()}")

            self.campos_texto[etiqueta.lower().replace(" ", "_")] = campo

    def _construir_botoes(self):
        """Constrói os botões de ação: adicionar, atualizar, remover, limpar e exportar CSV."""
        quadro_botoes = ttk.Frame(self)
        quadro_botoes.pack(fill=tk.X, pady=5)

        ttk.Button(quadro_botoes, text="Adicionar", command=self.adicionar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Atualizar", command=self.atualizar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Remover", command=self.remover_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Exportar CSV", command=self.exportar_clientes).pack(side=tk.RIGHT, padx=5)

    def _construir_lista(self):
        """Constrói a Treeview para exibir a lista de clientes cadastrados."""
        quadro_lista = ttk.Frame(self)
        quadro_lista.pack(fill=tk.BOTH, expand=True, pady=5)

        colunas = ("id", "nome", "email", "telefone", "nif", "data_registo")
        self.arvore = ttk.Treeview(quadro_lista, columns=colunas, show="headings", selectmode="browse")

        for coluna in colunas:
            cabecalho = coluna.replace("_", " ").capitalize()
            self.arvore.heading(coluna, text=cabecalho)
            self.arvore.column(coluna, width=120, anchor=tk.CENTER)

        barra_vertical = ttk.Scrollbar(quadro_lista, orient="vertical", command=self.arvore.yview)
        barra_horizontal = ttk.Scrollbar(quadro_lista, orient="horizontal", command=self.arvore.xview)
        self.arvore.configure(yscroll=barra_vertical.set, xscroll=barra_horizontal.set)

        self.arvore.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        quadro_lista.rowconfigure(0, weight=1)
        quadro_lista.columnconfigure(0, weight=1)

        self.arvore.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _obter_valor_campo(self, campo):
        """
        Retorna o valor atual de um campo de entrada.

        Args:
            campo (str): Nome do campo a ser lido.

        Returns:
            str: Valor atual do campo.
        """
        return self.campos_texto[campo].get().strip()

    def _definir_valor_campo(self, campo, valor):
        """
        Define o valor de um campo de entrada.

        Args:
            campo (str): Nome do campo a ser atualizado.
            valor (str): Valor a ser inserido no campo.
        """
        entrada = self.campos_texto[campo]
        entrada.config(state="normal")
        entrada.delete(0, tk.END)
        entrada.insert(0, valor or "")
        if campo in ("id", "data_registo"):
            entrada.config(state="readonly")

    def _validar_campos_geral(self, modo="insercao"):
        """
        Valida os campos antes de inserir ou atualizar um cliente.

        Args:
            modo (str): "insercao" ou "atualizacao" para validar corretamente a unicidade.

        Returns:
            bool: True se todos os campos forem válidos, False caso contrário.
        """
        nome = self._obter_valor_campo("nome")
        email = self._obter_valor_campo("email")
        telefone = self._obter_valor_campo("telefone")
        nif = self._obter_valor_campo("nif")
        id_atual = self._obter_valor_campo("id")

        if not all([nome, email, telefone, nif]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return False

        existente = procurar_cliente_por_email(email)
        if existente:
            if modo == "insercao" or (modo == "atualizacao" and str(existente["id"]) != id_atual):
                messagebox.showerror("Erro", "Email já está associado a outro cliente.")
                return False

        for cliente in listar_clientes():
            if cliente["nif"] == nif:
                if modo == "insercao" or (modo == "atualizacao" and str(cliente["id"]) != id_atual):
                    messagebox.showerror("Erro", "NIF já existe na base de dados.")
                    return False

        return True

    def adicionar_cliente(self):
        """Adiciona um novo cliente à base de dados."""
        if not self._validar_campos_geral("insercao"):
            return
        nome = self._obter_valor_campo("nome")
        email = self._obter_valor_campo("email")
        telefone = self._obter_valor_campo("telefone")
        nif = self._obter_valor_campo("nif")

        sucesso, msg = criar_cliente(nome, email, telefone, nif)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def atualizar_cliente(self):
        """Atualiza os dados do cliente selecionado."""
        id_str = self._obter_valor_campo("id")
        if not id_str:
            messagebox.showerror("Erro", "Selecione um cliente para atualizar.")
            return
        if not self._validar_campos_geral("atualizacao"):
            return

        nome = self._obter_valor_campo("nome")
        email = self._obter_valor_campo("email")
        telefone = self._obter_valor_campo("telefone")
        nif = self._obter_valor_campo("nif")

        sucesso, msg = editar_cliente(int(id_str), nome, email, telefone, nif)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self._atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def remover_cliente(self):
        """Remove o cliente selecionado da base de dados."""
        id_str = self._obter_valor_campo("id")
        if not id_str:
            messagebox.showerror("Erro", "Selecione um cliente para remover.")
            return

        if messagebox.askyesno("Confirmação", "Remover cliente?"):
            sucesso, msg = excluir_cliente(int(id_str))
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.limpar_campos()
                self._atualizar_lista()
            else:
                messagebox.showerror("Erro", msg)

    def _ao_selecionar(self, event):
        """Popula os campos do formulário ao selecionar um cliente na lista."""
        selecionado = self.arvore.selection()
        if not selecionado:
            return

        valores = self.arvore.item(selecionado[0], "values")
        campos = ("id", "nome", "email", "telefone", "nif", "data_registo")
        for campo, valor in zip(campos, valores):
            self._definir_valor_campo(campo, valor)

    def _atualizar_lista(self):
        """Atualiza a Treeview exibindo a lista atual de clientes."""
        self.arvore.delete(*self.arvore.get_children())
        clientes = listar_clientes()

        for cliente in clientes:
            self.arvore.insert("", tk.END, values=(
                str(cliente.get("id", "")),
                str(cliente.get("nome", "")),
                str(cliente.get("email", "")),
                str(cliente.get("telefone", "")),
                str(cliente.get("nif", "")),
                str(cliente.get("data_registo", ""))
            ))

    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        for campo in self.campos_texto:
            self._definir_valor_campo(campo, "")

    def exportar_clientes(self):
        """Exporta todos os clientes para um arquivo CSV."""
        sucesso = salvar_clientes_csv()
        if sucesso:
            messagebox.showinfo("Sucesso", "Exportado para clientes_export.csv")
        else:
            messagebox.showerror("Erro", "Falha ao exportar.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoClientes(root)
    root.mainloop()
