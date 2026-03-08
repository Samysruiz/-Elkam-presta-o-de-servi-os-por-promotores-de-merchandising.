import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="DUH Sistema", layout="wide")

# ---------- PASTA DE FOTOS ----------
if not os.path.exists("fotos"):
    os.makedirs("fotos")

# ---------- BANCO ----------
conn = sqlite3.connect("duh.db", check_same_thread=False)
c = conn.cursor()

# ---------- TABELAS ----------
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
usuario TEXT PRIMARY KEY,
senha TEXT,
tipo TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS mercados(
id INTEGER PRIMARY KEY AUTOINCREMENT,
mercado TEXT,
endereco TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
mercado TEXT,
produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS agenda(
id INTEGER PRIMARY KEY AUTOINCREMENT,
funcionario TEXT,
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

# ---------- ADMIN PADRÃO ----------
admin = pd.read_sql("SELECT * FROM usuarios", conn)

if admin.empty:
    c.execute("INSERT INTO usuarios VALUES('admin','123','admin')")
    conn.commit()

# ---------- LOGIN ----------
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        login = pd.read_sql(
        f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND senha='{senha}'",
        conn)

        if len(login) > 0:

            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.tipo = login.iloc[0]["tipo"]
            st.rerun()

        else:
            st.error("Usuário ou senha inválidos")

    st.stop()

usuario = st.session_state.usuario
tipo = st.session_state.tipo

# ---------- LOGOUT ----------
if st.sidebar.button("Sair"):
    st.session_state.logado = False
    st.rerun()

# ======================================================
# ===================== ADMIN ==========================
# ======================================================

if tipo == "admin":

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

# ---------- DASHBOARD ----------
    if menu == "Dashboard":

        st.header("Dashboard")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        st.metric("Relatórios enviados", len(rel))

        if len(rel) > 0:

            graf = rel.groupby("status").size()
            st.bar_chart(graf)

# ---------- FUNCIONÁRIOS ----------
    elif menu == "Funcionários":

        st.subheader("Cadastrar funcionário")

        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Cadastrar"):

            c.execute(
            "INSERT INTO usuarios VALUES(?,?,?)",
            (user,senha,"funcionario"))

            conn.commit()
            st.success("Funcionário criado")

        funcionarios = pd.read_sql(
        "SELECT usuario FROM usuarios WHERE tipo='funcionario'",
        conn)

        if len(funcionarios) > 0:

            func_del = st.selectbox("Excluir funcionário",
            funcionarios["usuario"])

            if st.button("Excluir funcionário"):

                c.execute(
                "DELETE FROM usuarios WHERE usuario=?",
                (func_del,))

                conn.commit()
                st.success("Removido")

# ---------- MERCADOS ----------
    elif menu == "Mercados":

        st.header("Mercados")

        mercado = st.text_input("Nome do mercado")
        endereco = st.text_input("Endereço")

        if st.button("Cadastrar mercado"):

            c.execute(
            "INSERT INTO mercados VALUES(NULL,?,?)",
            (mercado,endereco))

            conn.commit()
            st.success("Mercado criado")

        mercados = pd.read_sql("SELECT * FROM mercados", conn)

        if len(mercados) > 0:

            mercado_sel = st.selectbox(
            "Selecionar mercado",
            mercados["mercado"])

# ---------- EDITAR ENDEREÇO ----------
            novo_end = st.text_input("Editar endereço")

            if st.button("Salvar endereço"):

                c.execute(
                "UPDATE mercados SET endereco=? WHERE mercado=?",
                (novo_end,mercado_sel))

                conn.commit()

                st.success("Atualizado")

# ---------- EXCLUIR MERCADO ----------
            if st.button("Excluir mercado"):

                c.execute(
                "DELETE FROM mercados WHERE mercado=?",
                (mercado_sel,))

                conn.commit()

                st.success("Mercado excluído")

# ---------- PRODUTOS ----------
            st.subheader("Produtos")

            produto = st.text_input("Produto")

            if st.button("Adicionar produto"):

                c.execute(
                "INSERT INTO produtos VALUES(NULL,?,?)",
                (mercado_sel,produto))

                conn.commit()

                st.success("Produto adicionado")

            produtos = pd.read_sql(
            f"SELECT * FROM produtos WHERE mercado='{mercado_sel}'",
            conn)

            if len(produtos) > 0:

                prod_del = st.selectbox(
                "Excluir produto",
                produtos["produto"])

                if st.button("Excluir produto"):

                    c.execute(
                    "DELETE FROM produtos WHERE produto=?",
                    (prod_del,))

                    conn.commit()

                    st.success("Produto removido")

# ---------- AGENDA ----------
    elif menu == "Agenda":

    st.header("Montar agenda da semana")

    funcionarios = pd.read_sql(
    "SELECT usuario FROM usuarios WHERE tipo='funcionario'",
    conn)

    mercados = pd.read_sql(
    "SELECT mercado FROM mercados",
    conn)

    func = st.selectbox(
    "Funcionário",
    funcionarios["usuario"]
    )

    dia = st.selectbox(
    "Dia",
    ["segunda","terça","quarta","quinta","sexta"]
    )

    mercado = st.selectbox(
    "Mercado",
    mercados["mercado"]
    )

    produtos = pd.read_sql(
    f"SELECT produto FROM produtos WHERE mercado='{mercado}'",
    conn)

    st.subheader("Produtos")

    selecionar_todos = st.checkbox("Todos os produtos")

    selecionados = []

    for p in produtos["produto"]:

        if selecionar_todos:
            selecionados.append(p)

        else:
            if st.checkbox(p):
                selecionados.append(p)

    if st.button("Salvar agenda"):

        for prod in selecionados:

            c.execute(
            "INSERT INTO agenda VALUES(NULL,?,?,?,?)",
            (func,dia,mercado,prod)
            )

        conn.commit()

        st.success("Agenda criada")

# ---------- RELATÓRIOS ----------
    elif menu == "Relatórios":

        st.header("Relatórios")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        st.dataframe(rel)

        if st.button("Exportar Excel"):

            rel.to_excel("relatorios.xlsx", index=False)

            st.success("Exportado")

# ---------- FOTOS ----------
    elif menu == "Fotos":

        st.header("Fotos")

        fotos = os.listdir("fotos")

        for f in fotos:
            st.image(f"fotos/{f}", width=300)

# ======================================================
# ================= FUNCIONÁRIO ========================
# ======================================================

else:

    st.header("Minha agenda")

    tarefas = pd.read_sql(
    f"SELECT * FROM agenda WHERE funcionario='{usuario}'",
    conn)

    registros = []

    for i,row in tarefas.iterrows():

        st.subheader(row["mercado"])

        info = pd.read_sql(
        f"SELECT endereco FROM mercados WHERE mercado='{row['mercado']}'",
        conn)

        endereco = info.iloc[0]["endereco"]

        st.write("Endereço:", endereco)

        mapa = "https://www.google.com/maps/search/" + endereco.replace(" ","+")

        st.markdown(f"[Abrir rota no Google Maps]({mapa})")

        st.write("Produto:", row["produto"])

        status = st.radio(
        "Status",
        ["Abastecido","Falta"],
        key=i)

        foto = st.file_uploader(
        "Foto da gôndola",
        key=f"foto{i}")

        caminho = ""

        if foto:

            caminho = f"fotos/{usuario}_{i}.jpg"

            with open(caminho,"wb") as f:
                f.write(foto.getbuffer())

        registros.append({
        "data":date.today(),
        "funcionario":usuario,
        "mercado":row["mercado"],
        "produto":row["produto"],
        "status":status,
        "foto":caminho
        })

    if st.button("Enviar relatório"):

        df = pd.DataFrame(registros)

        df.to_sql("relatorio", conn, if_exists="append", index=False)

        st.success("Relatório enviado")
