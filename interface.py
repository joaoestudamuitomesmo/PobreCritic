import tkinter as tk
from tkinter import ttk, Menu

class CleanUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clean UI Example")
        self.geometry("1366x768")
        self.configure(bg="#F8FAFC")
        self.setup_login_screen()

    def round_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, 
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, 
            x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, 
            x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, 
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def setup_login_screen(self):
        self.canvas = tk.Canvas(self, bg="#F8FAFC", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(683, 180, text="Bem-vindo", font=("Segoe UI", 24, "bold"), fill="#0F172A")

        self.round_rect(self.canvas, 433, 230, 933, 530, radius=20, fill="#FFFFFF", outline="#E2E8F0")

        self.canvas.create_text(473, 280, text="Email", font=("Segoe UI", 10), fill="#64748B", anchor="w")

        self.round_rect(self.canvas, 473, 300, 893, 350, radius=12, fill="#F8FAFC", outline="#CBD5E1")
        
        self.user_entry = tk.Entry(self, font=("Segoe UI", 12), bg="#F8FAFC", fg="#0F172A", bd=0, highlightthickness=0, insertbackground="#0F172A")
        self.user_entry.place(x=485, y=312, width=396, height=26)

        self.btn_shape = self.round_rect(self.canvas, 473, 420, 893, 470, radius=15, fill="#3B82F6")
        self.btn_text = self.canvas.create_text(683, 445, text="Continuar", font=("Segoe UI", 12, "bold"), fill="#FFFFFF")

        self.canvas.tag_bind(self.btn_shape, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.btn_text, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.btn_shape, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.btn_text, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.btn_shape, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.btn_text, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.btn_shape, "<ButtonRelease-1>", self.on_release)
        self.canvas.tag_bind(self.btn_text, "<ButtonRelease-1>", self.on_release)

    def on_enter(self, e):
        try:
            self.canvas.itemconfig(self.btn_shape, fill="#2563EB")
        except tk.TclError:
            pass

    def on_leave(self, e):
        try:
            self.canvas.itemconfig(self.btn_shape, fill="#3B82F6")
        except tk.TclError:
            pass

    def on_click(self, e):
        try:
            self.canvas.itemconfig(self.btn_shape, fill="#1D4ED8")
        except tk.TclError:
            pass

    def on_release(self, e):
        try:
            self.canvas.itemconfig(self.btn_shape, fill="#2563EB")
            self.after(150, self.open_dashboard)
        except tk.TclError:
            pass

    def open_dashboard(self):
        self.canvas.destroy()
        self.user_entry.destroy()

        style = ttk.Style()
        style.theme_use("clam")
        
        bg_main = "#F8FAFC"
        card_bg = "#FFFFFF"
        primary = "#3B82F6"
        text_color = "#0F172A"
        muted_color = "#64748B"
        border_color = "#E2E8F0"

        style.configure(".", background=bg_main, font=("Segoe UI", 10), foreground=text_color)
        
        style.configure("TNotebook", background=bg_main, borderwidth=0)
        style.configure("TNotebook.Tab", background=bg_main, foreground=muted_color, padding=[20, 10], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", card_bg)], foreground=[("selected", primary)])

        style.configure("Card.TFrame", background=card_bg, borderwidth=1, relief="solid")
        
        style.configure("Treeview", background=card_bg, foreground=text_color, rowheight=36, fieldbackground=card_bg, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#F1F5F9", foreground=text_color, font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
        style.map("Treeview", background=[("selected", "#EFF6FF")], foreground=[("selected", primary)])
        
        style.configure("TCombobox", fieldbackground="#F8FAFC", background=card_bg, bordercolor=border_color, arrowcolor=muted_color, padding=6)
        style.configure("TSpinbox", fieldbackground="#F8FAFC", background=card_bg, bordercolor=border_color, arrowcolor=muted_color, padding=6)
        
        style.configure("TCheckbutton", background=card_bg, foreground=text_color, font=("Segoe UI", 10))
        style.configure("TRadiobutton", background=card_bg, foreground=text_color, font=("Segoe UI", 10))
        
        style.configure("THorizontal.TScale", background=card_bg, troughcolor="#E2E8F0", sliderthickness=16)
        style.configure("TProgressbar", thickness=10, troughcolor="#E2E8F0", background=primary, borderwidth=0)

        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background=primary, foreground="#FFFFFF", padding=[15, 8], borderwidth=0)
        style.map("Action.TButton", background=[("active", "#2563EB")])

        menubar = Menu(self, bg=card_bg, fg=text_color, activebackground=primary, activeforeground="#FFFFFF", bd=0)
        self.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0, bg=card_bg, fg=text_color, activebackground=primary, activeforeground="#FFFFFF")
        file_menu.add_command(label="Novo")
        file_menu.add_command(label="Abrir")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        header = tk.Frame(self, bg=card_bg, height=60, highlightthickness=1, highlightbackground=border_color)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_label = tk.Label(header, text="Painel do Sistema", font=("Segoe UI", 14, "bold"), bg=card_bg, fg=text_color)
        title_label.pack(side="left", padx=25)

        user_badge = tk.Label(header, text="• Admin Conectado", font=("Segoe UI", 10, "bold"), bg="#DCFCE7", fg="#15803D", padx=10, pady=4)
        user_badge.pack(side="right", padx=25)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=25, pady=20)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Visão Geral & Dados")

        t1_left = tk.Frame(tab1, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        t1_left.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        tk.Label(t1_left, text="Tabela de Produtos (Treeview)", font=("Segoe UI", 12, "bold"), bg=card_bg, fg=text_color).pack(anchor="w", padx=20, pady=(20, 10))

        cols = ("ID", "Nome do Produto", "Estoque", "Status")
        tree = ttk.Treeview(t1_left, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center" if col in ("ID", "Estoque", "Status") else "w")
        
        data = [
            ("001", "Teclado Mecânico RGB", "45", "Disponível"),
            ("002", "Mouse Wireless Ergônomico", "12", "Disponível"),
            ("003", "Monitor UltraWide 29\"", "0", "Esgotado"),
            ("004", "Webcam Full HD 1080p", "5", "Baixo Estoque"),
            ("005", "Headset Surround 7.1", "28", "Disponível"),
            ("006", "Cadeira Ergonômica", "3", "Baixo Estoque")
        ]
        for row in data:
            tree.insert("", "end", values=row)
            
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        t1_right = tk.Frame(tab1, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        t1_right.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        tk.Label(t1_right, text="Logs do Sistema (Listbox)", font=("Segoe UI", 12, "bold"), bg=card_bg, fg=text_color).pack(anchor="w", padx=20, pady=(20, 10))

        listbox = tk.Listbox(t1_right, font=("Segoe UI", 10), borderwidth=0, highlightthickness=0, bg="#F8FAFC", fg=text_color, selectbackground="#EFF6FF", selectforeground=primary, activestyle="none")
        for i in range(1, 30):
            listbox.insert("end", f"  [LOG #{i:03d}] Sessão sincronizada com o servidor.")
        listbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Controles e Formulários")

        t2_left = tk.Frame(tab2, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        t2_left.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        tk.Label(t2_left, text="Configurações Básicas", font=("Segoe UI", 12, "bold"), bg=card_bg, fg=text_color).pack(anchor="w", padx=20, pady=(20, 15))

        tk.Label(t2_left, text="Seleção de Perfil:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20)
        combo = ttk.Combobox(t2_left, values=["Administrador", "Gerente", "Operador"], state="readonly")
        combo.set("Administrador")
        combo.pack(anchor="w", fill="x", padx=20, pady=(5, 15))

        tk.Label(t2_left, text="Limite de Requisições:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20)
        spin = ttk.Spinbox(t2_left, from_=0, to=100)
        spin.set(50)
        spin.pack(anchor="w", fill="x", padx=20, pady=(5, 15))

        tk.Label(t2_left, text="Opções:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20, pady=(5, 0))
        ttk.Checkbutton(t2_left, text="Receber notificações push").pack(anchor="w", padx=20, pady=5)
        ttk.Checkbutton(t2_left, text="Autenticação em dois fatores").pack(anchor="w", padx=20, pady=5)

        tk.Label(t2_left, text="Formato de Exportação:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20, pady=(15, 0))
        radio_var = tk.StringVar(value="PDF")
        ttk.Radiobutton(t2_left, text="Exportar relatório em PDF", variable=radio_var, value="PDF").pack(anchor="w", padx=20, pady=5)
        ttk.Radiobutton(t2_left, text="Exportar dados brutos em CSV", variable=radio_var, value="CSV").pack(anchor="w", padx=20, pady=5)

        ttk.Button(t2_left, text="Salvar Alterações", style="Action.TButton").pack(anchor="w", padx=20, pady=25)

        t2_right = tk.Frame(tab2, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        t2_right.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        tk.Label(t2_right, text="Entradas Avançadas", font=("Segoe UI", 12, "bold"), bg=card_bg, fg=text_color).pack(anchor="w", padx=20, pady=(20, 15))

        tk.Label(t2_right, text="Volume do Sistema:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20)
        scale = ttk.Scale(t2_right, from_=0, to=100, orient="horizontal")
        scale.set(65)
        scale.pack(fill="x", padx=20, pady=(5, 15))

        tk.Label(t2_right, text="Sincronização do Banco:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20)
        prog = ttk.Progressbar(t2_right, value=80, mode="determinate")
        prog.pack(fill="x", padx=20, pady=(5, 20))

        tk.Label(t2_right, text="Observações Adicionais:", bg=card_bg, fg=muted_color).pack(anchor="w", padx=20)
        text_area = tk.Text(t2_right, height=8, font=("Segoe UI", 10), bg="#F8FAFC", fg=text_color, bd=0, highlightthickness=1, highlightbackground=border_color, padx=10, pady=10)
        text_area.insert("1.0", "Digite notas internas ou observações aqui...")
        text_area.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Módulos & Gráficos")

        paned = ttk.PanedWindow(tab3, orient="horizontal")
        paned.pack(fill="both", expand=True, pady=10)

        pane1 = tk.Frame(paned, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        pane2 = tk.Frame(paned, bg=card_bg, highlightthickness=1, highlightbackground=border_color)
        paned.add(pane1, weight=1)
        paned.add(pane2, weight=3)

        tk.Label(pane1, text="Navegação", font=("Segoe UI", 12, "bold"), bg=card_bg, fg=text_color).pack(pady=20)
        
        for item in ["Módulo 01 - Analytics", "Módulo 02 - Vendas", "Módulo 03 - Financeiro", "Módulo 04 - Suporte"]:
            lbl = tk.Label(pane1, text=item, font=("Segoe UI", 10), bg="#F8FAFC", fg=text_color, anchor="w", padx=15, pady=10, cursor="hand2")
            lbl.pack(fill="x", padx=15, pady=4)

        canvas_demo = tk.Canvas(pane2, bg=card_bg, highlightthickness=0)
        canvas_demo.pack(fill="both", expand=True, padx=20, pady=20)

        canvas_demo.create_text(20, 20, text="Métricas Visuais (Canvas Component)", font=("Segoe UI", 12, "bold"), fill=text_color, anchor="nw")

        self.round_rect(canvas_demo, 20, 60, 240, 180, radius=15, fill="#EFF6FF", outline="")
        canvas_demo.create_text(40, 90, text="Total de Vendas", font=("Segoe UI", 10), fill=muted_color, anchor="w")
        canvas_demo.create_text(40, 130, text="R$ 48.290", font=("Segoe UI", 20, "bold"), fill=primary, anchor="w")

        self.round_rect(canvas_demo, 260, 60, 480, 180, radius=15, fill="#ECFDF5", outline="")
        canvas_demo.create_text(280, 90, text="Novos Clientes", font=("Segoe UI", 10), fill=muted_color, anchor="w")
        canvas_demo.create_text(280, 130, text="+ 1,240", font=("Segoe UI", 20, "bold"), fill="#10B981", anchor="w")

        canvas_demo.create_line(20, 240, 740, 240, fill=border_color, width=1)

        points = [20, 380, 140, 320, 260, 350, 380, 280, 500, 300, 620, 260, 740, 290]
        canvas_demo.create_line(points, fill=primary, width=3, smooth=True)

        for i in range(0, len(points), 2):
            canvas_demo.create_oval(points[i]-4, points[i+1]-4, points[i]+4, points[i+1]+4, fill=primary, outline="#FFFFFF", width=2)