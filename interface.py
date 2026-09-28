import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from dados import BancoDados
from validacoes import CATEGORIAS, STATUS, nota_digitacao_valida, validar_jogo


def formatar_nota(nota, vazio=""):
    if nota is None:
        return vazio
    return f"{round(nota, 1):g}".replace(".", ",")


TAMANHO_PAGINA = 100
POSICOES_STATUS = ((30, 60), (100, 130), (240, 110), (360, 120))
TEXTO_ADICIONAR_DESEJO = "+ Adicionar"
TEXTO_NA_LISTA_DESEJO = "✓ Na lista"


def texto_status(status):
    return f"{status}  ▾"


def texto_desejo(desejo):
    return TEXTO_NA_LISTA_DESEJO if desejo else TEXTO_ADICIONAR_DESEJO


def mostrar_erro_banco(erro, parent=None):
    messagebox.showerror(
        "Erro", f"Não foi possível acessar os dados: {erro}", parent=parent
    )


def configurar_cores(root):
    root.option_add("*Button.background", "#7c3aed")
    root.option_add("*Button.foreground", "#ffffff")
    root.option_add("*Button.activeBackground", "#a855f7")
    root.option_add("*Button.activeForeground", "#ffffff")
    root.option_add("*Button.disabledForeground", "#5b4a7a")
    root.option_add("*Button.relief", "flat")
    root.option_add("*Button.borderWidth", 0)
    root.option_add("*Button.highlightThickness", 0)
    root.option_add("*Radiobutton.highlightThickness", 0)
    root.option_add("*Button.cursor", "hand2")
    root.option_add("*Entry.background", "#1b1029")
    root.option_add("*Entry.foreground", "#ffffff")
    root.option_add("*Entry.insertBackground", "#ffffff")
    root.option_add("*Entry.selectBackground", "#7c3aed")
    root.option_add("*Entry.selectForeground", "#ffffff")
    root.option_add("*Entry.relief", "flat")
    root.option_add("*Entry.highlightThickness", 1)
    root.option_add("*Entry.highlightBackground", "#3b2666")
    root.option_add("*Entry.highlightColor", "#a855f7")
    root.option_add("*Text.background", "#1b1029")
    root.option_add("*Text.foreground", "#ffffff")
    root.option_add("*Text.insertBackground", "#ffffff")
    root.option_add("*Text.selectBackground", "#7c3aed")
    root.option_add("*Text.selectForeground", "#ffffff")
    root.option_add("*Text.relief", "flat")
    root.option_add("*Text.highlightThickness", 1)
    root.option_add("*Text.highlightBackground", "#3b2666")
    root.option_add("*Text.highlightColor", "#a855f7")
    root.option_add("*Menu.background", "#1b1029")
    root.option_add("*Menu.foreground", "#ffffff")
    root.option_add("*Menu.activeBackground", "#7c3aed")
    root.option_add("*Menu.activeForeground", "#ffffff")
    root.option_add("*TCombobox*Listbox.background", "#1b1029")
    root.option_add("*TCombobox*Listbox.foreground", "#ffffff")
    root.option_add("*TCombobox*Listbox.selectBackground", "#7c3aed")
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")


def configurar_estilo():
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure(
        "Catalogo.Treeview",
        background="#1b1029",
        foreground="#ffffff",
        fieldbackground="#1b1029",
        rowheight=32,
        font=("Helvetica", 12),
        borderwidth=0,
        bordercolor="#0a0a0f",
        lightcolor="#0a0a0f",
        darkcolor="#0a0a0f",
    )
    estilo.configure(
        "Catalogo.Treeview.Heading",
        background="#0a0a0f",
        foreground="#ffffff",
        font=("Helvetica", 12, "bold"),
        relief="flat",
    )
    estilo.map(
        "Catalogo.Treeview",
        background=[("selected", "#7c3aed")],
        foreground=[("selected", "#ffffff")],
    )
    estilo.map("Catalogo.Treeview.Heading", background=[("active", "#1b1029")])
    estilo.configure(
        "TCombobox",
        fieldbackground="#1b1029",
        background="#7c3aed",
        foreground="#ffffff",
        arrowcolor="#ffffff",
        bordercolor="#7c3aed",
        lightcolor="#1b1029",
        darkcolor="#1b1029",
        selectbackground="#1b1029",
        selectforeground="#ffffff",
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", "#1b1029")],
        foreground=[("readonly", "#ffffff")],
        selectbackground=[("readonly", "#1b1029")],
        selectforeground=[("readonly", "#ffffff")],
    )
    estilo.configure(
        "Vertical.TScrollbar",
        background="#7c3aed",
        troughcolor="#0a0a0f",
        bordercolor="#0a0a0f",
        arrowcolor="#ffffff",
        lightcolor="#7c3aed",
        darkcolor="#7c3aed",
    )
    estilo.map("Vertical.TScrollbar", background=[("active", "#a855f7")])


