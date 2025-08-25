import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from utils.tooltip import DicaFerramenta
from controllers.formas_pagamento.formas_pag_servico import (
    adicionar_forma_pagamento,
    editar_forma_pagamento,
    excluir_forma_pagamento,
    exportar_formas_pagamento_para_csv,
    obter_formas_pagamento
)


class AplicacaoFormasPagamento(ttk.Frame):
    """
    Interface gráfica para gestão de formas de pagamento.

    Permite adicionar, atualizar, remover, listar e exportar formas de pagamento
    utilizando uma interface com formulário, botões de ação e uma tabela (Treeview).
    """
    TAMANHO_MIN_NOME = 3

    def __init__(self, mestre: Optional[tk.Tk] = None):
        """
        Inicializa a aplicação de formas de pagamento.

        Args:
            mestre (Optional[tk.Tk]): Janela principal da aplicação.
        """
        super().__init__(mestre, padding=10)
        if mestre is not None:
            mestre.title("Gestão de Formas de Pagamento")
            mestre.geometry("400x350")
            mestre.resizable(True, True)

        self.pack(fill=tk.BOTH, expand=True)
        self._construir_formulario()
        self._construir_botoes()
        self._construir_lista()
        self._carregar_lista()

    def _construir_formulario(self) -> None:
        """
        Cria o formulário de entrada com os campos ID e Nome da forma de pagamento.
        O campo ID é readonly e o campo Nome possui tooltip com instrução de mínimo de caracteres.
        """
        formulario = ttk.Labelframe(self, text="Dados da Forma de Pagamento", padding=10)
        formulario.pack(fill=tk.X, pady=5)

        etiquetas = [("ID", False), ("Nome", True)]
        self.campos = {}

        for i, (texto_etiqueta, editavel) in enumerate(etiquetas):
            ttk.Label(formulario, text=f"{texto_etiqueta}:").grid(row=i, column=0, sticky=tk.E, padx=5, pady=2)
            entrada = ttk.Entry(formulario, width=40)
            entrada.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)

            if not editavel:
                entrada.state(["readonly"])
            else:
                DicaFerramenta(entrada, f"{texto_etiqueta}: mínimo {self.TAMANHO_MIN_NOME} caracteres")

            self.campos[texto_etiqueta.lower()] = entrada

    def _construir_botoes(self) -> None:
        """
        Cria os botões de ação da aplicação: Adicionar, Atualizar, Remover, Limpar e Exportar CSV.
        """
        quadro_botoes = ttk.Frame(self)
        quadro_botoes.pack(fill=tk.X, pady=5)

        ttk.Button(quadro_botoes, text="Adicionar", command=self.adicionar).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Atualizar", command=self.atualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Remover", command=self.remover).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Limpar", command=self.limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(quadro_botoes, text="Exportar CSV", command=self.exportar).pack(side=tk.RIGHT, padx=5)

    def _construir_lista(self) -> None:
        """
        Cria a Treeview para exibir todas as formas de pagamento cadastradas,
        com barra de scroll e evento de seleção.
        """
        quadro_lista = ttk.Frame(self)
        quadro_lista.pack(fill=tk.BOTH, expand=True, pady=5)

        colunas = ("id", "nome")
        self.arvore = ttk.Treeview(quadro_lista, columns=colunas, show="headings", selectmode="browse")
        self.arvore.heading("id", text="ID")
        self.arvore.column("id", width=50, anchor=tk.CENTER)
        self.arvore.heading("nome", text="Nome")
        self.arvore.column("nome", width=300, anchor=tk.CENTER)

        barra_scroll = ttk.Scrollbar(quadro_lista, orient=tk.VERTICAL, command=self.arvore.yview)
        self.arvore.configure(yscroll=barra_scroll.set)
        self.arvore.grid(row=0, column=0, sticky="nsew")
        barra_scroll.grid(row=0, column=1, sticky="ns")

        quadro_lista.rowconfigure(0, weight=1)
        quadro_lista.columnconfigure(0, weight=1)
        self.arvore.bind("<<TreeviewSelect>>", self._ao_selecionar)

    # ------------------------ Manipulação de Campos ------------------------
    def _obter_valor(self, campo: str) -> str:
        """
        Retorna o valor do campo informado.

        Args:
            campo (str): Nome do campo ('id' ou 'nome').

        Returns:
            str: Valor atual do campo.
        """
        return self.campos[campo].get().strip()

    def _definir_valor(self, campo: str, valor: str) -> None:
        """
        Define o valor de um campo. O campo 'id' permanece readonly.

        Args:
            campo (str): Nome do campo ('id' ou 'nome').
            valor (str): Valor a ser definido no campo.
        """
        entrada = self.campos[campo]
        if campo == "id":
            entrada.state(["!readonly"])
            entrada.delete(0, tk.END)
            entrada.insert(0, valor or "")
            entrada.state(["readonly"])
        else:
            entrada.delete(0, tk.END)
            entrada.insert(0, valor or "")

    # ------------------------ Validação ------------------------
    def _validar(self) -> bool:
        """
        Valida o campo 'nome' e verifica se já existe registro com o mesmo nome.

        Returns:
            bool: True se os dados forem válidos, False caso contrário.
        """
        nome = self._obter_valor("nome")
        if len(nome) < self.TAMANHO_MIN_NOME:
            messagebox.showerror("Erro", f"Nome deve ter pelo menos {self.TAMANHO_MIN_NOME} caracteres.")
            return False

        formas_existentes = obter_formas_pagamento()
        id_atual = self._obter_valor("id")
        nome_atual = nome.lower()

        for fp in formas_existentes:
            id_fp, nome_fp = (fp["id"], fp["metodo"]) if isinstance(fp, dict) else fp
            if nome_fp.lower() == nome_atual and (not id_atual or int(id_atual) != id_fp):
                messagebox.showerror("Erro", "Nome já está registado.")
                return False

        return True

    # ------------------------ Ações ------------------------
    def adicionar(self) -> None:
        """
        Adiciona uma nova forma de pagamento após validação.
        Exibe mensagens de sucesso ou erro.
        """
        if not self._validar():
            return
        nome = self._obter_valor("nome")
        if adicionar_forma_pagamento(nome):
            messagebox.showinfo("Sucesso", "Forma de pagamento adicionada.")
            self.limpar()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao adicionar. Verifique o nome informado.")

    def atualizar(self) -> None:
        """
        Atualiza a forma de pagamento selecionada após validação.
        Exibe mensagens de sucesso ou erro.
        """
        if not self._validar():
            return
        id_str = self._obter_valor("id")
        if not id_str:
            messagebox.showerror("Erro", "Selecione uma forma para atualizar.")
            return
        nome = self._obter_valor("nome")
        if editar_forma_pagamento(int(id_str), nome):
            messagebox.showinfo("Sucesso", "Forma de pagamento atualizada.")
            self.limpar()
            self._carregar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar. Verifique o nome informado.")

    def remover(self) -> None:
        """
        Remove a forma de pagamento selecionada após confirmação do usuário.
        """
        id_str = self._obter_valor("id")
        if not id_str:
            messagebox.showerror("Erro", "Selecione uma forma para remover.")
            return
        if messagebox.askyesno("Confirmar", "Remover esta forma de pagamento?"):
            if excluir_forma_pagamento(int(id_str)):
                messagebox.showinfo("Sucesso", "Forma de pagamento removida.")
                self.limpar()
                self._carregar_lista()
            else:
                messagebox.showerror("Erro", "Falha ao remover forma de pagamento.")

    # ------------------------ Seleção e Listagem ------------------------
    def _ao_selecionar(self, _evento: tk.Event) -> None:
        """
        Preenche os campos do formulário com os dados selecionados na Treeview.

        Args:
            _evento (tk.Event): Evento de seleção (não utilizado diretamente).
        """
        selecionados = self.arvore.selection()
        if selecionados:
            valores = self.arvore.item(selecionados[0], "values")
            self._definir_valor("id", valores[0])
            self._definir_valor("nome", valores[1])

    def _carregar_lista(self) -> None:
        """
        Atualiza a Treeview com todas as formas de pagamento registradas.
        """
        for item in self.arvore.get_children():
            self.arvore.delete(item)
        for linha in obter_formas_pagamento():
            if isinstance(linha, dict):
                self.arvore.insert("", tk.END, values=(linha["id"], linha["metodo"]))
            else:
                self.arvore.insert("", tk.END, values=linha)

    # ------------------------ Limpar e Exportar ------------------------
    def limpar(self) -> None:
        """
        Limpa todos os campos do formulário.
        """
        for campo in self.campos:
            self._definir_valor(campo, "")

    def exportar(self) -> None:
        """
        Exporta as formas de pagamento para CSV.
        Exibe mensagem de sucesso ou erro.
        """
        if exportar_formas_pagamento_para_csv():
            messagebox.showinfo("Sucesso", "Exportado para CSV com sucesso.")
        else:
            messagebox.showerror("Erro", "Falha ao exportar CSV.")


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoFormasPagamento(raiz)
    raiz.mainloop()
