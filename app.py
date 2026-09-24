import json
import os
from datetime import datetime
import streamlit as st

# Configuração da Página para Otimizar no Celular e Notebook
st.set_page_config(
    page_title="Brava Construções - Gestão de EPIs",
    page_icon="👷",
    layout="wide",
)

# Estilização Visual Personalizada (Mantendo o Padrão do Sistema)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #ffdf00 !important;
    }
    .css-1dp5vir {
        background-color: #141414;
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
    {"matricula": "2924", "nome": "ABNOAN IRINEU DOS SANTOS", "funcao": "FERREIRO"},
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
    {"matricula": "2938", "nome": "FRANCISCO DAVI DA ROCHA", "funcao": "BETONEIRO"},
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


# Inicialização de Sessão para Login
if "logado" not in st.session_state:
  st.session_state.logado = False
  st.session_state.usuario = ""

# TELA DE LOGIN
if not st.session_state.logado:
  st.markdown(
      "<h2 style='text-align: center;'>👷 Brava Construções</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #cccccc;'>Controle de Estoque e"
      " EPIs</p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    usuario_input = st.text_input("Usuário / Responsável:")
    senha_input = st.text_input("Senha:", type="password")

    if st.button("Entrar no Sistema", use_container_width=True):
      usuarios_cadastrados = carregar_json(ARQUIVO_USUARIOS, [])
      tst_encontrado = next(
          (
              u
              for u in usuarios_cadastrados
              if u["usuario"].upper() == usuario_input.strip().upper()
              and u["senha"] == senha_input
          ),
          None,
      )

      if senha_input == "Penin@54" and usuario_input != "":
        st.session_state.logado = True
        st.session_state.usuario = usuario_input.upper()
        st.rerun()
      elif tst_encontrado:
        st.session_state.logado = True
        st.session_state.usuario = usuario_input.upper()
        st.rerun()
      else:
        st.error("Usuário ou Senha inválidos!")

else:
  # SISTEMA PRINCIPAL (COM ABAS)
  st.sidebar.markdown(f"👤 **Logado como:** {st.session_state.usuario}")
  if st.sidebar.button("Sair / Trocar Usuário"):
    st.session_state.logado = False
    st.session_state.usuario = ""
    st.rerun()

  aba1, aba2, aba3, aba4 = st.tabs([
      "📦 1. Estoque / EPIs",
      "👥 2. Colaboradores",
      "🛡️ 3. Entrega",
      "📜 4. Histórico",
  ])

  # ABA 1: ESTOQUE
  with aba1:
    st.subheader("Gerenciamento de Códigos, Tamanhos e Estoque")
    with st.form("form_cad_prod"):
      c1, c2, c3, c4, c5 = st.columns(5)
      with c1:
        cd = st.text_input("Código")
      with c2:
        ds = st.text_input("Descrição")
      with c3:
        tm = st.text_input("Tam")
      with c4:
        ca = st.text_input("CA")
      with c5:
        qt = st.text_input("Qtd Estoque", "0")

      if st.form_submit_button("Cadastrar Produto"):
        if cd and ds:
          produtos = carregar_json(ARQUIVO_PRODUTOS, [])
          produtos.append({
              "codigo": cd,
              "descricao": ds,
              "tamanho": tm,
              "ca": ca,
              "estoque": int(qt) if qt.isdigit() else 0,
          })
          salvar_json(ARQUIVO_PRODUTOS, produtos)
          st.success("Produto cadastrado com sucesso!")
          st.rerun()
        else:
          st.error("Preencha o código e a descrição!")

    st.markdown("---")
    st.subheader("Lista de Produtos Cadastrados")
    produtos = carregar_json(ARQUIVO_PRODUTOS, [])
    if produtos:
      st.dataframe(produtos, use_container_width=True)
    else:
      st.info("Nenhum produto cadastrado ainda.")

  # ABA 2: COLABORADORES
  with aba2:
    colaboradores = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
    st.subheader(f"Gerenciamento de Colaboradores (Total: {len(colaboradores)})")

    with st.form("form_cad_colab"):
      cc1, cc2, cc3 = st.columns(3)
      with cc1:
        mat = st.text_input("Matrícula")
      with cc2:
        nom = st.text_input("Nome Completo")
      with cc3:
        fun = st.text_input("Função")

      if st.form_submit_button("Cadastrar Colaborador"):
        if mat and nom:
          if any(str(c["matricula"]) == mat for c in colaboradores):
            st.error("Esta matrícula já existe!")
          else:
            colaboradores.append({
                "matricula": mat,
                "nome": nom.upper(),
                "funcao": fun.upper(),
            })
            salvar_json(ARQUIVO_COLABORADORES, colaboradores)
            st.success("Colaborador cadastrado com sucesso!")
            st.rerun()
        else:
          st.error("Preencha matrícula e nome!")

    st.markdown("---")
    if colaboradores:
      st.dataframe(colaboradores, use_container_width=True)

  # ABA 3: ENTREGA
  with aba3:
    st.subheader("Registro de Entrega de EPI")
    colab_lista = carregar_json(ARQUIVO_COLABORADORES, COLABORADORES_INICIAIS)
    prod_lista = carregar_json(ARQUIVO_PRODUTOS, [])

    matricula_busca = st.selectbox(
        "Selecione o Colaborador (por Matrícula e Nome):",
        options=colab_lista,
        format_func=lambda x: f"{x['matricula']} - {x['nome']} ({x['funcao']})",
    )

    produto_escolhido = st.selectbox(
        "Selecione o EPI:",
        options=prod_lista,
        format_func=lambda x: (
            f"Cód: {x['codigo']} - {x['descricao']} (Estoque:"
            f" {x.get('estoque', 0)})"
        ),
    )

    qtd_entrega = st.number_input(
        "Quantidade Entregue:", min_value=1, value=1, step=1
    )

    if st.button("✅ Confirmar Entrega de EPI"):
      if matricula_busca and produto_escolhido:
        entregas = carregar_json(ARQUIVO_ENTREGAS, [])
        nova_entrega = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "matricula": matricula_busca["matricula"],
            "colaborador": matricula_busca["nome"],
            "funcao": matricula_busca["funcao"],
            "codigo_epi": produto_escolhido["codigo"],
            "descricao_epi": produto_escolhido["descricao"],
            "quantidade": qtd_entrega,
            "responsavel": st.session_state.usuario,
        }
        entregas.append(nova_entrega)
        salvar_json(ARQUIVO_ENTREGAS, entregas)

        # Atualiza estoque
        for p in prod_lista:
          if p["codigo"] == produto_escolhido["codigo"]:
            p["estoque"] = max(0, p.get("estoque", 0) - qtd_entrega)
        salvar_json(ARQUIVO_PRODUTOS, prod_lista)

        st.success("Entrega registrada com sucesso e estoque atualizado!")
      else:
        st.error("Selecione o colaborador e o produto.")

  # ABA 4: HISTÓRICO
  with aba4:
    st.subheader("📜 Histórico de Entregas Realizadas")
    entregas = carregar_json(ARQUIVO_ENTREGAS, [])
    if entregas:
      st.dataframe(entregas, use_container_width=True)
    else:
      st.info("Nenhuma entrega registrada até o momento.")
