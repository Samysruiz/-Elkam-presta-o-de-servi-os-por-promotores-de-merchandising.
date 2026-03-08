import streamlit as st
import pandas as pd
import os
from datetime import date
try:
    from streamlit_js_eval import get_geolocation
    GEO = True
except:
    GEO = False

# ---------------- CONFIG ----------------

st.set_page_config(page_title="EL KAM", layout="wide")

# ---------------- ESTILO ----------------

st.markdown("""
<style>

.stApp{
    background-color:black;
}

h1,h2,h3{
    color:#ff2b2b;
}

label{
    color:white !important;
}

.stButton button{
    background-color:#ff2b2b;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGO SE EXISTIR ----------------

import os

logo_path = "el_kam_logo.png"

if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)
else:
    st.warning("Logo não encontrada")

# ---------------- FUNÇÃO CRIAR PLANILHA ----------------

def garantir_arquivo(nome,colunas):

    if not os.path.exists(nome):

        df = pd.DataFrame(columns=colunas)

        df.to_excel(nome,index=False)

# ---------------- GARANTIR ARQUIVOS ----------------

garantir_arquivo(
"usuarios.xlsx",
["usuario","senha","tipo"]
)

garantir_arquivo(
"funcionarios.xlsx",
["funcionario"]
)

garantir_arquivo(
"mercados.xlsx",
["mercado","item","lat","lon"]
)

garantir_arquivo(
"agenda.xlsx",
["funcionario","dia","mercado","item"]
)

garantir_arquivo(
"relatorio.xlsx",
["data","funcionario","mercado","item","status"]
)

garantir_arquivo(
"faltas.xlsx",
["data","funcionario","mercado","produto","motivo"]
)

# ---------------- CARREGAR ----------------

usuarios = pd.read_excel("usuarios.xlsx")
funcionarios = pd.read_excel("funcionarios.xlsx")
mercados = pd.read_excel("mercados.xlsx")
agenda = pd.read_excel("agenda.xlsx")
relatorio = pd.read_excel("relatorio.xlsx")
faltas = pd.read_excel("faltas.xlsx")

# ---------------- LOGIN ----------------

with st.sidebar.form("login"):

    st.subheader("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha",type="password")

    entrar = st.form_submit_button("Entrar")

if not entrar:
    st.stop()

login = usuarios[
(usuarios.usuario==usuario) &
(usuarios.senha==senha)
]

if len(login)==0:

    st.error("Usuário ou senha incorretos")

    st.stop()

tipo = login.iloc[0]["tipo"]

# ================= ADMIN =================

if tipo=="admin":

    menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard","Mercados","Mapa","Relatórios","Falta de Produtos"]
    )

# ---------------- DASHBOARD ----------------

    if menu=="Dashboard":

        st.header("Dashboard")

        total = len(relatorio)

        feitos = len(
        relatorio[relatorio["status"]=="feito"]
        )

        c1,c2 = st.columns(2)

        c1.metric("Tarefas",total)

        c2.metric("Concluídas",feitos)

# ---------------- MERCADOS ----------------

    elif menu=="Mercados":

        st.header("Cadastrar mercado")

        with st.form("merc"):

            mercado = st.text_input("Mercado")
            item = st.text_input("Produto")

            lat = st.number_input("Latitude")

            lon = st.number_input("Longitude")

            cadastrar = st.form_submit_button("Cadastrar")

            if cadastrar:

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

    elif menu=="Mapa":

        st.header("Mapa dos mercados")

        if len(mercados)>0:

            st.map(mercados[["lat","lon"]])

        else:

            st.info("Nenhum mercado cadastrado")

# ---------------- RELATORIOS ----------------

    elif menu=="Relatórios":

        st.header("Relatórios")

        st.dataframe(relatorio)

# ---------------- FALTA PRODUTOS ----------------

    elif menu=="Falta de Produtos":

        st.header("Produtos não abastecidos")

        st.dataframe(faltas)

        if len(faltas)>0:

            ranking = faltas.groupby("produto").size()

            st.bar_chart(ranking)

# ================= FUNCIONARIO =================

else:

    st.header("Minhas tarefas")

    tarefas = agenda[agenda.funcionario==usuario]

# -------- LOCALIZAÇÃO --------

    st.subheader("Minha localização")

    loc = get_geolocation()

    if loc:

        lat = loc["coords"]["latitude"]

        lon = loc["coords"]["longitude"]

        pos = pd.DataFrame({
        "lat":[lat],
        "lon":[lon]
        })

        st.map(pos)

# -------- TAREFAS --------

    registros_falta=[]

    for i,row in tarefas.iterrows():

        st.markdown(
        f"### {row.mercado} - {row.item}"
        )

        abastecido = st.checkbox(
        "Produto abastecido",
        key=f"a{i}"
        )

        nao = st.checkbox(
        "Não foi possível abastecer",
        key=f"n{i}"
        )

        if nao:

            motivo = st.selectbox(
            "Motivo",
            [
            "Produto em falta",
            "Produto não entregue",
            "Mercado não autorizou",
            "Sem espaço",
            "Outro"
            ],
            key=f"m{i}"
            )

            registros_falta.append({

            "data":date.today(),

            "funcionario":usuario,

            "mercado":row.mercado,

            "produto":row.item,

            "motivo":motivo

            })

        if abastecido:

            relatorio = pd.concat([

            relatorio,

            pd.DataFrame({

            "data":[date.today()],

            "funcionario":[usuario],

            "mercado":[row.mercado],

            "item":[row.item],

            "status":["feito"]

            })

            ])

    if st.button("Salvar"):

        relatorio.to_excel("relatorio.xlsx",index=False)

        if registros_falta:

            faltas2 = pd.concat([

            faltas,

            pd.DataFrame(registros_falta)

            ],ignore_index=True)

            faltas2.to_excel("faltas.xlsx",index=False)

        st.success("Registro salvo")
