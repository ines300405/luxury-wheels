import tkinter as tk

class DicaFerramenta:
    """
    Exibe uma dica (tooltip) associada a um widget do Tkinter.
    A dica aparece após um breve atraso e é posicionada próxima ao cursor ou ao widget.

    Args:
        widget (tk.Widget): Widget ao qual a dica será associada.
        texto (str): Texto a ser exibido na dica.
        atraso_ms (int): Atraso em milissegundos antes de mostrar a dica. Padrão: 500ms.
    """

    def __init__(self, widget: tk.Widget, texto: str, atraso_ms: int = 500):
        self.widget = widget
        self.texto = texto
        self.atraso_ms = atraso_ms
        self._id_acao_agendada = None  # id do after agendado
        self.janela_tooltip = None     # referência para a janela da dica

        # Eventos do widget
        widget.bind("<Enter>", self._agendar_exibicao)
        widget.bind("<Leave>", self._cancelar_exibicao)
        widget.bind("<ButtonPress>", self._cancelar_exibicao)

    def _agendar_exibicao(self, evento=None) -> None:
        """Agenda a exibição da dica após o atraso definido."""
        self._cancelar_exibicao()
        self._id_acao_agendada = self.widget.after(
            self.atraso_ms, lambda e=evento: self._mostrar(e)
        )

    def _cancelar_exibicao(self, evento=None) -> None:
        """Cancela a exibição agendada e esconde a dica se estiver visível."""
        if self._id_acao_agendada is not None:
            self.widget.after_cancel(self._id_acao_agendada)
            self._id_acao_agendada = None
        self._esconder()

    def _mostrar(self, evento=None) -> None:
        """Cria e mostra a janela da dica."""
        if self.janela_tooltip:
            return

        # Determina a posição
        if evento:
            pos_x = evento.x_root + 10
            pos_y = evento.y_root + 10
        else:
            pos_x = self.widget.winfo_rootx() + 10
            pos_y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Cria janela sem borda
        janela = tk.Toplevel(self.widget)
        janela.wm_overrideredirect(True)
        janela.wm_geometry(f"+{pos_x}+{pos_y}")

        etiqueta = tk.Label(
            janela, text=self.texto, justify="left",
            background="#ffffe0", relief="solid", borderwidth=1,
            padx=5, pady=2
        )
        etiqueta.pack()
        self.janela_tooltip = janela

    def _esconder(self) -> None:
        """Destrói a janela da dica, se existir."""
        if self.janela_tooltip:
            self.janela_tooltip.destroy()
            self.janela_tooltip = None
