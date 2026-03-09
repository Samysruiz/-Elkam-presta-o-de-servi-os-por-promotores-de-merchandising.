import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

# ---------------- CONFIG ----------------

st.set_page_config(
page_title="DUH Sistema",
layout="wide",
initial_sidebar_state="expanded"
)

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

input{
    background-color:white !important;
    color:black !important;
}

.stButton button{
    background-color:#ff2b2b;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGO ----------------

if os.path.exists("el_kam_logo.png"):
    st.image("el_kam_logo.png",use_container_width=True)



# ---------------- PASTA FOTO ----------------

if not os.path.exists("fotos"):
    os.makedirs("fotos")

# ---------------- BANCO ----------------

conn = sqlite3.connect("duh.db", check_same_thread=False)
c = conn.cursor()

# ---------------- TABELAS ----------------

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
usuario TEXT,
senha TEXT,
tipo TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS mercados(
mercado TEXT,
endereco TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS produtos(
mercado TEXT,
produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS agenda(
funcionario TEXT,
dia TEXT,
mercado TEXT,
produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS relatorio(
data TEXT,
funcionario TEXT,
mercado TEXT,
produto TEXT,
status TEXT,
foto TEXT
)
""")

conn.commit()

# ---------------- ADMIN PADRÃO ----------------

admin = pd.read_sql("SELECT * FROM usuarios", conn)

if admin.empty:

    c.execute("INSERT INTO usuarios VALUES('admin','123','admin')")
    conn.commit()

# ---------------- LOGIN ----------------

if "logado" not in st.session_state:
    st.session_state.logado=False

if not st.session_state.logado:

    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        login = pd.read_sql(
        f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND senha='{senha}'",
        conn)

        if len(login)>0:

            st.session_state.logado=True
            st.session_state.usuario=usuario
            st.session_state.tipo=login.iloc[0]["tipo"]

            st.rerun()

        else:

            st.error("Usuário ou senha inválidos")

    st.stop()

usuario = st.session_state.usuario
tipo = st.session_state.tipo

# ---------------- LOGOUT ----------------

if st.sidebar.button("Sair"):

    st.session_state.logado=False
    st.rerun()

# =====================================================
# ================= DASHBOARD ==========================
# =====================================================

if tipo=="admin":

    menu = st.sidebar.selectbox(
    "Menu",
    [
    "Dashboard",
    "Funcionários",
    "Mercados",
    "Agenda",
    "Relatórios",
    "Fotos"
    ])

# ---------------- DASHBOARD ----------------

    if menu=="Dashboard":

        st.header("Dashboard")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        st.metric("Relatórios enviados", len(rel))

        if len(rel)>0:

            graf = rel.groupby("status").size()

            st.bar_chart(graf)

        st.subheader("Ranking Promotores")

        rank = rel.groupby("funcionario").size().sort_values(ascending=False)

        st.dataframe(rank)

        st.subheader("Produtos com mais falta")

        faltas = rel[rel["status"]=="Falta"]

        if len(faltas)>0:

            graf2 = faltas.groupby("produto").size()

            st.bar_chart(graf2)

# ---------------- FUNCIONARIOS ----------------

    elif menu=="Funcionários":

        st.header("Funcionários")

        user = st.text_input("Usuário")
        senha = st.text_input("Senha")

        if st.button("Cadastrar"):

            c.execute(
            "INSERT INTO usuarios VALUES(?,?,?)",
            (user,senha,"funcionario"))

            conn.commit()

            st.success("Funcionário criado")

# ---------------- MERCADOS ----------------

    elif menu=="Mercados":

        st.header("Mercados")

        mercado = st.text_input("Mercado")
        endereco = st.text_input("Endereço")

        if st.button("Cadastrar mercado"):

            c.execute(
            "INSERT INTO mercados VALUES(?,?)",
            (mercado,endereco))

            conn.commit()

            st.success("Mercado criado")

        mercados = pd.read_sql("SELECT * FROM mercados", conn)

        mercado_sel = st.selectbox(
        "Selecionar mercado",
        mercados["mercado"])

        st.subheader("Produtos")

        produto = st.text_input("Produto")

        if st.button("Adicionar produto"):

            c.execute(
            "INSERT INTO produtos VALUES(?,?)",
            (mercado_sel,produto))

            conn.commit()

            st.success("Produto adicionado")

# ---------------- AGENDA ----------------

    elif menu=="Agenda":

        st.header("Montar agenda")

        funcionarios = pd.read_sql(
        "SELECT usuario FROM usuarios WHERE tipo='funcionario'",
        conn)

        mercados = pd.read_sql(
        "SELECT mercado FROM mercados",
        conn)

        func = st.selectbox("Funcionário", funcionarios["usuario"])

        dia = st.selectbox(
        "Dia",
        ["segunda","terça","quarta","quinta","sexta"]
        )

        mercado = st.selectbox("Mercado", mercados["mercado"])

        produtos = pd.read_sql(
        f"SELECT produto FROM produtos WHERE mercado='{mercado}'",
        conn)

        st.subheader("Produtos")

        selecionar_todos = st.checkbox("Todos os produtos")

        selecionados=[]

        for p in produtos["produto"]:

            if selecionar_todos:

                selecionados.append(p)

            else:

                if st.checkbox(p):

                    selecionados.append(p)

        if st.button("Salvar agenda"):

            for prod in selecionados:

                c.execute(
                "INSERT INTO agenda VALUES(?,?,?,?)",
                (func,dia,mercado,prod))

            conn.commit()

            st.success("Agenda criada")

# ---------------- RELATORIOS ----------------

    elif menu=="Relatórios":

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        st.dataframe(rel)

# ---------------- FOTOS ----------------

    elif menu=="Fotos":

        fotos = os.listdir("fotos")

        for f in fotos:

            st.image(f"fotos/{f}", width=300)

# =====================================================
# ================= FUNCIONARIO =======================
# =====================================================

else:

    st.header("Minha agenda da semana")

    tarefas = pd.read_sql(
    f"SELECT * FROM agenda WHERE funcionario='{usuario}'",
    conn)

    dias = tarefas.groupby("dia")

    for dia, dados in dias:

        st.header(dia.upper())

        mercados = dados.groupby("mercado")

        for mercado, produtos in mercados:

            st.subheader(mercado)

            info = pd.read_sql(
            f"SELECT endereco FROM mercados WHERE mercado='{mercado}'",
            conn)

            endereco = info.iloc[0]["endereco"]

            st.write("📍", endereco)

            mapa = "https://www.google.com/maps/search/" + endereco.replace(" ","+")

            st.markdown(f"[Abrir rota no Google Maps]({mapa})")

            for i,row in produtos.iterrows():

                st.checkbox(row["produto"], key=f"{i}")

            foto = st.file_uploader(
            "Foto da gôndola",
            key=f"foto{i}")

            caminho=""

            if foto:

                caminho=f"fotos/{usuario}_{i}.jpg"

                with open(caminho,"wb") as f:

                    f.write(foto.getbuffer())

            if st.button(f"Enviar relatório {mercado}"):

                df = pd.DataFrame([{
                "data":date.today(),
                "funcionario":usuario,
                "mercado":mercado,
                "produto":"varios",
                "status":"ok",
                "foto":caminho
                }])

                df.to_sql("relatorio", conn, if_exists="append", index=False)

                st.success("Relatório enviado")
