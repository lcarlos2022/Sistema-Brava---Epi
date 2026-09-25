import json
import os
import re
from datetime import datetime
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Brava Construções - Gestão de EPIs e Colaboradores",
    page_icon="👷",
    layout="wide",
)

# Estilização CSS refinada para forçar o fundo do container de login e cores
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Força o fundo escuro nos blocos de formulário e containers */
    div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background-color: #1a1c23 !important;
    }
    /* Estilo personalizado para o container de login */
    .login-box {
        background-color: #1a1c23 !important;
        padding: 35px !important;
        border-radius: 12px !important;
        border: 2px solid #009b3a !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    label, .stTextInput label, .stNumberInput label, .stSelectbox label, p, span {
        color: #ffffff !important;
    }
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #009b3a;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        color: #ffdf00;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Arquivos de Dados Locais
ARQUIVO_PRODUTOS = "produtos_epis.json"
ARQUIVO_COLABORADORES = "colaboradores_cadastrados.json"
ARQUIVO_ENTREGAS = "entregas_epi.json"
ARQUIVO_USUARIOS = "usuarios_tst.json"

COLABORADORES_INICIAIS = [
    {
        "matricula": "2924",
        "nome": "ABNOAN IRINEU DOS SANTOS",
        "funcao": "FERREIRO",
    },
    {
        "matricula": "2926",
        "nome": "CARLOS CARDOZO DO NASCIMENTO",
        "funcao": "SERVENTE",
    },
    {
        "matricula": "2940",
        "nome": "ERIVALDO GOMES SILVEIRA- GHCC",
        "funcao": "CARPINTEIRO",
    },
    {
        "matricula": "2923",
        "nome": "EVANDRO MATIAS DO NASCIMENTO",
        "funcao": "VIGIA",
    },
    {
        "matricula": "2933",
        "nome": "FERNANDO PROCOPIO DA SILVA",
        "funcao": "FERREIRO",
    },
    {
        "matricula": "2938",
        "nome": "FRANCISCO DAVI DA ROCHA",
        "funcao": "BETONEIRO",
    },
    {
        "matricula": "2927",
        "nome": "FRANCISCO JEFFERSON RODRIGUES DOS SANTOS",
        "funcao": "SERVENTE",
    },
    {
        "matricula": "2931",
        "nome": "FRANCISCO JOCIVANE DA SILVA",
        "funcao": "CARPINTEIRO",
    },
    {
        "matricula": "2935",
        "nome": "FRANCISCO JOSÉ DE CASTRO",
        "funcao": "SERVENTE",
    },
    {
        "matricula": "2929",
        "nome": "FRANCISCO REBOUÇAS FERREIRA- GHCC",
        "funcao": "ENCARREGADO DE CARPINTARIA",
    },
    {
        "matricula": "2928",
        "nome": "FRANCISCO SAVIO LIMA PINTO",
        "funcao": "CARPINTEIRO",
    },
    {"matricula": "1588", "nome": "JOSE ARIMAR DE OLIVEIRA", "funcao": "PEDREIRO"},
    {
        "matricula": "2941",
        "nome": "LUCAS IRINEU ALVES- GHCC",
        "funcao": "TÉC. EM SEGURANÇA DO TRABALHO",
    },
    {
        "matricula": "2942",
        "nome": "LUIZ CARLOS OLIVEIRA - GHCC",
        "funcao": "ALMOXARIFE",
    },
    {
        "matricula": "2932",
        "nome": "NAEVÂNIO DA SILVA FERREIRA",
        "funcao": "AUXILIAR DE CARPINTARIA",
    },
    {
        "matricula": "1178",
        "nome": "RAIMUNDO NONATO FERREIRA - FERREIRO",
        "funcao": "FERREIRO",
    },
    {"matricula": "2936", "nome": "RENAM VIEIRA SOUSA", "funcao": "SERVENTE"},
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


# Inicialização de Variáveis de Sessão
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
if "usuario_atual" not in st.session_state:
  st.session_state.usuario_atual = ""
if "mudar_senha" not in st.session_state:
  st.session_state.mudar_senha = False


def validar_senha_forte(senha):
  if len(senha) < 8:
    return "A senha deve ter pelo menos 8 caracteres."
  if not re.search(r"[A-Z]", senha):
    return "A senha deve conter pelo menos 1 letra maiúscula."
  if not re.search(r"[a-z]", senha):
    return "A senha deve conter letras minúsculas."
  if not re.search(r"[0-9]", senha):
    return "A senha deve conter números."
  if not re.search(r"[^A-Za-z0-9]", senha):
    return (
        "A senha deve conter pelo menos 1 caractere especial (ex: @, #, $, !,"
        " etc.)."
    )
  return None


# ==================== TELA DE LOGIN ====================
if not st.session_state.autenticado:
  st.markdown(
      "<h1 style='text-align: center; color: #ffdf00;'>👷 Brava Construções"
      "</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h3 style='text-align: center; color: #ffffff;'>Controle de Estoque e"
      " EPIs</h3>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 1.2, 1])

  with col2:
    # Usando a classe CSS dedicada 'login-box'
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    if st.session_state.get("tela_cadastro_tst"):
      st.markdown(
          "<h4 style='color: #ffdf00;'>Cadastro de Novo TST</h4>",
          unsafe_allow_html=True,
      )
      novo_tst_nome = st.text_input("Nome / Usuário do TST").strip().upper()
      if st.button("Salvar Cadastro TST"):
        if not novo_tst_nome:
          st.error("Preencha o nome do TST!")
        else:
          usuarios = carregar_json(ARQUIVO_USUARIOS, [])
          if any(u["usuario"].upper() == novo_tst_nome for u in usuarios):
            st.error("Este usuário já está cadastrado!")
          else:
            usuarios.append({
                "usuario": novo_tst_nome,
                "senha": "12345678",
                "mudar_senha": True,
            })
            salvar_json(ARQUIVO_USUARIOS, usuarios)
            st.success(
                f"TST '{novo_tst_nome}' cadastrado! Senha padrão inicial:"
                " 12345678"
            )
            st.session_state.tela_cadastro_tst = False
            st.rerun()

      if st.button("Voltar ao Login"):
        st.session_state.tela_cadastro_tst = False
        st.rerun()

    elif st.session_state.mudar_senha:
      st.markdown(
          "<h4 style='color: #ffdf00;'>🔒 Primeiro Acesso - Alterar Senha</h4>",
          unsafe_allow_html=True,
      )
      nova_senha_input = st.text_input("Nova Senha Forte", type="password")
      if st.button("Salvar Nova Senha e Entrar"):
        erro = validar_senha_forte(nova_senha_input)
        if erro:
          st.error(erro)
        else:
          usuarios = carregar_json(ARQUIVO_USUARIOS, [])
          for u in usuarios:
            if (
                u["usuario"].upper()
                == st.session_state.usuario_pendente.upper()
            ):
              u["senha"] = nova_senha_input
              u["mudar_senha"] = False
              break
          salvar_json(ARQUIVO_USUARIOS, usuarios)
          st.session_state.autenticado = True
          st.session_state.usuario_atual = (
              st.session_state.usuario_pendente.upper()
          )
          st.session_state.mudar_senha = False
          st.success("Senha alterada com sucesso!")
          st.rerun()

    else:
      usuario_input = st.text_input("Usuário / Responsável")
      senha_input = st.text_input("Senha", type="password")

      if st.button("Entrar no Sistema", use_container_width=True):
        u_clean = usuario_input.strip()
        s_clean = senha_input.strip()

        usuarios_cadastrados = carregar_json(ARQUIVO_USUARIOS, [])
        tst_encontrado = next(
            (
                u
                for u in usuarios_cadastrados
                if u["usuario"].upper() == u_clean.upper()
                and u["senha"] == s_clean
            ),
            None,
        )

        if s_clean == "Penin@54" and u_clean != "":
          st.session_state.autenticado = True
          st.session_state.usuario_atual = u_clean.upper()
          st.rerun()
        elif tst_encontrado:
          if tst_encontrado.get("mudar_senha", False):
            st.session_state.mudar_senha = True
            st.session_state.usuario_pendente = tst_encontrado["usuario"]
            st.rerun()
          else:
            st.session_state.autenticado = True
            st.session_state.usuario_atual = u_clean.upper()
            st.rerun()
        else:
          st.error("Usuário ou Senha inválidos!")

      if st.button("Cadastrar Novo TST", use_container_width=True):
        st.session_state.tela_cadastro_tst = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== SISTEMA PRINCIPAL ====================
else:
  topo1, topo2 = st.columns([4, 1])
  with topo1:
    st.markdown(
        f"👤 **Logado como:** `{st.session_state.usuario_atual}`",
        unsafe_allow_html=True,
    )
  with topo2:
    if st.button("Sair / Trocar Usuário"):
      st.session_state.autenticado = False
      st.session_state.usuario_atual = ""
      st.rerun()

  # Abas do Sistema
  aba_produtos, aba_colab, aba_entrega, aba_hist = st.tabs([
      "📦 1. Estoque / EPIs",
      "👥 2. Colaboradores",
      "🛡️ 3. Entrega",
      "📜 4. Histórico de Entregas",
  ])

  # --- ABA 1: PRODUTOS ---
  with aba_produtos:
    st.markdown(
        "<div class='main-header'>Gerenciamento de Códigos, Tamanhos e"
        " Estoque</div>",
        unsafe_allow_html=True,
    )

    with st.expander("➕ Adicionar Novo Item / EPI", expanded=True):
      with st.form("form_novo_produto"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
          c_cod = st.text_input("Código")
        with col2:
          c_desc = st.text_input("Descrição")
        with col3:
          c_tam = st.text_input("Tamanho")
        with col4:
          c_ca = st.text_input("CA")
        with col5:
          c_qtd = st.text_input("Qtd Estoque", "0")

        if st.form_submit_button("Cadastrar Produto"):
          if not c_cod or not c_desc:
            st.error("Preencha o código e a descrição!")
          else:
            try:
              estoque_val = int(c_qtd)
            except:
              estoque_val = 0
            produtos = carregar_json(ARQUIVO_PRODUTOS, [])
            produtos.append({
                "codigo": c_cod,
                "descricao": c_desc,
                "tamanho": c_tam,
                "ca": c_ca,
                "estoque": estoque_val,
            })
            salvar_json(ARQUIVO_PRODUTOS, produtos)
            st.success("Produto cadastrado com sucesso!")
            st.rerun()

    st.markdown(
        "<div class='sub-header'>Lista de Produtos Cadastrados</div>",
        unsafe_allow_html=True,
    )
    produtos = carregar_json(ARQUIVO_PRODUTOS, [])
    if produtos:
      for idx, p in enumerate(produtos):
        col_a, col_b, col_c, col_d, col_e, col_f = st.columns([1, 3, 1, 1, 1, 1])
        col_a.write(f"Cód: {p['codigo']}")
        col_b.write(f"{p['descricao']}")
        col_c.write(f"Tam: {p.get('tamanho', '')}")
        col_d.write(f"CA: {p['ca']}")
        col_e.write(f"Estoque: {p.get('estoque', 0)}")
        if col_f.button("🗑️ Excluir", key=f"del_prod_{idx}"):
          produtos.pop(idx)
          salvar_json(ARQUIVO_PRODUTOS, produtos)
          st.rerun()
    else:
      st.info("Nenhum produto cadastrado.")

  # --- ABA 2: COLABORADORES ---
  with aba_colab:
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
      st.markdown(
          "<div class='main-header'>Gerenciamento e Cadastro de"
          " Colaboradores</div>",
          unsafe_allow_html=True,
      )
    colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
    with col_t2:
      st.markdown(
          f"👷 **Total na Obra:** `{len(colaboradores)}`", unsafe_allow_html=True
      )

    with st.expander("➕ Adicionar Novo Colaborador", expanded=True):
      with st.form("form_novo_colab"):
        col1, col2, col3 = st.columns([1, 2, 1.5])
        with col1:
          m_mat = st.text_input("Matrícula")
        with col2:
          m_nome = st.text_input("Nome Completo")
        with col3:
          m_func = st.text_input("Função")

        if st.form_submit_button("Cadastrar Colaborador"):
          if not m_mat or not m_nome:
            st.error("Preencha a matrícula e o nome!")
          else:
            if any(
                str(c["matricula"]).strip() == m_mat.strip()
                for c in colaboradores
            ):
              st.error(f"Já existe uma matrícula {m_mat} cadastrada!")
            else:
              colaboradores.append({
                  "matricula": m_mat,
                  "nome": m_nome.upper(),
                  "funcao": m_func.upper(),
              })
              salvar_json(ARQUIVO_COLABORADORES, colaboradores)
              st.success("Colaborador cadastrado com sucesso!")
              st.rerun()

    st.markdown(
        "<div class='sub-header'>Lista de Colaboradores</div>",
        unsafe_allow_html=True,
    )
    if colaboradores:
      for idx, c in enumerate(colaboradores):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        col1.write(f"Mat: {c['matricula']}")
        col2.write(f"{c['nome']}")
        col3.write(f"Função: {c['funcao']}")
        if col4.button("🗑️ Excluir", key=f"del_col_{idx}"):
          colaboradores.pop(idx)
          salvar_json(ARQUIVO_COLABORADORES, colaboradores)
          st.rerun()

  # --- ABA 3: ENTREGA ---
  with aba_entrega:
    st.markdown(
        "<div class='main-header'>Registro de Entrega de EPI</div>",
        unsafe_allow_html=True,
    )

    mat_busca = st.text_input("Digite a Matrícula do Colaborador").strip()
    colab_selecionado = None
    if mat_busca:
      match = next(
          (
              c
              for c in carregar_json(
                  ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS
              )
              if str(c["matricula"]).strip() == mat_busca
          ),
          None,
      )
      if match:
        colab_selecionado = match
        st.success(
            f"✅ Colaborador: {match['nome']} — Função: {match['funcao']}"
        )
      else:
        st.error("⚠️ Matrícula não encontrada.")

    produtos = carregar_json(ARQUIVO_PRODUTOS, [])
    lista_opcoes_prod = [
        f"Cód: {p['codigo']} - {p['descricao']} (CA: {p['ca']} | Estoque:"
        f" {p.get('estoque', 0)})"
        for p in produtos
    ]

    prod_escolhido = st.selectbox("Selecione o EPI", lista_opcoes_prod)
    qtd_entrega = st.number_input(
        "Quantidade Entregue", min_value=1, value=1, step=1
    )

    if st.button("✅ Registrar Entrega"):
      if not colab_selecionado:
        st.error("Selecione um colaborador válido!")
      elif not prod_escolhido:
        st.error("Selecione um EPI!")
      else:
        entregas = carregar_json(ARQUIVO_ENTREGAS, [])
        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        entregas.append({
            "data": data_hora_atual,
            "matricula": colab_selecionado["matricula"],
            "colaborador": colab_selecionado["nome"],
            "produto": prod_escolhido,
            "quantidade": qtd_entrega,
            "responsavel": st.session_state.usuario_atual,
        })
        salvar_json(ARQUIVO_ENTREGAS, entregas)
        st.success("Entrega registrada com sucesso!")

  # --- ABA 4: HISTÓRICO ---
  with aba_hist:
    st.markdown(
        "<div class='main-header'>📜 Histórico de Entregas Realizadas</div>",
        unsafe_allow_html=True,
    )
    entregas = carregar_json(ARQUIVO_ENTREGAS, [])
    if entregas:
      for e in reversed(entregas):
        st.markdown(
            f"**Data:** {e['data']} | **Colaborador:** {e['colaborador']} (Mat:"
            f" {e['matricula']}) | **EPI:** {e['produto']} | **Qtd:**"
            f" {e['quantidade']} | **TST:** {e['responsavel']}"
        )
        st.divider()
    else:
      st.info("Nenhuma entrega registrada até o momento.")
