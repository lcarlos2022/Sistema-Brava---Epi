import json
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Arquivos de Dados Locais
ARQUIVO_PRODUTOS = "produtos_epis.json"
ARQUIVO_COLABORADORES = "colaboradores_cadastrados.json"
ARQUIVO_ENTREGAS = "entregas_epi.json"
ARQUIVO_USUARIOS = "usuarios_tst.json"

COLABORADORES_INICIAIS = [
    {"matricula": "2924", "nome": "ABNOAN IRINEU DOS SANTOS", "funcao": "FERREIRO"},
    {"matricula": "2926", "nome": "CARLOS CARDOZO DO NASCIMENTO", "funcao": "SERVENTE"},
    {"matricula": "2940", "nome": "ERIVALDO GOMES SILVEIRA- GHCC", "funcao": "CARPINTEIRO"},
    {"matricula": "2923", "nome": "EVANDRO MATIAS DO NASCIMENTO", "funcao": "VIGIA"},
    {"matricula": "2933", "nome": "FERNANDO PROCOPIO DA SILVA", "funcao": "FERREIRO"},
    {"matricula": "2938", "nome": "FRANCISCO DAVI DA ROCHA", "funcao": "BETONEIRO"},
    {"matricula": "2927", "nome": "FRANCISCO JEFFERSON RODRIGUES DOS SANTOS", "funcao": "SERVENTE"},
    {"matricula": "2931", "nome": "FRANCISCO JOCIVANE DA SILVA", "funcao": "CARPINTEIRO"},
    {"matricula": "2935", "nome": "FRANCISCO JOSÉ DE CASTRO", "funcao": "SERVENTE"},
    {"matricula": "2929", "nome": "FRANCISCO REBOUÇAS FERREIRA- GHCC", "funcao": "ENCARREGADO DE CARPINTARIA"},
    {"matricula": "2928", "nome": "FRANCISCO SAVIO LIMA PINTO", "funcao": "CARPINTEIRO"},
    {"matricula": "1588", "nome": "JOSE ARIMAR DE OLIVEIRA", "funcao": "PEDREIRO"},
    {"matricula": "2941", "nome": "LUCAS IRINEU ALVES- GHCC", "funcao": "TÉC. EM SEGURANÇA DO TRABALHO"},
    {"matricula": "2942", "nome": "LUIZ CARLOS OLIVEIRA - GHCC", "funcao": "ALMOXARIFE"},
    {"matricula": "2932", "nome": "NAEVÂNIO DA SILVA FERREIRA", "funcao": "AUXILIAR DE CARPINTARIA"},
    {"matricula": "1178", "nome": "RAIMUNDO NONATO FERREIRA - FERREIRO", "funcao": "FERREIRO"},
    {"matricula": "2936", "nome": "RENAM VIEIRA SOUSA", "funcao": "SERVENTE"}
]

def salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_json(arquivo, padrao):
    if arquivo == ARQUIVO_COLABORADORES:
        if not os.path.exists(arquivo):
            salvar_json(arquivo, COLABORADORES_INICIAIS)
            return COLABORADORES_INICIAIS
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if not dados:
                    salvar_json(arquivo, COLABORADORES_INICIAIS)
                    return COLABORADORES_INICIAIS
                return dados
        except:
            salvar_json(arquivo, COLABORADORES_INICIAIS)
            return COLABORADORES_INICIAIS
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados if dados is not None else padrao
        except:
            return padrao
    return padrao

class SistemaEPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brava Construções - Gestão de EPIs e Colaboradores")
        try:
            self.root.state('zoomed')
        except:
            self.root.geometry("1024x768")

        self.root.configure(bg="#0a0a0a")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background="#0a0a0a", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#141414", foreground="#009b3a", padding=[12, 8], font=("Arial", 10, "bold"))
        self.style.map('TNotebook.Tab', background=[('selected', '#009b3a')], foreground=[('selected', '#ffdf00')])

        if not os.path.exists(ARQUIVO_COLABORADORES):
            salvar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)

        self.criar_tela_login()

    def criar_tela_login(self):
        self.login_container = tk.Frame(self.root, bg="#0a0a0a")
        self.login_container.pack(fill="both", expand=True)

        self.login_frame = tk.Frame(self.login_container, bg="#141414", padx=45, pady=45, highlightbackground="#009b3a", highlightthickness=2)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        try:
            self.img_capacete = tk.PhotoImage(file="capacete.png")
            img_reduzida = self.img_capacete.subsample(2, 2) 
            lbl_imagem = tk.Label(self.login_frame, image=img_reduzida, bg="#141414")
            lbl_imagem.image = img_reduzida 
            lbl_imagem.pack(pady=(0, 10))
        except:
            pass

        tk.Label(self.login_frame, text="👷 Brava Construções", font=("Arial", 20, "bold"), fg="#ffdf00", bg="#141414").pack(pady=(0, 5))
        tk.Label(self.login_frame, text="Controle de Estoque e EPIs", font=("Arial", 11), fg="#cccccc", bg="#141414").pack(pady=(0, 20))

        tk.Label(self.login_frame, text="Usuário / Responsável:", font=("Arial", 10, "bold"), fg="#009b3a", bg="#141414").pack(anchor="w", pady=(5, 2))
        self.entry_usuario = ttk.Entry(self.login_frame, width=32, font=("Arial", 11))
        self.entry_usuario.pack(pady=(0, 10), ipady=3)
        # Removido o preenchimento automático do usuário

        tk.Label(self.login_frame, text="Senha:", font=("Arial", 10, "bold"), fg="#009b3a", bg="#141414").pack(anchor="w", pady=(5, 2))
        
        # Frame para agrupar a senha e o botão de ver/ocultar
        frame_senha = tk.Frame(self.login_frame, bg="#141414")
        frame_senha.pack(fill="x", pady=(0, 15))

        self.entry_senha = ttk.Entry(frame_senha, width=25, show="*", font=("Arial", 11))
        self.entry_senha.pack(side="left", ipady=3)
        # Removido o preenchimento automático da senha

        def alternar_visibilidade_senha():
            if self.entry_senha.cget('show') == '*':
                self.entry_senha.config(show='')
                btn_ver_senha.config(text="🙈 Ocultar")
            else:
                self.entry_senha.config(show='*')
                btn_ver_senha.config(text="👁️ Ver")

        btn_ver_senha = tk.Button(
            frame_senha, text="👁️ Ver", command=alternar_visibilidade_senha,
            font=("Arial", 9, "bold"), bg="#333333", fg="#ffffff", activebackground="#444444",
            activeforeground="#ffdf00", relief="flat", cursor="hand2", padx=8, pady=3
        )
        btn_ver_senha.pack(side="left", padx=(5, 0))

        btn_entrar = tk.Button(
            self.login_frame, text="Entrar no Sistema", command=self.verificar_login,
            font=("Arial", 11, "bold"), bg="#009b3a", fg="#ffffff", activebackground="#007a2d",
            activeforeground="#ffdf00", relief="flat", cursor="hand2", padx=10, pady=8
        )
        btn_entrar.pack(fill="x", pady=5)

        btn_cad_tst = tk.Button(
            self.login_frame, text="Cadastrar Novo TST", command=self.abrir_janela_cadastro_tst,
            font=("Arial", 9, "bold"), bg="#222222", fg="#ffdf00", activebackground="#333333",
            activeforeground="#ffffff", relief="flat", cursor="hand2", padx=10, pady=5
        )
        btn_cad_tst.pack(fill="x", pady=(5, 0))

        btn_fechar = tk.Button(
            self.login_frame, text="❌ Fechar Sistema", command=self.root.destroy,
            font=("Arial", 9, "bold"), bg="#cc0000", fg="#ffffff", activebackground="#990000",
            activeforeground="#ffffff", relief="flat", cursor="hand2", padx=10, pady=5
        )
        btn_fechar.pack(fill="x", pady=(5, 0))

    def validar_senha_forte(self, senha):
        if len(senha) < 8:
            return "A senha deve ter pelo menos 8 caracteres."
        if not re.search(r'[A-Z]', senha):
            return "A senha deve conter pelo menos 1 letra maiúscula."
        if not re.search(r'[a-z]', senha):
            return "A senha deve conter letras minúsculas."
        if not re.search(r'[0-9]', senha):
            return "A senha deve conter números."
        if not re.search(r'[^A-Za-z0-9]', senha):
            return "A senha deve conter pelo menos 1 caractere especial (ex: @, #, $, !, etc.)."
        return None

    def abrir_janela_cadastro_tst(self):
        janela_tst = tk.Toplevel(self.root)
        janela_tst.title("Cadastro de Novo TST")
        janela_tst.geometry("420x260")
        janela_tst.configure(bg="#141414")
        janela_tst.grab_set()

        tk.Label(janela_tst, text="👷 Cadastro de Novo TST", font=("Arial", 14, "bold"), fg="#ffdf00", bg="#141414").pack(pady=15)

        tk.Label(janela_tst, text="Nome / Usuário do TST:", font=("Arial", 9, "bold"), fg="#009b3a", bg="#141414").pack(anchor="w", padx=30)
        e_nome_tst = ttk.Entry(janela_tst, width=32, font=("Arial", 10))
        e_nome_tst.pack(padx=30, pady=3, ipady=3)

        def salvar_novo_tst():
            nome = e_nome_tst.get().strip().upper()
            if not nome:
                messagebox.showerror("Erro", "Preencha o nome do TST!", parent=janela_tst)
                return

            usuarios = carregar_json(ARQUIVO_USUARIOS, [])
            if any(u["usuario"].upper() == nome for u in usuarios):
                messagebox.showerror("Erro", "Este usuário já está cadastrado!", parent=janela_tst)
                return

            usuarios.append({"usuario": nome, "senha": "12345678", "mudar_senha": True})
            salvar_json(ARQUIVO_USUARIOS, usuarios)
            messagebox.showinfo("Sucesso", f"TST '{nome}' cadastrado!\nSenha padrão inicial: 12345678\nO usuário deverá alterá-la no primeiro acesso.", parent=janela_tst)
            janela_tst.destroy()

        btn_salvar = tk.Button(
            janela_tst, text="Cadastrar TST (Senha Padrão 12345678)", command=salvar_novo_tst,
            font=("Arial", 9, "bold"), bg="#009b3a", fg="#ffffff", relief="flat", cursor="hand2", padx=10, pady=6
        )
        btn_salvar.pack(pady=20)

    def abrir_janela_alterar_senha(self, usuario_nome):
        janela_alt = tk.Toplevel(self.root)
        janela_alt.title("Alteração de Senha Obrigatória")
        janela_alt.geometry("420x320")
        janela_alt.configure(bg="#141414")
        janela_alt.grab_set()

        tk.Label(janela_alt, text="🔒 Primeiro Acesso", font=("Arial", 14, "bold"), fg="#ffdf00", bg="#141414").pack(pady=10)
        tk.Label(janela_alt, text="Por favor, cadastre uma nova senha forte.", font=("Arial", 9), fg="#cccccc", bg="#141414").pack(pady=(0, 10))

        tk.Label(janela_alt, text="Nova Senha (8+ chars, Maiúscula, Especial, etc):", font=("Arial", 9, "bold"), fg="#009b3a", bg="#141414").pack(anchor="w", padx=30)
        e_nova_senha = ttk.Entry(janela_alt, width=32, show="*", font=("Arial", 10))
        e_nova_senha.pack(padx=30, pady=3, ipady=3)

        def salvar_nova_senha():
            nova = e_nova_senha.get().strip()
            erro = self.validar_senha_forte(nova)
            if erro:
                messagebox.showerror("Senha Inválida", erro, parent=janela_alt)
                return

            usuarios = carregar_json(ARQUIVO_USUARIOS, [])
            for u in usuarios:
                if u["usuario"].upper() == usuario_nome.upper():
                    u["senha"] = nova
                    u["mudar_senha"] = False
                    break
            salvar_json(ARQUIVO_USUARIOS, usuarios)
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso! Entrando no sistema...", parent=janela_alt)
            janela_alt.destroy()
            self.usuario_atual = usuario_nome.upper()
            self.login_container.destroy()
            self.iniciar_sistema_principal()

        btn_alt = tk.Button(
            janela_alt, text="Salvar Nova Senha e Entrar", command=salvar_nova_senha,
            font=("Arial", 10, "bold"), bg="#009b3a", fg="#ffffff", relief="flat", cursor="hand2", padx=10, pady=6
        )
        btn_alt.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        usuarios_cadastrados = carregar_json(ARQUIVO_USUARIOS, [])
        tst_encontrado = next((u for u in usuarios_cadastrados if u["usuario"].upper() == usuario.upper() and u["senha"] == senha), None)

        if (senha == "Penin@54" and usuario != ""):
            self.usuario_atual = usuario.upper()
            self.login_container.destroy()
            self.iniciar_sistema_principal()
        elif tst_encontrado:
            if tst_encontrado.get("mudar_senha", False):
                self.abrir_janela_alterar_senha(tst_encontrado["usuario"])
            else:
                self.usuario_atual = usuario.upper()
                self.login_container.destroy()
                self.iniciar_sistema_principal()
        else:
            messagebox.showerror("Erro de Acesso", "Usuário ou Senha inválidos!")

    def iniciar_sistema_principal(self):
        topo_frame = tk.Frame(self.root, bg="#141414", highlightbackground="#009b3a", highlightthickness=1)
        topo_frame.pack(fill="x", side="top")
        
        tk.Label(topo_frame, text=f"👤 Logado como: {self.usuario_atual}", font=("Arial", 10, "bold"), bg="#141414", fg="#ffdf00").pack(side="left", padx=15, pady=10)
        tk.Button(topo_frame, text="Sair / Trocar Usuário", command=self.sair_sistema, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").pack(side="right", padx=15, pady=8)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_produtos = tk.Frame(self.root, bg="#0a0a0a")
        self.notebook.add(self.frame_produtos, text="📦 1. Estoque / EPIs")
        self.construir_aba_produtos()

        self.frame_colab = tk.Frame(self.root, bg="#0a0a0a")
        self.notebook.add(self.frame_colab, text="👥 2. Colaboradores")
        self.construir_aba_colaboradores()

        self.frame_entrega = tk.Frame(self.root, bg="#0a0a0a")
        self.notebook.add(self.frame_entrega, text="🛡️ 3. Entrega")
        self.construir_aba_entrega()

        self.frame_hist = tk.Frame(self.root, bg="#0a0a0a")
        self.notebook.add(self.frame_hist, text="📜 4. Histórico de Entregas")
        self.construir_aba_historico()

    def sair_sistema(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.criar_tela_login()

    def criar_bloco(self, pai, texto):
        f = tk.LabelFrame(pai, text=f" {texto} ", bg="#141414", fg="#ffdf00", font=("Arial", 10, "bold"), bd=2, relief="groove")
        f.config(highlightbackground="#009b3a", highlightthickness=1)
        return f

    # ==================== ABA 1 ====================
    def construir_aba_produtos(self):
        tk.Label(self.frame_produtos, text="Gerenciamento de Códigos, Tamanhos e Estoque", font=("Arial", 11, "bold"), bg="#0a0a0a", fg="#009b3a").pack(pady=10)

        f1 = self.criar_bloco(self.frame_produtos, "Adicionar Novo Item / Código, Tamanho e Quantidade em Estoque")
        f1.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f1, text="Código:", bg="#141414", fg="#ffffff").grid(row=0, column=0, sticky="w", padx=3)
        self.e_cod = ttk.Entry(f1, width=10)
        self.e_cod.grid(row=0, column=1, padx=3, pady=5)

        tk.Label(f1, text="Descrição:", bg="#141414", fg="#ffffff").grid(row=0, column=2, sticky="w", padx=3)
        self.e_desc = ttk.Entry(f1, width=22)
        self.e_desc.grid(row=0, column=3, padx=3, pady=5)

        tk.Label(f1, text="Tam:", bg="#141414", fg="#ffffff").grid(row=0, column=4, sticky="w", padx=3)
        self.e_tam = ttk.Entry(f1, width=6)
        self.e_tam.grid(row=0, column=5, padx=3, pady=5)

        tk.Label(f1, text="CA:", bg="#141414", fg="#ffffff").grid(row=0, column=6, sticky="w", padx=3)
        self.e_ca = ttk.Entry(f1, width=8)
        self.e_ca.grid(row=0, column=7, padx=3, pady=5)

        tk.Label(f1, text="Qtd Estoque:", bg="#141414", fg="#ffffff").grid(row=0, column=8, sticky="w", padx=3)
        self.e_qtd_estoque = ttk.Entry(f1, width=8)
        self.e_qtd_estoque.grid(row=0, column=9, padx=3, pady=5)

        tk.Button(f1, text="Cadastrar", command=self.salvar_novo_produto, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=10, padx=8)

        f2 = self.criar_bloco(self.frame_produtos, "Lista de Produtos Cadastrados")
        f2.pack(fill="both", expand=True, padx=15, pady=10, ipadx=5, ipady=5)

        self.tree_prod = ttk.Treeview(f2, columns=("codigo", "descricao", "tamanho", "ca", "estoque"), show="headings", height=12)
        for col, txt, larg, alinh in [("codigo", "Código", 90, "center"), ("descricao", "Descrição do EPI", 340, "w"), ("tamanho", "Tamanho", 80, "center"), ("ca", "CA", 90, "center"), ("estoque", "Qtd Estoque", 90, "center")]:
            self.tree_prod.heading(col, text=txt)
            self.tree_prod.column(col, width=larg, anchor=alinh)
        self.tree_prod.pack(side="left", fill="both", expand=True)

        sc = ttk.Scrollbar(f2, orient="vertical", command=self.tree_prod.yview)
        sc.pack(side="right", fill="y")
        self.tree_prod.configure(yscrollcommand=sc.set)
        self.tree_prod.bind("<<TreeviewSelect>>", self.carregar_produto_selecionado)

        f3 = self.criar_bloco(self.frame_produtos, "Alterar / Editar Item Selecionado")
        f3.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f3, text="Cód:", bg="#141414", fg="#ffffff").grid(row=0, column=0, padx=2)
        self.e_edit_cod = ttk.Entry(f3, width=9)
        self.e_edit_cod.grid(row=0, column=1, padx=2)

        tk.Label(f3, text="Desc:", bg="#141414", fg="#ffffff").grid(row=0, column=2, padx=2)
        self.e_edit_desc = ttk.Entry(f3, width=22)
        self.e_edit_desc.grid(row=0, column=3, padx=2)

        tk.Label(f3, text="Tam:", bg="#141414", fg="#ffffff").grid(row=0, column=4, padx=2)
        self.e_edit_tam = ttk.Entry(f3, width=6)
        self.e_edit_tam.grid(row=0, column=5, padx=2)

        tk.Label(f3, text="CA:", bg="#141414", fg="#ffffff").grid(row=0, column=6, padx=2)
        self.e_edit_ca = ttk.Entry(f3, width=8)
        self.e_edit_ca.grid(row=0, column=7, padx=2)

        tk.Label(f3, text="Estoque:", bg="#141414", fg="#ffffff").grid(row=0, column=8, padx=2)
        self.e_edit_estoque = ttk.Entry(f3, width=8)
        self.e_edit_estoque.grid(row=0, column=9, padx=2)

        tk.Button(f3, text="💾 Salvar", command=self.atualizar_produto_selecionado, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=10, padx=6)
        tk.Button(f3, text="🗑️ Excluir", command=self.excluir_produto_selecionado, bg="#cc0000", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=11, padx=4)

        self.atualizar_tabela_produtos()

    def atualizar_tabela_produtos(self):
        for row in self.tree_prod.get_children():
            self.tree_prod.delete(row)
        produtos = carregar_json(ARQUIVO_PRODUTOS, [])
        for p in produtos:
            self.tree_prod.insert("", "end", values=(p["codigo"], p["descricao"], p.get("tamanho", ""), p["ca"], p.get("estoque", 0)))
        if hasattr(self, 'combo_prod'):
            self.combo_prod['values'] = [f"Cód: {p['codigo']} - {p['descricao']} (CA: {p['ca']} | Estoque: {p.get('estoque', 0)})" for p in produtos]

    def salvar_novo_produto(self):
        cod, desc, tam, ca, qtd_est = self.e_cod.get().strip(), self.e_desc.get().strip(), self.e_tam.get().strip(), self.e_ca.get().strip(), self.e_qtd_estoque.get().strip()
        if not cod or not desc:
            messagebox.showerror("Erro", "Preencha o código e a descrição!")
            return
        try:
            estoque = int(qtd_est) if qtd_est else 0
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            return
        produtos = carregar_json(ARQUIVO_PRODUTOS, [])
        produtos.append({"codigo": cod, "descricao": desc, "tamanho": tam, "ca": ca, "estoque": estoque})
        salvar_json(ARQUIVO_PRODUTOS, produtos)
        messagebox.showinfo("Sucesso", "Produto cadastrado!")
        for e in [self.e_cod, self.e_desc, self.e_tam, self.e_ca, self.e_qtd_estoque]:
            e.delete(0, tk.END)
        self.atualizar_tabela_produtos()

    def carregar_produto_selecionado(self, event):
        sel = self.tree_prod.selection()
        if sel:
            v = self.tree_prod.item(sel[0], "values")
            for e, val in zip([self.e_edit_cod, self.e_edit_desc, self.e_edit_tam, self.e_edit_ca, self.e_edit_estoque], v):
                e.delete(0, tk.END)
                e.insert(0, val)

    def atualizar_produto_selecionado(self):
        sel = self.tree_prod.selection()
        if not sel: return
        old = self.tree_prod.item(sel[0], "values")
        produtos = carregar_json(ARQUIVO_PRODUTOS, [])
        for p in produtos:
            if str(p["codigo"]) == str(old[0]):
                p["codigo"] = self.e_edit_cod.get().strip()
                p["descricao"] = self.e_edit_desc.get().strip()
                p["tamanho"] = self.e_edit_tam.get().strip()
                p["ca"] = self.e_edit_ca.get().strip()
                p["estoque"] = int(self.e_edit_estoque.get().strip() or 0)
                break
        salvar_json(ARQUIVO_PRODUTOS, produtos)
        self.atualizar_tabela_produtos()
        messagebox.showinfo("Sucesso", "Atualizado com sucesso!")

    def excluir_produto_selecionado(self):
        sel = self.tree_prod.selection()
        if not sel: return
        v = self.tree_prod.item(sel[0], "values")
        if messagebox.askyesno("Confirmação", "Excluir item?"):
            produtos = carregar_json(ARQUIVO_PRODUTOS, [])
            produtos = [p for p in produtos if str(p["codigo"]) != str(v[0])]
            salvar_json(ARQUIVO_PRODUTOS, produtos)
            self.atualizar_tabela_produtos()

    # ==================== ABA 2 ====================
    def construir_aba_colaboradores(self):
        topo_colab = tk.Frame(self.frame_colab, bg="#0a0a0a")
        topo_colab.pack(fill="x", padx=15, pady=8)
        tk.Label(topo_colab, text="Gerenciamento e Cadastro de Colaboradores", font=("Arial", 11, "bold"), bg="#0a0a0a", fg="#009b3a").pack(side="left")
        self.lbl_total_obra = tk.Label(topo_colab, text="👷 Total na Obra: 0", font=("Arial", 11, "bold"), bg="#0a0a0a", fg="#ffdf00")
        self.lbl_total_obra.pack(side="right", padx=5)

        f1 = self.criar_bloco(self.frame_colab, "Adicionar Novo Colaborador")
        f1.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f1, text="Matrícula:", bg="#141414", fg="#ffffff").grid(row=0, column=0, sticky="w", padx=3)
        self.e_mat = ttk.Entry(f1, width=12)
        self.e_mat.grid(row=0, column=1, padx=3, pady=5)

        tk.Label(f1, text="Nome Completo:", bg="#141414", fg="#ffffff").grid(row=0, column=2, sticky="w", padx=3)
        self.e_nome = ttk.Entry(f1, width=32)
        self.e_nome.grid(row=0, column=3, padx=3, pady=5)

        tk.Label(f1, text="Função:", bg="#141414", fg="#ffffff").grid(row=0, column=4, sticky="w", padx=3)
        self.e_func = ttk.Entry(f1, width=22)
        self.e_func.grid(row=0, column=5, padx=3, pady=5)

        tk.Button(f1, text="Cadastrar", command=self.salvar_novo_colaborador, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=6, padx=8)

        f2 = self.criar_bloco(self.frame_colab, "Lista de Colaboradores Cadastrados (Clique para selecionar e editar)")
        f2.pack(fill="both", expand=True, padx=15, pady=10, ipadx=5, ipady=5)

        self.tree_colab = ttk.Treeview(f2, columns=("matricula", "nome", "funcao"), show="headings", height=12)
        for col, txt, larg, alinh in [("matricula", "Matrícula", 110, "center"), ("nome", "Nome Completo", 420, "w"), ("funcao", "Função", 260, "w")]:
            self.tree_colab.heading(col, text=txt)
            self.tree_colab.column(col, width=larg, anchor=alinh)
        self.tree_colab.pack(side="left", fill="both", expand=True)

        sc = ttk.Scrollbar(f2, orient="vertical", command=self.tree_colab.yview)
        sc.pack(side="right", fill="y")
        self.tree_colab.configure(yscrollcommand=sc.set)
        self.tree_colab.bind("<<TreeviewSelect>>", self.carregar_colaborador_selecionado)

        f3 = self.criar_bloco(self.frame_colab, "Alterar / Editar ou Excluir Colaborador Selecionado")
        f3.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f3, text="Matrícula:", bg="#141414", fg="#ffffff").grid(row=0, column=0, padx=2)
        self.e_edit_mat = ttk.Entry(f3, width=12)
        self.e_edit_mat.grid(row=0, column=1, padx=2)

        tk.Label(f3, text="Nome:", bg="#141414", fg="#ffffff").grid(row=0, column=2, padx=2)
        self.e_edit_nome = ttk.Entry(f3, width=32)
        self.e_edit_nome.grid(row=0, column=3, padx=2)

        tk.Label(f3, text="Função:", bg="#141414", fg="#ffffff").grid(row=0, column=4, padx=2)
        self.e_edit_func = ttk.Entry(f3, width=22)
        self.e_edit_func.grid(row=0, column=5, padx=2)

        tk.Button(f3, text="💾 Salvar", command=self.atualizar_colaborador_selecionado, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=6, padx=6)
        tk.Button(f3, text="🗑️ Excluir", command=self.excluir_colaborador_selecionado, bg="#cc0000", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=7, padx=4)

        self.atualizar_tabela_colaboradores()

    def atualizar_tabela_colaboradores(self):
        for row in self.tree_colab.get_children():
            self.tree_colab.delete(row)
        colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
        for c in colaboradores:
            self.tree_colab.insert("", "end", values=(c["matricula"], c["nome"], c["funcao"]))
        if hasattr(self, 'lbl_total_obra'):
            self.lbl_total_obra.config(text=f"👷 Total na Obra: {len(colaboradores)}")

    def salvar_novo_colaborador(self):
        mat = self.e_mat.get().strip()
        nome = self.e_nome.get().strip().upper()
        func = self.e_func.get().strip().upper()
        if not mat or not nome:
            messagebox.showerror("Erro", "Preencha a matrícula e o nome!")
            return
        colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
        if any(str(c["matricula"]).strip() == mat for c in colaboradores):
            messagebox.showerror("Erro", f"Já existe matrícula {mat}!")
            return
        colaboradores.append({"matricula": mat, "nome": nome, "funcao": func})
        salvar_json(ARQUIVO_COLABORADORES, colaboradores)
        messagebox.showinfo("Sucesso", "Cadastrado com sucesso!")
        self.e_mat.delete(0, tk.END)
        self.e_nome.delete(0, tk.END)
        self.e_func.delete(0, tk.END)
        self.atualizar_tabela_colaboradores()

    def carregar_colaborador_selecionado(self, event):
        sel = self.tree_colab.selection()
        if sel:
            v = self.tree_colab.item(sel[0], "values")
            self.e_edit_mat.delete(0, tk.END)
            self.e_edit_mat.insert(0, v[0])
            self.e_edit_nome.delete(0, tk.END)
            self.e_edit_nome.insert(0, v[1])
            self.e_edit_func.delete(0, tk.END)
            self.e_edit_func.insert(0, v[2])

    def atualizar_colaborador_selecionado(self):
        sel = self.tree_colab.selection()
        if not sel: return
        old = self.tree_colab.item(sel[0], "values")
        colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
        for c in colaboradores:
            if str(c["matricula"]).strip() == str(old[0]).strip():
                c["matricula"] = self.e_edit_mat.get().strip()
                c["nome"] = self.e_edit_nome.get().strip().upper()
                c["funcao"] = self.e_edit_func.get().strip().upper()
                break
        salvar_json(ARQUIVO_COLABORADORES, colaboradores)
        self.atualizar_tabela_colaboradores()
        messagebox.showinfo("Sucesso", "Atualizado com sucesso!")

    def excluir_colaborador_selecionado(self):
        sel = self.tree_colab.selection()
        if not sel: return
        v = self.tree_colab.item(sel[0], "values")
        if messagebox.askyesno("Confirmação", f"Remover {v[1]}?"):
            colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
            colaboradores = [c for c in colaboradores if str(c["matricula"]).strip() != str(v[0]).strip()]
            salvar_json(ARQUIVO_COLABORADORES, colaboradores)
            self.atualizar_tabela_colaboradores()

    # ==================== ABA 3 ====================
    def construir_aba_entrega(self):
        tk.Label(self.frame_entrega, text="Registro de Entrega de EPI", font=("Arial", 11, "bold"), bg="#0a0a0a", fg="#009b3a").pack(pady=10)
        
        f1 = self.criar_bloco(self.frame_entrega, "Dados da Entrega")
        f1.pack(fill="both", expand=True, padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f1, text="Matrícula do Colaborador:", bg="#141414", fg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.var_matricula = tk.StringVar()
        self.var_matricula.trace_add("write", lambda *args: self.buscar_colaborador_automatico())
        ttk.Entry(f1, textvariable=self.var_matricula, width=20).grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.lbl_info_colab = tk.Label(f1, text="Colaborador: [Aguardando...]", font=("Arial", 10, "bold"), bg="#141414", fg="#ffdf00")
        self.lbl_info_colab.grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        tk.Label(f1, text="Produto (EPI):", bg="#141414", fg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_prod = ttk.Combobox(f1, width=65, state="readonly")
        self.combo_prod.grid(row=2, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        produtos = carregar_json(ARQUIVO_PRODUTOS, [])
        self.combo_prod['values'] = [f"Cód: {p['codigo']} - {p['descricao']} (CA: {p['ca']} | Estoque: {p.get('estoque', 0)})" for p in produtos]

        tk.Label(f1, text="Quantidade Entregue:", bg="#141414", fg="#ffffff").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.e_qtd_entrega = ttk.Entry(f1, width=10)
        self.e_qtd_entrega.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.e_qtd_entrega.insert(0, "1")

        tk.Button(f1, text="✅ Registrar Entrega", command=self.salvar_entrega, bg="#009b3a", fg="#ffffff", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", padx=10, pady=5).grid(row=4, column=1, pady=15, sticky="w")

    def buscar_colaborador_automatico(self):
        mat = self.var_matricula.get().strip()
        if not mat:
            self.lbl_info_colab.config(text="Colaborador: [Aguardando...]", fg="#ffdf00")
            self.colab_encontrado = None
            return
        colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
        match = next((c for c in colaboradores if str(c['matricula']).strip() == mat), None)
        if match:
            self.colab_encontrado = match
            self.lbl_info_colab.config(text=f"✅ {match['nome']} - Função: {match['funcao']}", fg="#009b3a")
        else:
            self.colab_encontrado = None
            self.lbl_info_colab.config(text="⚠️ Matrícula não encontrada", fg="#ff4444")

    def salvar_entrega(self):
        if not hasattr(self, 'colab_encontrado') or not self.colab_encontrado:
            messagebox.showerror("Erro", "Selecione um colaborador válido!")
            return
        selecao_prod = self.combo_prod.get()
        if not selecao_prod:
            messagebox.showerror("Erro", "Selecione um EPI!")
            return
        try:
            qtd = int(self.e_qtd_entrega.get().strip())
            if qtd <= 0: raise ValueError()
        except:
            messagebox.showerror("Erro", "Quantidade inválida!")
            return
        
        codigo_prod = selecao_prod.split(" - ")[0].replace("Cód: ", "").strip()
        produtos = carregar_json(ARQUIVO_PRODUTOS, [])
        produto_obj = next((p for p in produtos if str(p['codigo']) == str(codigo_prod)), None)
        if not produto_obj: return

        produto_obj["estoque"] = produto_obj.get("estoque", 0) - qtd
        salvar_json(ARQUIVO_PRODUTOS, produtos)
        self.atualizar_tabela_produtos()

        entregas = carregar_json(ARQUIVO_ENTREGAS, [])
        entregas.insert(0, {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "matricula": self.colab_encontrado["matricula"],
            "nome": self.colab_encontrado["nome"],
            "produto": f"{produto_obj['descricao']} (CA: {produto_obj['ca']})",
            "quantidade": qtd,
            "responsavel": self.usuario_atual
        })
        salvar_json(ARQUIVO_ENTREGAS, entregas)
        self.atualizar_tabela_historico()
        messagebox.showinfo("Sucesso", "Entrega registrada!")
        self.var_matricula.set("")
        self.combo_prod.set("")
        self.e_qtd_entrega.delete(0, tk.END)
        self.e_qtd_entrega.insert(0, "1")

    # ==================== ABA 4 ====================
    def construir_aba_historico(self):
        tk.Label(self.frame_hist, text="Histórico Geral de Entregas de EPIs", font=("Arial", 11, "bold"), bg="#0a0a0a", fg="#009b3a").pack(pady=10)
        
        f1 = self.criar_bloco(self.frame_hist, "Lista de Registros de Entregas")
        f1.pack(fill="both", expand=True, padx=15, pady=5, ipadx=5, ipady=5)

        self.tree_hist = ttk.Treeview(f1, columns=("data", "mat", "nome", "prod", "qtd", "resp"), show="headings", height=12)
        for col, txt, larg, alinh in [("data", "Data / Hora", 130, "center"), ("mat", "Matrícula", 90, "center"), ("nome", "Colaborador", 280, "w"), ("prod", "EPI Entregue", 260, "w"), ("qtd", "Qtd", 60, "center"), ("resp", "Responsável", 120, "center")]:
            self.tree_hist.heading(col, text=txt)
            self.tree_hist.column(col, width=larg, anchor=alinh)
        self.tree_hist.pack(side="left", fill="both", expand=True)
        self.tree_hist.bind("<<TreeviewSelect>>", self.carregar_historico_selecionado)

        sc = ttk.Scrollbar(f1, orient="vertical", command=self.tree_hist.yview)
        sc.pack(side="right", fill="y")
        self.tree_hist.configure(yscrollcommand=sc.set)

        f2 = self.criar_bloco(self.frame_hist, "Alterar / Editar Item Selecionado")
        f2.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

        tk.Label(f2, text="Data:", bg="#141414", fg="#ffffff").grid(row=0, column=0, padx=2)
        self.e_hist_data = ttk.Entry(f2, width=13)
        self.e_hist_data.grid(row=0, column=1, padx=2)

        tk.Label(f2, text="Mat:", bg="#141414", fg="#ffffff").grid(row=0, column=2, padx=2)
        self.e_hist_mat = ttk.Entry(f2, width=8)
        self.e_hist_mat.grid(row=0, column=3, padx=2)

        tk.Label(f2, text="Nome:", bg="#141414", fg="#ffffff").grid(row=0, column=4, padx=2)
        self.e_hist_nome = ttk.Entry(f2, width=22)
        self.e_hist_nome.grid(row=0, column=5, padx=2)

        tk.Label(f2, text="Produto:", bg="#141414", fg="#ffffff").grid(row=0, column=6, padx=2)
        self.e_hist_prod = ttk.Entry(f2, width=22)
        self.e_hist_prod.grid(row=0, column=7, padx=2)

        tk.Label(f2, text="Qtd:", bg="#141414", fg="#ffffff").grid(row=0, column=8, padx=2)
        self.e_hist_qtd = ttk.Entry(f2, width=5)
        self.e_hist_qtd.grid(row=0, column=9, padx=2)

        tk.Label(f2, text="Resp:", bg="#141414", fg="#ffffff").grid(row=0, column=10, padx=2)
        self.e_hist_resp = ttk.Entry(f2, width=10)
        self.e_hist_resp.grid(row=0, column=11, padx=2)

        tk.Button(f2, text="💾 Salvar", command=self.atualizar_historico_selecionado, bg="#009b3a", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=12, padx=6)
        tk.Button(f2, text="🗑️ Excluir", command=self.excluir_historico_selecionado, bg="#cc0000", fg="#ffffff", font=("Arial", 9, "bold"), relief="flat", cursor="hand2").grid(row=0, column=13, padx=4)

        self.atualizar_tabela_historico()

    def atualizar_tabela_historico(self):
        if not hasattr(self, 'tree_hist'): return
        for row in self.tree_hist.get_children():
            self.tree_hist.delete(row)
        for e in carregar_json(ARQUIVO_ENTREGAS, []):
            self.tree_hist.insert("", "end", values=(e.get("data"), e.get("matricula"), e.get("nome"), e.get("produto"), e.get("quantidade"), e.get("responsavel")))

    def carregar_historico_selecionado(self, event):
        sel = self.tree_hist.selection()
        if sel:
            v = self.tree_hist.item(sel[0], "values")
            for w, val in zip([self.e_hist_data, self.e_hist_mat, self.e_hist_nome, self.e_hist_prod, self.e_hist_qtd, self.e_hist_resp], v):
                w.delete(0, tk.END)
                w.insert(0, val)

    def atualizar_historico_selecionado(self):
        sel = self.tree_hist.selection()
        if not sel: return
        idx = self.tree_hist.index(sel[0])
        entregas = carregar_json(ARQUIVO_ENTREGAS, [])
        if 0 <= idx < len(entregas):
            try:
                qtd = int(self.e_hist_qtd.get().strip())
            except:
                return
            entregas[idx] = {
                "data": self.e_hist_data.get().strip(),
                "matricula": self.e_hist_mat.get().strip(),
                "nome": self.e_hist_nome.get().strip(),
                "produto": self.e_hist_prod.get().strip(),
                "quantidade": qtd,
                "responsavel": self.e_hist_resp.get().strip()
            }
            salvar_json(ARQUIVO_ENTREGAS, entregas)
            self.atualizar_tabela_historico()
            messagebox.showinfo("Sucesso", "Atualizado!")

    def excluir_historico_selecionado(self):
        sel = self.tree_hist.selection()
        if not sel: return
        if messagebox.askyesno("Confirmação", "Excluir registro?"):
            entregas = carregar_json(ARQUIVO_ENTREGAS, [])
            idx = self.tree_hist.index(sel[0])
            if 0 <= idx < len(entregas):
                entregas.pop(idx)
                salvar_json(ARQUIVO_ENTREGAS, entregas)
                self.atualizar_tabela_historico()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEPIApp(root)
    root.mainloop()