class Interface:

    def __init__(self, root):
        self.root = root
        configurar_cores(root)
        root.title("PobreCritic - Login")
        root.geometry("1366x768")

        self.frame1 = tk.Frame(root, bg="#0a0a0f", relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=1366, height=1668)

        self.frame2 = tk.Frame(self.frame1, bg="#1b1029")
        self.frame2.place(x=433, y=90, width=500, height=600)

        self.label1 = tk.Label(
            self.frame2,
            text="BEM VINDO ",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 32, "bold"),
        )
        self.label1.place(x=80, y=0, width=350, height=120)

        self.label2 = tk.Label(
            self.frame2,
            text="Login",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 24, "bold"),
        )
        self.label2.place(x=75, y=40, width=350, height=120)

        self.in_putEmail = tk.Entry(self.frame2, font=("Helvetica", 12))
        self.in_putEmail.place(x=55, y=220, width=400, height=40)
        self.in_putEmail.bind("<Return>", self.on_in_putEmail_return)

        self.in_putSenha = tk.Entry(self.frame2, font=("Helvetica", 12), show="*")
        self.in_putSenha.place(x=55, y=310, width=400, height=40)
        self.in_putSenha.bind("<Return>", self.on_buttonLogin)

        self.buttonLogin = tk.Button(
            self.frame2,
            text="LOGIN",
            command=self.on_buttonLogin,
            font=("Helvetica", 14, "bold"),
        )
        self.buttonLogin.place(x=110, y=500, width=290, height=70)

        self.labelEmail = tk.Label(
            self.frame2,
            text="Email",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 24, "bold"),
        )
        self.labelEmail.place(x=60, y=180, width=90, height=40)

        self.labelSenha = tk.Label(
            self.frame2,
            text="Senha",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 24, "bold"),
        )
        self.labelSenha.place(x=60, y=270, width=100, height=40)

        self.in_putEmail.focus_set()

    def open_pobrecritic___cat_logo(self):
        try:
            banco = BancoDados()
        except (sqlite3.Error, OSError, ValueError) as erro:
            mostrar_erro_banco(erro)
            self.root.deiconify()
            return None
        return PobreCriticCatLogo(self.root, banco)

    def is_valid_email(self, email):
        return "@" in email and "." in email and len(email.strip()) > 5

    def on_in_putEmail_return(self, event):
        self.in_putSenha.focus_set()

    def on_buttonLogin(self, event=None):
        email = self.in_putEmail.get().strip()
        senha = self.in_putSenha.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Erro", "Por favor, insira um e-mail válido!")
            return

        if len(senha) < 4:
            messagebox.showerror("Erro", "A senha deve ter no mínimo 4 caracteres!")
            return

        self.root.withdraw()
        self.open_pobrecritic___cat_logo()


