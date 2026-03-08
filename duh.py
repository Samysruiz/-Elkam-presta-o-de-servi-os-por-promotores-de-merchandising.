import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="EL KAM", layout="wide")

# ---------------- PASTA DE FOTOS ----------------

if not os.path.exists("fotos"):
    os.makedirs("fotos")

# ---------------- CRIAR ARQUIVOS ----------------

def garantir(nome,colunas):

    if not os.path.exists(nome):

        df = pd.DataFrame(columns=colunas)

        df.to_excel(nome,index=False)

garantir("usuarios.xlsx",["usuario","senha","tipo"])
garantir("mercados.xlsx",["mercado","endereco","produto"])
garantir("agenda.xlsx",["funcionario","mercado","produto"])
garantir("relatorio.xlsx",["data","funcionario","mercado","produto","status","foto"])

usuarios = pd.read_excel("usuarios.xlsx")
mercados = pd.read_excel("mercados.xlsx")
agenda = pd.read_excel("agenda.xlsx")
relatorio = pd.read_excel("relatorio.xlsx")

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

# ---------------- LOGOUT ----------------

if st.sidebar.button("Sair"):

    st.session_state.logado=False
    st.rerun()

# ================= ADMIN =================

if tipo == "admin":

    menu = st.sidebar.selectbox(
    "Menu",
    [
    "📊 Dashboard",
    "👥 Funcionários",
    "🏪 Mercados",
    "🗓 Criar Agenda",
    "📑 Relatórios"
    ]
    )

# -------- DASHBOARD --------

    if menu == "📊 Dashboard":

        st.header("Dashboard")

        total = len(relatorio)

        st.metric("Relatórios enviados",total)

        if total > 0:

            graf = relatorio.groupby("status").size()

            st.bar_chart(graf)

# -------- FUNCIONARIOS --------

    elif menu == "👥 Funcionários":

        st.header("Cadastrar funcionário")

        usuario_novo = st.text_input("Usuário")
        senha_nova = st.text_input("Senha",type="password")

        if st.button("Cadastrar funcionário"):

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

# -------- MERCADOS --------

    elif menu == "🏪 Mercados":

        st.header("Cadastrar mercado")

        mercado = st.text_input("Nome do mercado")
        endereco = st.text_input("Endereço")
        produto = st.text_input("Produto")

        if st.button("Cadastrar mercado"):

            novo = pd.concat([

            mercados,

            pd.DataFrame({

            "mercado":[mercado],
            "endereco":[endereco],
            "produto":[produto]

            })

            ],ignore_index=True)

            novo.to_excel("mercados.xlsx",index=False)

            st.success("Mercado cadastrado")

        st.dataframe(mercados)

# -------- AGENDA --------

    elif menu == "🗓 Criar Agenda":

        st.header("Criar agenda")

        funcionario = st.selectbox(
        "Funcionário",
        usuarios[usuarios.tipo=="funcionario"]["usuario"]
        )

        mercado = st.selectbox(
        "Mercado",
        mercados["mercado"]
        )

        produto = st.selectbox(
        "Produto",
        mercados["produto"]
        )

        if st.button("Adicionar tarefa"):

            agenda2 = pd.concat([

            agenda,

            pd.DataFrame({

            "funcionario":[funcionario],
            "mercado":[mercado],
            "produto":[produto]

            })

            ],ignore_index=True)

            agenda2.to_excel("agenda.xlsx",index=False)

            st.success("Agenda criada")

        st.dataframe(agenda)

# -------- RELATORIOS --------

    elif menu == "📑 Relatórios":

        st.header("Relatórios enviados")

        st.dataframe(relatorio)

# ================= FUNCIONARIO =================

else:

    st.header("Minha agenda")

    tarefas = agenda[
    agenda.funcionario==usuario
    ]

    registros=[]

    for i,row in tarefas.iterrows():

        mercado_info = mercados[
        mercados.mercado==row.mercado
        ]

        endereco=""

        if len(mercado_info)>0:

            endereco = mercado_info.iloc[0]["endereco"]

        st.subheader(row.mercado)

        st.write("📍 Endereço:",endereco)

        # BOTÃO GOOGLE MAPS
        if endereco != "":
            mapa_url = "https://www.google.com/maps/search/" + endereco.replace(" ","+")

            st.markdown(f"[🗺 Abrir rota no Google Maps]({mapa_url})")

        st.write("📦 Produto:",row.produto)

        status = st.radio(
        "Status",
        ["Abastecido","Falta"],
        key=i
        )

        foto = st.file_uploader(
        "Foto da gôndola",
        key=f"foto{i}"
        )

        caminho_foto=""

        if foto is not None:

            caminho_foto = f"fotos/{usuario}_{i}.jpg"

            with open(caminho_foto,"wb") as f:
                f.write(foto.getbuffer())

        registros.append({

        "data":date.today(),
        "funcionario":usuario,
        "mercado":row.mercado,
        "produto":row.produto,
        "status":status,
        "foto":caminho_foto

        })

    if st.button("Enviar relatório"):

        relatorio2 = pd.concat([

        relatorio,
        pd.DataFrame(registros)

        ],ignore_index=True)

        relatorio2.to_excel("relatorio.xlsx",index=False)

        st.success("Relatório enviado")
