import streamlit as st
import pandas as pd
import os
from datetime import date

# ---------------- CONFIG ----------------

st.set_page_config(page_title="EL KAM", layout="wide")

# ---------------- CSS PROFISSIONAL ----------------

st.markdown("""
<style>

/* fundo geral */

.stApp{
background-color:black;
}

/* sidebar */

section[data-testid="stSidebar"]{
background-color:#111;
}

/* texto menu */

section[data-testid="stSidebar"] *{
color:white;
font-weight:600;
}

/* selectbox menu */

div[data-baseweb="select"]{
background-color:#ff2b2b;
border-radius:8px;
}

/* hover */

div[data-baseweb="select"]:hover{
background-color:#cc0000;
}

/* títulos */

h1,h2,h3{
color:#ff2b2b;
}

/* inputs */

input{
background-color:white !important;
color:black !important;
}

/* botões */

.stButton button{
background-color:#ff2b2b;
color:white;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGO ----------------

if os.path.exists("el_kam_logo.png"):
    st.image("el_kam_logo.png",use_container_width=True)

st.title("Sistema EL KAM")

# ---------------- CRIAR ARQUIVOS ----------------

def garantir(nome,colunas):

    if not os.path.exists(nome):

        df = pd.DataFrame(columns=colunas)

        df.to_excel(nome,index=False)

garantir("usuarios.xlsx",["usuario","senha","tipo"])
garantir("funcionarios.xlsx",["funcionario"])
garantir("mercados.xlsx",["mercado","item","lat","lon"])
garantir("agenda.xlsx",["funcionario","dia","mercado","item"])
garantir("relatorio.xlsx",["data","funcionario","mercado","item","status"])
garantir("faltas.xlsx",["data","funcionario","mercado","produto","motivo"])

usuarios = pd.read_excel("usuarios.xlsx")
funcionarios = pd.read_excel("funcionarios.xlsx")
mercados = pd.read_excel("mercados.xlsx")
agenda = pd.read_excel("agenda.xlsx")
relatorio = pd.read_excel("relatorio.xlsx")
faltas = pd.read_excel("faltas.xlsx")

# ---------------- ADMIN PADRÃO ----------------

if usuarios.empty:

    usuarios = pd.DataFrame({

    "usuario":["admin"],
    "senha":["123"],
    "tipo":["admin"]

    })

    usuarios.to_excel("usuarios.xlsx",index=False)

# ---------------- LOGIN ----------------

if "logado" not in st.session_state:
    st.session_state.logado=False

if not st.session_state.logado:

    with st.sidebar.form("login"):

        usuario = st.text_input("Usuário")

        senha = st.text_input("Senha",type="password")

        entrar = st.form_submit_button("Entrar")

        if entrar:

            login = usuarios[
            (usuarios.usuario==usuario) &
            (usuarios.senha==senha)
            ]

            if len(login)>0:

                st.session_state.logado=True
                st.session_state.usuario=usuario
                st.session_state.tipo=login.iloc[0]["tipo"]

                st.rerun()

            else:

                st.error("Usuário ou senha incorretos")

    st.stop()

usuario = st.session_state.usuario
tipo = st.session_state.tipo
st.sidebar.write("Logado como:", tipo)

# ---------------- LOGOUT ----------------

if st.sidebar.button("Sair"):

    st.session_state.logado=False
    st.rerun()

# ================= MENU ADMIN =================

if tipo=="admin":

    menu_opcoes = {
"📊 Dashboard":"dashboard",
"👥 Funcionários":"funcionarios",
"🏪 Mercados":"mercados",
"🗺️ Mapa":"mapa",
"📑 Relatórios":"relatorios",
"📦 Falta de Produtos":"faltas",
"🔑 Alterar Senha":"senha"
}

menu = st.sidebar.selectbox(
"Menu",
list(menu_opcoes.keys())
)

menu = menu_opcoes[menu]

# ---------------- DASHBOARD ----------------

if menu == "dashboard":

    st.header("Dashboard")

    st.metric("Tarefas registradas",len(relatorio))


# ---------------- FUNCIONARIOS ----------------

elif menu == "funcionarios":

    st.header("Cadastrar funcionário")

    nome = st.text_input("Nome")
    usuario_novo = st.text_input("Usuário")
    senha_nova = st.text_input("Senha",type="password")

    if st.button("Cadastrar"):

        if usuario_novo in usuarios["usuario"].values:

            st.error("Usuário já existe")

        else:

            usuarios2 = pd.concat([

            usuarios,

            pd.DataFrame({

            "usuario":[usuario_novo],
            "senha":[senha_nova],
            "tipo":["funcionario"]

            })

            ],ignore_index=True)

            usuarios2.to_excel("usuarios.xlsx",index=False)

            st.success("Funcionário criado")


# ---------------- MERCADOS ----------------

elif menu == "mercados":

    st.header("Cadastrar mercado")

    mercado = st.text_input("Mercado")
    item = st.text_input("Produto")

    lat = st.number_input("Latitude")
    lon = st.number_input("Longitude")

    if st.button("Cadastrar mercado"):

        novo = pd.concat([

        mercados,

        pd.DataFrame({

        "mercado":[mercado],
        "item":[item],
        "lat":[lat],
        "lon":[lon]

        })

        ],ignore_index=True)

        novo.to_excel("mercados.xlsx",index=False)

        st.success("Mercado cadastrado")

    st.dataframe(mercados)


# ---------------- MAPA ----------------

elif menu == "mapa":

    st.header("Mapa")

    if len(mercados)>0:

        st.map(mercados[["lat","lon"]])


# ---------------- RELATORIOS ----------------

elif menu == "relatorios":

    st.header("Relatórios")

    st.dataframe(relatorio)


# ---------------- FALTAS ----------------

elif menu == "faltas":

    st.header("Produtos não abastecidos")

    st.dataframe(faltas)


# ---------------- ALTERAR SENHA ----------------

elif menu == "senha":

    st.header("Alterar senha")

    usuario_sel = st.selectbox("Usuário",usuarios["usuario"])

    nova = st.text_input("Nova senha",type="password")

    if st.button("Salvar nova senha"):

        usuarios.loc[
        usuarios.usuario==usuario_sel,
        "senha"
        ] = nova

        usuarios.to_excel("usuarios.xlsx",index=False)

        st.success("Senha atualizada")
