import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import ttk, messagebox, filedialog
from controllers.veiculos import veiculos_servico

# Caminho absoluto e robusto para a pasta photo_cars (assumindo que este ficheiro está em ui/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO_DIR = os.path.join(BASE_DIR, "photo_cars")


class AplicacaoVeiculo(ttk.Frame):
    """
    Interface gráfica para gestão de veículos da frota.

    Funcionalidades:
        - Listar veículos
        - Adicionar/editar/remover veículos
        - Marcar manutenção
        - Exportar lista de veículos para CSV
        - Visualizar imagem do veículo selecionado
    """

    def __init__(self, mestre: tk.Tk):
        """
        Inicializa a interface de gestão de veículos.

        Args:
            mestre (tk.Tk): Janela principal do Tkinter.
        """
        super().__init__(mestre, padding=10)
        mestre.title("Gestão de Veículos")
        mestre.geometry("1100x600")
        self.pack(fill=tk.BOTH, expand=True)

        self.id_selecionado = None
        self.img_atual = None  # manter referência da imagem

        # Frame da lista de veículos
        self.frame_lista = ttk.Frame(self)
        self.frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Colunas do Treeview
        self.colunas = [
            ("id", "ID"), ("marca", "Marca"), ("modelo", "Modelo"), ("matricula", "Matrícula"),
            ("ano", "Ano"), ("categoria", "Categoria"), ("transmissao", "Transmissão"),
            ("tipo", "Tipo"), ("lugares", "Lugares"),
            ("diaria", "Diária"), ("estado", "Estado")
        ]
        self.tree = ttk.Treeview(self.frame_lista, columns=[c[0] for c in self.colunas], show='headings')
        for chave, titulo in self.colunas:
            self.tree.heading(chave, text=titulo)
            self.tree.column(chave, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_selecionar_veiculo)

        # Botões de ação
        btn_frame = ttk.Frame(self.frame_lista)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Adicionar", command=self.abrir_formulario_adicionar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.abrir_formulario_editar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover_veiculo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Marcar Manutenção", command=self.marcar_manutencao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar CSV", command=self.exportar_csv).pack(side=tk.LEFT, padx=5)

        # Área para mostrar imagem do veículo selecionado
        self.label_imagem = tk.Label(self)
        self.label_imagem.pack(side=tk.RIGHT, padx=10, pady=10)

        self.formulario = None
        self.carregar_veiculos()

    def carregar_veiculos(self):
        """Carrega e exibe todos os veículos na Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        lista = veiculos_servico.obter_veiculos_servico() or []
        for veiculo in lista:
            valores = [veiculo.get(chave, "") for chave, _ in self.colunas]
            self.tree.insert("", tk.END, values=valores)

    def on_selecionar_veiculo(self, event):
        """Exibe os detalhes e a imagem do veículo selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            return
        valores = self.tree.item(selecionado[0])["values"]
        try:
            self.id_selecionado = int(valores[0])
        except (ValueError, TypeError):
            self.id_selecionado = valores[0]

        veiculos = veiculos_servico.obter_veiculos_servico() or []
        veiculo = next((v for v in veiculos if v.get("id") == self.id_selecionado or str(v.get("id")) == str(self.id_selecionado)), None)

        if veiculo and veiculo.get("imagem"):
            self.mostrar_imagem_lista(veiculo["imagem"])
        else:
            self.label_imagem.config(text="Sem imagem", image="")
            self.img_atual = None

    def _resolver_caminho_imagem(self, nome_arquivo: str) -> str:
        """Retorna o caminho absoluto para uma imagem, se existir."""
        if not nome_arquivo:
            return ""
        if os.path.isabs(nome_arquivo) and os.path.exists(nome_arquivo):
            return nome_arquivo
        caminho1 = os.path.join(PHOTO_DIR, nome_arquivo)
        if os.path.exists(caminho1):
            return caminho1
        caminho2 = os.path.join("photo_cars", nome_arquivo)
        if os.path.exists(caminho2):
            return caminho2
        return ""

    def mostrar_imagem_lista(self, nome_arquivo):
        """Mostra a imagem do veículo selecionado na interface."""
        caminho = self._resolver_caminho_imagem(nome_arquivo)
        if caminho:
            img = Image.open(caminho)
            img.thumbnail((400, 280), Image.Resampling.LANCZOS)
            self.img_atual = ImageTk.PhotoImage(img)
            self.label_imagem.config(image=self.img_atual, text="")
        else:
            self.label_imagem.config(text=f"Imagem não encontrada: {nome_arquivo}", image="")
            self.img_atual = None

    def abrir_formulario_adicionar(self):
        """Abre o formulário para adicionar um novo veículo."""
        if self.formulario:
            self.formulario.destroy()
        self.formulario = FormularioVeiculo(self, "Adicionar Veículo", self.adicionar_veiculo)
        self.formulario.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    def abrir_formulario_editar(self):
        """Abre o formulário para editar o veículo selecionado."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar.")
            return
        veiculos = veiculos_servico.obter_veiculos_servico() or []
        veiculo = next((v for v in veiculos if v.get("id") == self.id_selecionado or str(v.get("id")) == str(self.id_selecionado)), None)
        if veiculo is None:
            messagebox.showerror("Erro", "Veículo não encontrado.")
            return
        if self.formulario:
            self.formulario.destroy()
        self.formulario = FormularioVeiculo(self, "Editar Veículo", self.atualizar_veiculo, veiculo)
        self.formulario.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    def adicionar_veiculo(self, dados):
        """Adiciona um veículo usando o serviço correspondente."""
        sucesso = veiculos_servico.adicionar_veiculo_servico(**dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso.")
            self.formulario.destroy()
            self.carregar_veiculos()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar veículo.")

    def atualizar_veiculo(self, dados):
        """Atualiza um veículo usando o serviço correspondente."""
        veiculo_id = dados.pop("veiculo_id")
        sucesso = veiculos_servico.atualizar_veiculo_servico(veiculo_id=int(veiculo_id), **dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso.")
            self.formulario.destroy()
            self.carregar_veiculos()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar veículo.")

    def remover_veiculo(self):
        """Remove o veículo selecionado da base de dados."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover.")
            return
        if messagebox.askyesno("Confirmação", "Deseja remover o veículo selecionado?"):
            sucesso = veiculos_servico.remover_veiculo_servico(self.id_selecionado)
            if sucesso:
                messagebox.showinfo("Sucesso", "Veículo removido.")
                self.carregar_veiculos()
            else:
                messagebox.showerror("Erro", "Falha ao remover veículo.")

    def marcar_manutencao(self):
        """Marca o veículo selecionado como em manutenção."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um veículo para marcar manutenção.")
            return
        sucesso = veiculos_servico.marcar_veiculo_manutencao_servico(self.id_selecionado)
        if sucesso:
            messagebox.showinfo("Sucesso", "Veículo marcado em manutenção.")
            self.carregar_veiculos()
        else:
            messagebox.showerror("Erro", "Falha ao marcar manutenção.")

    def exportar_csv(self):
        """Exporta a lista de veículos para arquivo CSV."""
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Todos os ficheiros", "*.*")]
        )
        if caminho:
            sucesso = veiculos_servico.exportar_veiculos_servico(caminho)
            if sucesso:
                messagebox.showinfo("Exportação", f"Exportado para {caminho}")
            else:
                messagebox.showerror("Erro", "Falha ao exportar CSV.")


class FormularioVeiculo(ttk.Frame):
    """
    Formulário para adicionar ou editar veículos.

    Args:
        pai (ttk.Frame): Frame pai onde será inserido o formulário.
        titulo (str): Título do formulário.
        callback_salvar (callable): Função chamada ao clicar em salvar, recebendo os dados.
        veiculo (dict, opcional): Dados do veículo para edição.
    """

    def __init__(self, pai, titulo, callback_salvar, veiculo=None):
        super().__init__(pai)
        self.callback_salvar = callback_salvar
        self.veiculo = veiculo
        self.entries = {}
        self.img_atual = None  # manter referência da imagem

        ttk.Label(self, text=titulo, font=("Arial", 14, "bold")).pack(pady=10)

        campos = [
            ("Marca", "marca"), ("Modelo", "modelo"), ("Matrícula", "matricula"),
            ("Ano", "ano"), ("Categoria", "categoria"), ("Transmissão", "transmissao"),
            ("Tipo Veículo", "tipo_veiculo"), ("Lugares", "quantidade_lugares"),
            ("Imagem", "imagem"),
            ("Diária", "diaria"),
            ("Última Revisão", "data_revisao_ultima"),
            ("Próxima Revisão", "data_revisao_proxima"),
            ("Última Inspeção", "data_inspecao_ultima"),
            ("Próxima Inspeção", "data_inspecao_proxima")
        ]

        for texto, chave in campos:
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=texto, width=25).pack(side=tk.LEFT)

            ent = ttk.Entry(frame)
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[chave] = ent

            if chave == "imagem":
                self.label_preview = tk.Label(self)
                self.label_preview.pack(pady=5)

        if veiculo:
            for chave in self.entries:
                valor = veiculo.get(chave, "") if chave != "veiculo_id" else veiculo.get("id", "")
                self.entries[chave].insert(0, valor)
            img_nome = veiculo.get("imagem")
            if img_nome:
                self.mostrar_imagem(img_nome)

        ttk.Button(self, text="Salvar", command=self.salvar).pack(pady=10)

    def mostrar_imagem(self, nome_arquivo):
        """Mostra preview da imagem selecionada no formulário."""
        pasta = "photo_cars"
        caminho = os.path.join(pasta, nome_arquivo)

        if not os.path.exists(caminho):
            nome_minusculo = nome_arquivo.lower()
            for ficheiro in os.listdir(pasta):
                if ficheiro.lower() == nome_minusculo:
                    caminho = os.path.join(pasta, ficheiro)
                    break

        if os.path.exists(caminho):
            img = Image.open(caminho)
            img = img.resize((200, 150))
            self.img_atual = ImageTk.PhotoImage(img)
            self.label_preview.config(image=self.img_atual, text="")
        else:
            self.label_preview.config(text="Imagem não encontrada", image="")

    def _resolver_caminho_imagem(self, nome_arquivo: str) -> str:
        """Retorna caminho absoluto da imagem, se existir."""
        if not nome_arquivo:
            return ""
        if os.path.isabs(nome_arquivo) and os.path.exists(nome_arquivo):
            return nome_arquivo
        caminho1 = os.path.join(PHOTO_DIR, nome_arquivo)
        if os.path.exists(caminho1):
            return caminho1
        caminho2 = os.path.join("photo_cars", nome_arquivo)
        if os.path.exists(caminho2):
            return caminho2
        return ""

    def salvar(self):
        """Chama o callback de salvar com os dados do formulário."""
        dados = {chave: ent.get().strip() for chave, ent in self.entries.items()}
        if self.veiculo:
            dados["veiculo_id"] = self.veiculo.get("id")
        self.callback_salvar(dados)


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoVeiculo(root)
    root.mainloop()
