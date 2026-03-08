import streamlit as st
import pandas as pd
from datetime import date
import os
from streamlit_js_eval import get_geolocation

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="EL KAM",
    layout="wide"
)

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

# ---------------- LOGO ----------------

logo_path = "el_kam_logo.png"

col1,col2,col3 = st.columns([1,2,1])

with col2:
    if os.path.exists(logo_path):
        st.image(logo_path,use_container_width=True)

st.title("Sistema EL KAM")

# ---------------- FUNÇÃO CARREGAR ----------------

def carregar(nome):

    if os.path.exists(nome):
        return pd.read_excel(nome)
    else:
        return pd.DataFrame()

usuarios = carregar("usuarios.xlsx")
funcionarios = carregar("funcionarios.xlsx")
mercados = carregar("mercados.xlsx")
agenda = carregar("agenda.xlsx")
relatorio = carregar("relatorio.xlsx")
faltas = carregar("faltas.xlsx")

# ---------------- LOGIN ----------------

with st.sidebar.form("login"):

    st.subheader("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha",type="password")

    entrar = st.form_submit_button("Entrar")

if not entrar:
    st.stop()

login = usuarios[(usuarios.usuario==usuario) & (usuarios.senha==senha)]

if len(login)==0:
    st.error("Usuário ou senha incorretos")
    st.stop()

tipo = login.iloc[0]["tipo"]

# ================= ADMIN =================

if tipo == "admin":

    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Dashboard",
            "Mercados",
            "Mapa",
            "Relatórios",
            "Falta de Produtos"
        ]
    )

# ---------------- DASHBOARD ----------------

    if menu == "Dashboard":

        st.header("Dashboard")

        total = len(relatorio)
        feitos = len(relatorio[relatorio["status"]=="feito"])

        c1,c2 = st.columns(2)

        c1.metric("Tarefas",total)
        c2.metric("Concluídas",feitos)

        if len(relatorio)>0:

            ranking = relatorio.groupby("funcionario").size()

            st.bar_chart(ranking)

# ---------------- MERCADOS ----------------

    elif menu == "Mercados":

        st.header("Cadastro de mercados")

        with st.form("merc"):

            mercado = st.text_input("Mercado")
            item = st.text_input("Produto")

            lat = st.number_input("Latitude")
            lon = st.number_input("Longitude")

            cadastrar = st.form_submit_button("Cadastrar")

            if cadastrar:

                novos = pd.concat([
                    mercados,
                    pd.DataFrame({
                        "mercado":[mercado],
                        "item":[item],
                        "lat":[lat],
                        "lon":[lon]
                    })
                ],ignore_index=True)

                novos.to_excel("mercados.xlsx",index=False)

                st.success("Mercado cadastrado")

        st.dataframe(mercados)

# ---------------- MAPA ----------------

    elif menu == "Mapa":

        st.header("Mapa dos mercados")

        if "lat" in mercados.columns:

            st.map(mercados[["lat","lon"]])

        else:

            st.warning("Cadastre latitude e longitude")

# ---------------- RELATORIOS ----------------

    elif menu == "Relatórios":

        st.header("Relatórios de tarefas")

        st.dataframe(relatorio)

# ---------------- FALTA PRODUTOS ----------------

    elif menu == "Falta de Produtos":

        st.header("Produtos não abastecidos")

        if len(faltas)>0:

            st.dataframe(faltas)

            st.subheader("Produtos com mais falta")

            ranking = faltas.groupby("produto").size()

            st.bar_chart(ranking)

        else:

            st.info("Nenhuma falta registrada")

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

    else:

        st.info("Permita acesso à localização")

# -------- TAREFAS --------

    registros_falta = []

    if len(tarefas)==0:

        st.info("Nenhuma tarefa")

    else:

        for i,row in tarefas.iterrows():

            st.markdown(f"### {row.mercado} - {row.item}")

            abastecido = st.checkbox("Produto abastecido",key=f"a{i}")
            nao = st.checkbox("Não foi possível abastecer",key=f"n{i}")

            motivo=""

            if nao:

                motivo = st.selectbox(
                    "Motivo",
                    [
                        "Produto em falta no estoque",
                        "Produto não entregue",
                        "Mercado não autorizou",
                        "Sem espaço na gôndola",
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

        if st.button("Salvar registro"):

            relatorio.to_excel("relatorio.xlsx",index=False)

            if registros_falta:

                faltas2 = pd.concat([
                    faltas,
                    pd.DataFrame(registros_falta)
                ],ignore_index=True)

                faltas2.to_excel("faltas.xlsx",index=False)

            st.success("Registro salvo")