class PobreCriticCatLogo:

    def __init__(self, master, banco):
        root = tk.Toplevel(master)
        self.root = root
        self.master = master
        self.banco = banco
        self.pagina = 0
        self.busca_agendada = None
        self.jogo_menu = None
        root.title("PobreCritic - Catálogo")
        root.geometry("1366x768")
        root.protocol("WM_DELETE_WINDOW", self.on_buttonSair)
        root.bind("<Control-n>", self.on_ctrl_n)
        root.bind("<Control-f>", self.on_ctrl_f)

        configurar_estilo()

        self.varBusca = tk.StringVar()

        self.frame1 = tk.Frame(root, bg="#0a0a0f", relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=1366, height=1668)

        self.labelTitulo = tk.Label(
            self.frame1,
            text="CATÁLOGO",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 32, "bold"),
            anchor="w",
        )
        self.labelTitulo.place(x=40, y=10, width=400, height=70)

        self.labelPagina = tk.Label(
            self.frame1,
            text="",
            fg="#a855f7",
            bg="#0a0a0f",
            font=("Helvetica", 14, "bold"),
            anchor="e",
        )
        self.labelPagina.place(x=460, y=25, width=530, height=40)

        self.buttonAnterior = tk.Button(
            self.frame1,
            text="< ANTERIOR",
            command=self.on_buttonAnterior,
            font=("Helvetica", 11, "bold"),
        )
        self.buttonAnterior.place(x=1000, y=25, width=150, height=40)

        self.buttonProxima = tk.Button(
            self.frame1,
            text="PRÓXIMA >",
            command=self.on_buttonProxima,
            font=("Helvetica", 11, "bold"),
        )
        self.buttonProxima.place(x=1165, y=25, width=161, height=40)

        self.labelBusca = tk.Label(
            self.frame1,
            text="Buscar",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        self.labelBusca.place(x=40, y=95, width=100, height=30)

        self.in_putBusca = tk.Entry(
            self.frame1, textvariable=self.varBusca, font=("Helvetica", 12)
        )
        self.in_putBusca.place(x=40, y=125, width=420, height=36)
        self.in_putBusca.bind("<KeyRelease>", self.on_in_putBusca_keyrelease)

        self.labelCategoria = tk.Label(
            self.frame1,
            text="Categoria",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        self.labelCategoria.place(x=480, y=95, width=220, height=30)

        self.comboCategoria = ttk.Combobox(
            self.frame1,
            values=("Todas",),
            state="readonly",
            font=("Helvetica", 12),
        )
        self.comboCategoria.set("Todas")
        self.comboCategoria.place(x=480, y=125, width=220, height=36)
        self.comboCategoria.bind("<<ComboboxSelected>>", self.atualizar_filtros)

        self.labelPlataforma = tk.Label(
            self.frame1,
            text="Plataforma",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        self.labelPlataforma.place(x=720, y=95, width=200, height=30)

        self.comboPlataforma = ttk.Combobox(
            self.frame1,
            values=("Todas",),
            state="readonly",
            font=("Helvetica", 12),
        )
        self.comboPlataforma.set("Todas")
        self.comboPlataforma.place(x=720, y=125, width=200, height=36)
        self.comboPlataforma.bind("<<ComboboxSelected>>", self.atualizar_filtros)

        self.labelStatus = tk.Label(
            self.frame1,
            text="Status",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        self.labelStatus.place(x=940, y=95, width=200, height=30)

        self.comboStatus = ttk.Combobox(
            self.frame1,
            values=("Todos",) + STATUS,
            state="readonly",
            font=("Helvetica", 12),
        )
        self.comboStatus.set("Todos")
        self.comboStatus.place(x=940, y=125, width=200, height=36)
        self.comboStatus.bind("<<ComboboxSelected>>", self.atualizar_filtros)

        self.buttonLimparFiltros = tk.Button(
            self.frame1,
            text="LIMPAR FILTROS",
            command=self.on_buttonLimparFiltros,
            font=("Helvetica", 11, "bold"),
        )
        self.buttonLimparFiltros.place(x=1160, y=125, width=166, height=36)

        self.menuStatus = tk.Menu(root, tearoff=0, font=("Helvetica", 12))
        for status in STATUS:
            self.menuStatus.add_command(
                label=status, command=lambda valor=status: self.definir_status(valor)
            )

        self.treeJogos = ttk.Treeview(
            self.frame1,
            columns=("titulo", "plataforma", "categoria", "nota", "status", "desejo"),
            show="headings",
            selectmode="browse",
            style="Catalogo.Treeview",
        )
        self.treeJogos.heading("titulo", text="Título")
        self.treeJogos.heading("plataforma", text="Plataforma")
        self.treeJogos.heading("categoria", text="Categoria")
        self.treeJogos.heading("nota", text="Nota")
        self.treeJogos.heading("status", text="Status")
        self.treeJogos.heading("desejo", text="Lista de desejos")
        self.treeJogos.column("titulo", width=470, anchor="w")
        self.treeJogos.column("plataforma", width=170, anchor="w")
        self.treeJogos.column("categoria", width=200, anchor="w")
        self.treeJogos.column("nota", width=90, anchor="center")
        self.treeJogos.column("status", width=150, anchor="w")
        self.treeJogos.column("desejo", width=186, anchor="center")
        self.treeJogos.place(x=40, y=175, width=1266, height=445)
        self.treeJogos.bind("<Button-1>", self.on_treeJogos_click)
        self.treeJogos.bind("<Double-1>", self.on_treeJogos_double)
        self.treeJogos.bind("<Return>", self.on_buttonAbrir)
        self.treeJogos.bind("<space>", self.on_treeJogos_space)
        self.treeJogos.bind("<Delete>", self.on_buttonExcluir)

        self.scrollJogos = ttk.Scrollbar(
            self.frame1, orient="vertical", command=self.treeJogos.yview
        )
        self.scrollJogos.place(x=1306, y=175, width=20, height=445)
        self.treeJogos.configure(yscrollcommand=self.scrollJogos.set)

        self.labelVazio = tk.Label(
            self.frame1,
            text="",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 14),
        )

        self.buttonSubmeter = tk.Button(
            self.frame1,
            text="SUBMETER UM JOGO",
            command=self.open_pobrecritic___submeter_um_jogo,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonSubmeter.place(x=40, y=640, width=300, height=60)

        self.buttonListaDesejos = tk.Button(
            self.frame1,
            text="LISTA DE DESEJOS",
            command=self.open_pobrecritic___lista_de_desejos,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonListaDesejos.place(x=360, y=640, width=300, height=60)

        self.buttonExcluir = tk.Button(
            self.frame1,
            text="EXCLUIR",
            command=self.on_buttonExcluir,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonExcluir.place(x=680, y=640, width=300, height=60)

        self.buttonSair = tk.Button(
            self.frame1,
            text="SAIR",
            command=self.on_buttonSair,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonSair.place(x=1000, y=640, width=326, height=60)

        self.atualizar_lista()
        self.in_putBusca.focus_set()

    def open_pobrecritic___jogo(self, jogo_id):
        return PobreCriticJogo(self.root, self.banco, jogo_id, self.atualizar_lista)

    def open_pobrecritic___lista_de_desejos(self):
        return PobreCriticListaDeDesejos(self.root, self.banco, self.atualizar_lista)

    def open_pobrecritic___submeter_um_jogo(self):
        return PobreCriticSubmeterUmJogo(self.root, self.banco, self.atualizar_lista)

    def obter_selecionado(self):
        selecao = self.treeJogos.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção", "Selecione um jogo na lista.", parent=self.root
            )
            return None

        return int(selecao[0])

    def atualizar_opcoes_filtros(self):
        categorias = ("Todas",) + tuple(self.banco.categorias())
        plataformas = ("Todas",) + tuple(self.banco.plataformas())

        self.comboCategoria.configure(values=categorias)
        self.comboPlataforma.configure(values=plataformas)

        if self.comboCategoria.get() not in categorias:
            self.comboCategoria.set("Todas")

        if self.comboPlataforma.get() not in plataformas:
            self.comboPlataforma.set("Todas")

    def atualizar_filtros(self, event=None):
        self.pagina = 0
        self.atualizar_lista()

    def atualizar_lista(self, event=None):
        selecao = self.treeJogos.selection()

        try:
            self.atualizar_opcoes_filtros()
            jogos = self.banco.listar(
                self.varBusca.get(),
                self.comboCategoria.get(),
                self.comboPlataforma.get(),
                self.comboStatus.get(),
            )
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        total = len(jogos)
        total_paginas = max(1, -(-total // TAMANHO_PAGINA))
        self.pagina = min(self.pagina, total_paginas - 1)
        inicio = self.pagina * TAMANHO_PAGINA

        self.treeJogos.delete(*self.treeJogos.get_children())

        for jogo in jogos[inicio : inicio + TAMANHO_PAGINA]:
            self.treeJogos.insert(
                "",
                "end",
                iid=str(jogo["id"]),
                values=(
                    jogo["titulo"],
                    jogo["plataforma"],
                    jogo["categoria"],
                    formatar_nota(jogo["nota"], "-"),
                    texto_status(jogo["status"]),
                    texto_desejo(jogo["desejo"]),
                ),
            )

        if selecao and self.treeJogos.exists(selecao[0]):
            self.treeJogos.selection_set(selecao[0])
            self.treeJogos.see(selecao[0])

        total_formatado = f"{total:,}".replace(",", ".")
        self.labelPagina.configure(
            text=f"Página {self.pagina + 1} de {total_paginas}   |   {total_formatado} jogos"
        )
        self.buttonAnterior.configure(state="normal" if self.pagina > 0 else "disabled")
        self.buttonProxima.configure(
            state="normal" if self.pagina < total_paginas - 1 else "disabled"
        )
        self.atualizar_mensagem_vazia(total > 0)

    def atualizar_mensagem_vazia(self, tem_jogos):
        if tem_jogos:
            self.labelVazio.place_forget()
            return

        filtrando = (
            self.varBusca.get().strip()
            or self.comboCategoria.get() != "Todas"
            or self.comboPlataforma.get() != "Todas"
            or self.comboStatus.get() != "Todos"
        )

        if filtrando:
            texto = "Nenhum jogo encontrado para os filtros informados."
        else:
            texto = "Nenhum jogo cadastrado. Clique em SUBMETER UM JOGO."

        self.labelVazio.configure(text=texto)
        self.labelVazio.place(x=40, y=350, width=1266, height=40)

    def alternar_desejo(self, jogo_id):
        try:
            desejo = self.banco.alternar_desejo(jogo_id)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.treeJogos.set(str(jogo_id), "desejo", texto_desejo(desejo))

    def definir_status(self, status):
        if self.jogo_menu is None:
            return

        try:
            self.banco.definir_status(self.jogo_menu, status)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.atualizar_lista()

    def on_ctrl_n(self, event):
        self.open_pobrecritic___submeter_um_jogo()

    def on_ctrl_f(self, event):
        self.in_putBusca.focus_set()
        self.in_putBusca.select_range(0, "end")

    def on_in_putBusca_keyrelease(self, event):
        if self.busca_agendada is not None:
            self.root.after_cancel(self.busca_agendada)
        self.busca_agendada = self.root.after(250, self.atualizar_filtros)

    def on_buttonAnterior(self):
        self.pagina -= 1
        self.atualizar_lista()

    def on_buttonProxima(self):
        self.pagina += 1
        self.atualizar_lista()

    def on_buttonLimparFiltros(self):
        self.varBusca.set("")
        self.comboCategoria.set("Todas")
        self.comboPlataforma.set("Todas")
        self.comboStatus.set("Todos")
        self.atualizar_filtros()
        self.in_putBusca.focus_set()

    def on_treeJogos_click(self, event):
        if self.treeJogos.identify_region(event.x, event.y) != "cell":
            return

        coluna = self.treeJogos.identify_column(event.x)
        linha = self.treeJogos.identify_row(event.y)

        if not linha:
            return

        if coluna == "#5":
            self.jogo_menu = int(linha)
            self.treeJogos.selection_set(linha)
            try:
                self.menuStatus.tk_popup(event.x_root, event.y_root)
            finally:
                self.menuStatus.grab_release()
            return "break"

        if coluna == "#6":
            self.alternar_desejo(int(linha))

    def on_treeJogos_double(self, event):
        if self.treeJogos.identify_column(event.x) in ("#5", "#6"):
            return

        if self.treeJogos.identify_region(event.x, event.y) != "cell":
            return

        self.on_buttonAbrir()

    def on_treeJogos_space(self, event):
        selecao = self.treeJogos.selection()

        if selecao:
            self.alternar_desejo(int(selecao[0]))

        return "break"

    def on_buttonAbrir(self, event=None):
        jogo_id = self.obter_selecionado()

        if jogo_id is None:
            return

        self.open_pobrecritic___jogo(jogo_id)

    def on_buttonExcluir(self, event=None):
        jogo_id = self.obter_selecionado()

        if jogo_id is None:
            return

        titulo = self.treeJogos.item(str(jogo_id), "values")[0]

        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir o jogo '{titulo}'?",
            parent=self.root,
        ):
            return

        try:
            self.banco.excluir(jogo_id)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.atualizar_lista()
        messagebox.showinfo(
            "Sucesso", "Jogo excluído com sucesso!", parent=self.root
        )

    def on_buttonSair(self):
        if not messagebox.askyesno(
            "Sair", "Deseja realmente sair do PobreCritic?", parent=self.root
        ):
            return

        self.banco.fechar()
        self.master.destroy()


class PobreCriticFormularioJogo:

    def __init__(self, master, titulo_janela, titulo_tela, banco, ao_salvar):
        root = tk.Toplevel(master)
        self.root = root
        self.banco = banco
        self.ao_salvar = ao_salvar
        self.jogo_id = None
        root.title(titulo_janela)
        root.geometry("560x730")
        root.resizable(False, False)
        root.transient(master)
        root.protocol("WM_DELETE_WINDOW", self.on_buttonVoltar)
        root.bind("<Escape>", self.on_buttonVoltar)
        root.bind("<Control-s>", self.on_buttonSalvar)

        self.varTitulo = tk.StringVar()
        self.varCategoria = tk.StringVar()
        self.varPlataforma = tk.StringVar()
        self.varNota = tk.StringVar()
        self.varStatus = tk.StringVar(value=STATUS[0])
        self.varDesejo = tk.BooleanVar(value=False)

        self.frame1 = tk.Frame(root, bg="#0a0a0f", relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=560, height=730)

        self.frame2 = tk.Frame(self.frame1, bg="#1b1029")
        self.frame2.place(x=20, y=20, width=520, height=690)

        self.labelTitulo = tk.Label(
            self.frame2,
            text=titulo_tela,
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 20, "bold"),
        )
        self.labelTitulo.place(x=30, y=10, width=460, height=40)

        self.labelNome = self.criar_rotulo("Título", 30, 60, 460)

        self.in_putTitulo = tk.Entry(
            self.frame2, textvariable=self.varTitulo, font=("Helvetica", 12)
        )
        self.in_putTitulo.place(x=30, y=86, width=460, height=34)
        self.in_putTitulo.bind("<Return>", self.on_in_putTitulo_return)

        self.labelCategoria = self.criar_rotulo("Categoria", 30, 130, 230)

        self.comboCategoria = ttk.Combobox(
            self.frame2,
            textvariable=self.varCategoria,
            values=self.listar_categorias(),
            font=("Helvetica", 12),
        )
        self.comboCategoria.place(x=30, y=156, width=230, height=34)

        self.labelPlataforma = self.criar_rotulo("Plataforma", 280, 130, 210)

        self.comboPlataforma = ttk.Combobox(
            self.frame2,
            textvariable=self.varPlataforma,
            values=self.listar_plataformas(),
            font=("Helvetica", 12),
        )
        self.comboPlataforma.place(x=280, y=156, width=210, height=34)

        self.labelNota = self.criar_rotulo("Nota (0 a 10)", 30, 200, 230)

        validacao_nota = (root.register(nota_digitacao_valida), "%P")
        self.in_putNota = tk.Entry(
            self.frame2,
            textvariable=self.varNota,
            font=("Helvetica", 12),
            validate="key",
            validatecommand=validacao_nota,
        )
        self.in_putNota.place(x=30, y=226, width=230, height=34)

        self.labelStatus = self.criar_rotulo("Status", 30, 270, 460)

        self.radiosStatus = []
        for indice, status in enumerate(STATUS):
            radio = tk.Radiobutton(
                self.frame2,
                text=status,
                value=status,
                variable=self.varStatus,
                fg="#ffffff",
                bg="#1b1029",
                selectcolor="#7c3aed",
                activebackground="#1b1029",
                activeforeground="#ffffff",
                font=("Helvetica", 12),
                anchor="w",
            )
            radio.place(
                x=POSICOES_STATUS[indice][0],
                y=296,
                width=POSICOES_STATUS[indice][1],
                height=30,
            )
            self.radiosStatus.append(radio)

        self.labelObservacao = self.criar_rotulo("Observação", 30, 340, 460)

        self.textObservacao = tk.Text(
            self.frame2, font=("Helvetica", 12), wrap="word"
        )
        self.textObservacao.place(x=30, y=366, width=460, height=90)
        self.textObservacao.bind("<Tab>", self.on_textObservacao_tab)
        self.textObservacao.bind("<Shift-Tab>", self.on_textObservacao_shift_tab)

        self.buttonDesejo = tk.Button(
            self.frame2,
            text=texto_desejo(False),
            command=self.on_buttonDesejo,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonDesejo.place(x=30, y=470, width=460, height=40)

        self.buttonSalvar = tk.Button(
            self.frame2,
            text="SALVAR",
            command=self.on_buttonSalvar,
            font=("Helvetica", 14, "bold"),
        )
        self.buttonSalvar.place(x=30, y=525, width=225, height=55)

        self.buttonSecundario = tk.Button(
            self.frame2, text="", font=("Helvetica", 14, "bold")
        )
        self.buttonSecundario.place(x=265, y=525, width=225, height=55)

        self.buttonVoltar = tk.Button(
            self.frame2,
            text="VOLTAR",
            command=self.on_buttonVoltar,
            font=("Helvetica", 14, "bold"),
        )
        self.buttonVoltar.place(x=30, y=595, width=460, height=45)

        self.labelDica = tk.Label(
            self.frame2,
            text="Ctrl+S salva   |   Esc volta",
            fg="#b9a3d9",
            bg="#1b1029",
            font=("Helvetica", 10),
        )
        self.labelDica.place(x=30, y=652, width=460, height=24)

        self.registrar_estado()
        root.wait_visibility()
        root.grab_set()
        self.in_putTitulo.focus_set()

    def listar_categorias(self):
        try:
            return self.banco.categorias() or list(CATEGORIAS)
        except sqlite3.Error:
            return list(CATEGORIAS)

    def listar_plataformas(self):
        try:
            return self.banco.plataformas()
        except sqlite3.Error:
            return []

    def criar_rotulo(self, texto, x, y, largura):
        label = tk.Label(
            self.frame2,
            text=texto,
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 12, "bold"),
            anchor="w",
        )
        label.place(x=x, y=y, width=largura, height=24)
        return label

    def ler_campos(self):
        return (
            self.varTitulo.get(),
            self.varCategoria.get(),
            self.varPlataforma.get(),
            self.varNota.get(),
            self.varStatus.get(),
            self.textObservacao.get("1.0", "end-1c"),
            self.varDesejo.get(),
        )

    def preencher(self, titulo, categoria, plataforma, nota, status, observacao, desejo):
        self.varTitulo.set(titulo)
        self.varCategoria.set(categoria)
        self.varPlataforma.set(plataforma)
        self.varNota.set(nota)
        self.varStatus.set(status)
        self.textObservacao.delete("1.0", "end")
        self.textObservacao.insert("1.0", observacao)
        self.varDesejo.set(bool(desejo))
        self.buttonDesejo.configure(text=texto_desejo(self.varDesejo.get()))
        self.registrar_estado()

    def registrar_estado(self):
        self.estado_inicial = self.ler_campos()

    def limpar(self):
        self.preencher("", "", "", "", STATUS[0], "", False)
        self.in_putTitulo.focus_set()

    def salvar_registro(self, dados):
        raise NotImplementedError

    def concluir_salvamento(self):
        raise NotImplementedError

    def on_buttonDesejo(self):
        self.varDesejo.set(not self.varDesejo.get())
        self.buttonDesejo.configure(text=texto_desejo(self.varDesejo.get()))

    def on_in_putTitulo_return(self, event):
        self.comboCategoria.focus_set()

    def on_textObservacao_tab(self, event):
        event.widget.tk_focusNext().focus_set()
        return "break"

    def on_textObservacao_shift_tab(self, event):
        event.widget.tk_focusPrev().focus_set()
        return "break"

    def on_buttonSalvar(self, event=None):
        try:
            dados = validar_jogo(*self.ler_campos())
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro), parent=self.root)
            return

        try:
            if self.banco.existe_titulo(
                dados["titulo"], dados["plataforma"], self.jogo_id
            ):
                messagebox.showwarning(
                    "Atenção",
                    "Já existe um jogo com esse título nessa plataforma.",
                    parent=self.root,
                )
                return
            self.salvar_registro(dados)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.ao_salvar()
        self.concluir_salvamento()

    def on_buttonVoltar(self, event=None):
        if self.ler_campos() != self.estado_inicial:
            if not messagebox.askyesno(
                "Alterações pendentes",
                "Existem alterações não salvas. Deseja sair sem salvar?",
                parent=self.root,
            ):
                return

        self.root.destroy()


class PobreCriticSubmeterUmJogo(PobreCriticFormularioJogo):

    def __init__(self, master, banco, ao_salvar):
        super().__init__(
            master,
            "PobreCritic - Submeter um jogo",
            "SUBMETER UM JOGO",
            banco,
            ao_salvar,
        )
        self.buttonSecundario.configure(text="LIMPAR", command=self.on_buttonLimpar)

    def salvar_registro(self, dados):
        self.banco.inserir(dados)

    def concluir_salvamento(self):
        messagebox.showinfo(
            "Sucesso", "Jogo submetido com sucesso!", parent=self.root
        )
        self.limpar()

    def on_buttonLimpar(self):
        self.limpar()


class PobreCriticJogo(PobreCriticFormularioJogo):

    def __init__(self, master, banco, jogo_id, ao_salvar):
        super().__init__(
            master, "PobreCritic - Jogo", "DETALHES DO JOGO", banco, ao_salvar
        )
        self.jogo_id = jogo_id
        self.buttonSecundario.configure(text="EXCLUIR", command=self.on_buttonExcluir)

        try:
            jogo = banco.obter(jogo_id)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            self.root.destroy()
            return

        if jogo is None:
            messagebox.showwarning(
                "Atenção", "Este jogo não existe mais.", parent=self.root
            )
            self.root.destroy()
            return

        self.titulo_original = jogo["titulo"]
        self.preencher(
            jogo["titulo"],
            jogo["categoria"],
            jogo["plataforma"],
            formatar_nota(jogo["nota"]),
            jogo["status"],
            jogo["observacao"],
            jogo["desejo"],
        )

    def salvar_registro(self, dados):
        self.banco.atualizar(self.jogo_id, dados)

    def concluir_salvamento(self):
        messagebox.showinfo(
            "Sucesso", "Jogo atualizado com sucesso!", parent=self.root
        )
        self.root.destroy()

    def on_buttonExcluir(self):
        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir o jogo '{self.titulo_original}'?",
            parent=self.root,
        ):
            return

        try:
            self.banco.excluir(self.jogo_id)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.ao_salvar()
        messagebox.showinfo(
            "Sucesso", "Jogo excluído com sucesso!", parent=self.root
        )
        self.root.destroy()


class PobreCriticListaDeDesejos:

    def __init__(self, master, banco, ao_alterar):
        root = tk.Toplevel(master)
        self.root = root
        self.banco = banco
        self.ao_alterar = ao_alterar
        root.title("PobreCritic - Lista de desejos")
        root.geometry("760x520")
        root.resizable(False, False)
        root.transient(master)
        root.bind("<Escape>", self.on_buttonFechar)

        self.frame1 = tk.Frame(root, bg="#0a0a0f", relief="groove", bd=2)
        self.frame1.place(x=0, y=0, width=760, height=520)

        self.labelTitulo = tk.Label(
            self.frame1,
            text="LISTA DE DESEJOS",
            fg="#ffffff",
            bg="#0a0a0f",
            font=("Helvetica", 24, "bold"),
            anchor="w",
        )
        self.labelTitulo.place(x=20, y=15, width=720, height=50)

        self.treeDesejos = ttk.Treeview(
            self.frame1,
            columns=("titulo", "plataforma", "categoria", "status"),
            show="headings",
            selectmode="browse",
            style="Catalogo.Treeview",
        )
        self.treeDesejos.heading("titulo", text="Título")
        self.treeDesejos.heading("plataforma", text="Plataforma")
        self.treeDesejos.heading("categoria", text="Categoria")
        self.treeDesejos.heading("status", text="Status")
        self.treeDesejos.column("titulo", width=280, anchor="w")
        self.treeDesejos.column("plataforma", width=130, anchor="w")
        self.treeDesejos.column("categoria", width=150, anchor="w")
        self.treeDesejos.column("status", width=140, anchor="w")
        self.treeDesejos.place(x=20, y=80, width=700, height=340)
        self.treeDesejos.bind("<Double-1>", self.on_buttonAbrir)
        self.treeDesejos.bind("<Return>", self.on_buttonAbrir)
        self.treeDesejos.bind("<Delete>", self.on_buttonRemover)

        self.scrollDesejos = ttk.Scrollbar(
            self.frame1, orient="vertical", command=self.treeDesejos.yview
        )
        self.scrollDesejos.place(x=720, y=80, width=20, height=340)
        self.treeDesejos.configure(yscrollcommand=self.scrollDesejos.set)

        self.labelVazio = tk.Label(
            self.frame1,
            text="Sua lista de desejos está vazia.",
            fg="#ffffff",
            bg="#1b1029",
            font=("Helvetica", 14),
        )

        self.buttonRemover = tk.Button(
            self.frame1,
            text="REMOVER DOS DESEJOS",
            command=self.on_buttonRemover,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonRemover.place(x=20, y=440, width=280, height=55)

        self.buttonAbrir = tk.Button(
            self.frame1,
            text="ABRIR JOGO",
            command=self.on_buttonAbrir,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonAbrir.place(x=315, y=440, width=200, height=55)

        self.buttonFechar = tk.Button(
            self.frame1,
            text="FECHAR",
            command=self.on_buttonFechar,
            font=("Helvetica", 12, "bold"),
        )
        self.buttonFechar.place(x=530, y=440, width=210, height=55)

        self.atualizar_lista()
        self.treeDesejos.focus_set()

    def obter_selecionado(self):
        selecao = self.treeDesejos.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção", "Selecione um jogo na lista.", parent=self.root
            )
            return None

        return int(selecao[0])

    def atualizar_lista(self):
        try:
            jogos = self.banco.listar(apenas_desejos=True)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.treeDesejos.delete(*self.treeDesejos.get_children())

        for jogo in jogos:
            self.treeDesejos.insert(
                "",
                "end",
                iid=str(jogo["id"]),
                values=(
                    jogo["titulo"],
                    jogo["plataforma"],
                    jogo["categoria"],
                    jogo["status"],
                ),
            )

        if jogos:
            self.labelVazio.place_forget()
        else:
            self.labelVazio.place(x=20, y=220, width=700, height=40)

    def atualizar_apos_edicao(self):
        self.atualizar_lista()
        self.ao_alterar()

    def on_buttonAbrir(self, event=None):
        jogo_id = self.obter_selecionado()

        if jogo_id is None:
            return

        PobreCriticJogo(self.root, self.banco, jogo_id, self.atualizar_apos_edicao)

    def on_buttonRemover(self, event=None):
        jogo_id = self.obter_selecionado()

        if jogo_id is None:
            return

        try:
            self.banco.remover_desejo(jogo_id)
        except sqlite3.Error as erro:
            mostrar_erro_banco(erro, self.root)
            return

        self.atualizar_apos_edicao()

    def on_buttonFechar(self, event=None):
        self.root.destroy()