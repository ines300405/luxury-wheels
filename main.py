import tkinter as tk
from tkinter import messagebox, Toplevel, ttk

from ui.cliente_ui import AplicacaoClientes
from ui.veiculo_ui import AplicacaoVeiculo
from ui.reserva_ui import AplicacaoReserva
from ui.forma_pagamento_ui import AplicacaoFormasPagamento
from ui.pagamento_ui import AplicacaoPagamentos
from ui.dashboard_ui import AplicacaoDashboard
from utils.alerta import alertar_revisoes_proximas


class AplicacaoPrincipal(ttk.Frame):
    """
    Interface principal da aplicação Luxury Wheels.

    Esta classe gerencia o menu principal da aplicação, permitindo a navegação
    entre diferentes módulos (clientes, veículos, reservas, pagamentos, formas
    de pagamento e dashboard) através de botões.

    Funcionalidades principais:
    - Exibir cabeçalho e botões de navegação.
    - Abrir cada módulo em uma nova janela separada (Toplevel).
    - Evitar abrir múltiplas janelas do mesmo módulo.
    - Estilo consistente dos botões e cabeçalho.
    - Botão para sair da aplicação com confirmação.
    - Exibir alerta de revisões de veículos próximas no início.
    """

    BOTOES_NAVEGACAO = [
        ("Gestão de Clientes", AplicacaoClientes, "Clientes"),
        ("Gestão de Veículos", AplicacaoVeiculo, "Veiculos"),
        ("Gestão de Reservas", AplicacaoReserva, "Reservas"),
        ("Formas de Pagamento", AplicacaoFormasPagamento, "FormasPagamento"),
        ("Gestão de Pagamentos", AplicacaoPagamentos, "Pagamentos"),
        ("Dashboard", AplicacaoDashboard, "Dashboard"),
    ]

    def __init__(self, mestre: tk.Widget):
        """
        Inicializa a interface principal.

        Args:
            mestre (tk.Widget): Janela pai (normalmente Tk root) onde o frame principal será exibido.

        Comportamento:
        - Configura estilos de widgets (labels, botões).
        - Constrói interface com cabeçalho, botões de navegação e botão de sair.
        - Agenda exibição de alerta de revisões próximas.
        """
        super().__init__(mestre, padding=20)
        self.mestre = mestre
        self.janelas_ativas = {}

        self._configurar_estilos()
        self._construir_interface()

        # Mensagem de boas-vindas e alerta de revisões
        self.after(100, lambda: messagebox.showinfo("Bem-vindo", "Bem-vindo ao Luxury Wheels!"))
        self.after(200, alertar_revisoes_proximas)
        self.pack(fill="both", expand=True)

    def _configurar_estilos(self):
        """
        Define os estilos (ttk.Style) para labels e botões da aplicação.

        Estilos definidos:
        - Cabecalho.TLabel: fonte, cor e background do cabeçalho.
        - Navegacao.TButton: estilo padrão dos botões de navegação.
        - Sair.TButton: estilo do botão de sair.
        """
        estilo = ttk.Style()
        estilo.theme_use('clam')

        estilo.configure(
            "Cabecalho.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#333333",
            background="#f0f0f0"
        )

        estilo.configure(
            "Navegacao.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
        )
        estilo.map(
            "Navegacao.TButton",
            background=[("!active", "#1e90ff"), ("active", "#104e8b")],
            foreground=[("!active", "white"), ("active", "white")],
        )

        estilo.configure(
            "Sair.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=8,
            foreground="white",
        )
        estilo.map(
            "Sair.TButton",
            background=[("!active", "#d32f2f"), ("active", "#b71c1c")],
            foreground=[("!active", "white"), ("active", "white")],
        )

    def _construir_interface(self):
        """
        Constrói a interface visual do menu principal.

        Componentes:
        - Label de cabeçalho "Menu Principal".
        - Botões de navegação para cada módulo.
        - Botão de sair da aplicação.
        """
        rotulo_cabecalho = ttk.Label(self, text="Menu Principal", style="Cabecalho.TLabel")
        rotulo_cabecalho.pack(pady=(0, 20))

        quadro_navegacao = ttk.Frame(self, padding=(0, 10))
        quadro_navegacao.pack(fill="x")

        for texto_botao, ClasseApp, chave_janela in self.BOTOES_NAVEGACAO:
            botao = ttk.Button(
                quadro_navegacao,
                text=texto_botao,
                style="Navegacao.TButton",
                command=lambda c=ClasseApp, k=chave_janela: self._abrir_janela(c, k)
            )
            botao.pack(fill="x", pady=5)

        botao_sair = ttk.Button(
            self,
            text="Sair da Aplicação",
            style="Sair.TButton",
            command=self._acao_sair
        )
        botao_sair.pack(pady=(30, 0))

    def _abrir_janela(self, ClasseApp, chave_janela: str):
        """
        Abre uma nova janela (Toplevel) com o módulo selecionado.

        Se a janela do módulo já existir, apenas a traz para frente.

        Args:
            ClasseApp: Classe do módulo a ser instanciado (ex: AplicacaoClientes).
            chave_janela (str): Chave única para identificar a janela aberta.
        """
        janela_existente = self.janelas_ativas.get(chave_janela)
        if janela_existente and janela_existente.winfo_exists():
            janela_existente.lift()
            return

        nova_janela = Toplevel(self.mestre)
        nova_janela.title(chave_janela)
        nova_janela.configure(bg="#f0f0f0")

        self.janelas_ativas[chave_janela] = nova_janela
        ClasseApp(nova_janela)

    def _acao_sair(self):
        """
        Exibe confirmação e encerra a aplicação se confirmado.
        """
        if messagebox.askokcancel("Sair", "Deseja realmente sair da aplicação?"):
            self.mestre.destroy()


if __name__ == "__main__":
    """
    Inicializa a aplicação principal Luxury Wheels.

    Configura:
    - Tk root
    - Canvas com scrollbar vertical para acomodar o menu principal
    - Container Frame dentro do canvas
    - Largura responsiva do frame conforme o canvas
    """
    raiz = tk.Tk()
    raiz.title("Luxury Wheels – Gestão de Frota")
    raiz.geometry("1000x700")
    raiz.configure(bg="#f0f0f0")
    raiz.resizable(True, True)

    canvas = tk.Canvas(raiz, bg="#f0f0f0", highlightthickness=0)
    barra_scroll_vertical = ttk.Scrollbar(raiz, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=barra_scroll_vertical.set)

    barra_scroll_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    container_frame = ttk.Frame(canvas, padding=20)
    id_canvas_frame = canvas.create_window((0, 0), window=container_frame, anchor="nw")

    # Ajusta o scrollregion do canvas sempre que o frame muda de tamanho
    def ao_configurar_frame(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Ajusta largura do container para sempre preencher o canvas
    def ao_configurar_canvas(event):
        canvas.itemconfig(id_canvas_frame, width=event.width)

    container_frame.bind("<Configure>", ao_configurar_frame)
    canvas.bind("<Configure>", ao_configurar_canvas)

    app = AplicacaoPrincipal(container_frame)
    app.pack(fill=tk.BOTH, expand=True)

    raiz.mainloop()
