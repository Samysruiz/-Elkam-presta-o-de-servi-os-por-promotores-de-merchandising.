import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="EL KAM",layout="wide")

# ---------------- PASTAS ----------------

for pasta in ["fotos"]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# ---------------- FUNÇÃO CRIAR ARQUIVO ----------------

def garantir(nome,colunas):

    if not os.path.exists(nome):

        df = pd.DataFrame(columns=colunas)

        df.to_excel(nome,index=False)

# ---------------- GARANTIR ARQUIVOS ----------------

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
    "🗓 Agenda Automática",
    "📑 Relatórios",
    "📸 Fotos"
    ]
    )

# -------- DASHBOARD --------

    if menu == "📊 Dashboard":

        st.header("Dashboard")

        st.metric("Relatórios enviados",len(relatorio))

        if len(relatorio)>0:

            graf = relatorio.groupby("status").size()

            st.bar_chart(graf)

# -------- FUNCIONARIOS --------

    elif menu == "👥 Funcionários":

        st.header("Funcionários")

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

        func_del = st.selectbox(
        "Excluir funcionário",
        usuarios[usuarios.tipo=="funcionario"]["usuario"]
        )

        if st.button("Excluir funcionário"):

            usuarios = usuarios[
            usuarios.usuario != func_del
            ]

            usuarios.to_excel("usuarios.xlsx",index=False)

            st.success("Funcionário removido")

# -------- MERCADOS --------

    elif menu == "🏪 Mercados":

    st.header("Gerenciar mercados")

    # ---------- CADASTRAR ----------

    st.subheader("Cadastrar novo mercado")

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

    st.divider()

    # ---------- EDITAR ----------

    st.subheader("Editar mercado")

    mercado_sel = st.selectbox(
    "Selecionar mercado",
    mercados["mercado"].unique()
    )

    dados = mercados[
    mercados.mercado == mercado_sel
    ]

    endereco_edit = st.text_input(
    "Endereço",
    dados.iloc[0]["endereco"]
    )

    if st.button("Salvar endereço"):

        mercados.loc[
        mercados.mercado == mercado_sel,
        "endereco"
        ] = endereco_edit

        mercados.to_excel("mercados.xlsx",index=False)

        st.success("Endereço atualizado")

    st.divider()

    # ---------- PRODUTOS ----------

    st.subheader("Produtos do mercado")

    produtos = dados["produto"].tolist()

    st.write(produtos)

    novo_produto = st.text_input("Adicionar produto")

    if st.button("Adicionar produto"):

        novo = pd.concat([
        mercados,
        pd.DataFrame({
        "mercado":[mercado_sel],
        "endereco":[endereco_edit],
        "produto":[novo_produto]
        })
        ],ignore_index=True)

        novo.to_excel("mercados.xlsx",index=False)

        st.success("Produto adicionado")

    prod_del = st.selectbox(
    "Excluir produto",
    produtos
    )

    if st.button("Excluir produto"):

        mercados = mercados[
        ~((mercados.mercado == mercado_sel) &
        (mercados.produto == prod_del))
        ]

        mercados.to_excel("mercados.xlsx",index=False)

        st.success("Produto removido")

    st.divider()

    st.dataframe(mercados)

    # ---------- CADASTRAR ----------

    st.subheader("Cadastrar novo mercado")

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

    st.divider()

    # ---------- EDITAR ----------

    st.subheader("Editar mercado")

    mercado_sel = st.selectbox(
    "Selecionar mercado",
    mercados["mercado"].unique()
    )

    dados = mercados[
    mercados.mercado == mercado_sel
    ]

    endereco_edit = st.text_input(
    "Endereço",
    dados.iloc[0]["endereco"]
    )

    if st.button("Salvar endereço"):

        mercados.loc[
        mercados.mercado == mercado_sel,
        "endereco"
        ] = endereco_edit

        mercados.to_excel("mercados.xlsx",index=False)

        st.success("Endereço atualizado")

    st.divider()

    # ---------- PRODUTOS ----------

    st.subheader("Produtos do mercado")

    produtos = dados["produto"].tolist()

    st.write(produtos)

    novo_produto = st.text_input("Adicionar produto")

    if st.button("Adicionar produto"):

        novo = pd.concat([
        mercados,
        pd.DataFrame({
        "mercado":[mercado_sel],
        "endereco":[endereco_edit],
        "produto":[novo_produto]
        })
        ],ignore_index=True)

        novo.to_excel("mercados.xlsx",index=False)

        st.success("Produto adicionado")

    prod_del = st.selectbox(
    "Excluir produto",
    produtos
    )

    if st.button("Excluir produto"):

        mercados = mercados[
        ~((mercados.mercado == mercado_sel) &
        (mercados.produto == prod_del))
        ]

        mercados.to_excel("mercados.xlsx",index=False)

        st.success("Produto removido")

    st.divider()

    st.dataframe(mercados)

# -------- AGENDA AUTOMATICA --------

    elif menu == "🗓 Agenda Automática":

        st.header("Criar agenda")

        funcionario = st.selectbox(
        "Funcionário",
        usuarios[usuarios.tipo=="funcionario"]["usuario"]
        )

        mercados_sel = st.multiselect(
        "Mercados",
        mercados["mercado"].unique()
        )

        tarefas=[]

        for m in mercados_sel:

            produtos = mercados[
            mercados.mercado==m
            ]["produto"]

            for p in produtos:

                tarefas.append({
                "funcionario":funcionario,
                "mercado":m,
                "produto":p
                })

        if len(tarefas)>0:

            df = pd.DataFrame(tarefas)

            st.dataframe(df)

            if st.button("Salvar agenda"):

                agenda2 = pd.concat([
                agenda,
                df
                ],ignore_index=True)

                agenda2.to_excel("agenda.xlsx",index=False)

                st.success("Agenda criada")

# -------- RELATORIOS --------

    elif menu == "📑 Relatórios":

        st.header("Relatórios")

        st.dataframe(relatorio)

# -------- FOTOS --------

    elif menu == "📸 Fotos":

        st.header("Fotos enviadas")

        arquivos = os.listdir("fotos")

        for f in arquivos:

            st.image(f"fotos/{f}",width=300)

# ================= FUNCIONARIO =================

else:

    st.header("Minha agenda")

    tarefas = agenda[
    agenda.funcionario==usuario
    ]

    registros=[]

    for i,row in tarefas.iterrows():

        info = mercados[
        mercados.mercado==row.mercado
        ]

        endereco=""

        if len(info)>0:
            endereco = info.iloc[0]["endereco"]

        st.subheader(row.mercado)

        st.write("📍",endereco)

        if endereco!="":

            mapa = "https://www.google.com/maps/search/" + endereco.replace(" ","+")

            st.markdown(f"[🗺 Abrir rota no Google Maps]({mapa})")

        st.write("Produto:",row.produto)

        status = st.radio(
        "Status",
        ["Abastecido","Falta"],
        key=i
        )

        foto = st.file_uploader(
        "Foto da gôndola",
        key=f"foto{i}"
        )

        caminho=""

        if foto:

            caminho=f"fotos/{usuario}_{i}.jpg"

            with open(caminho,"wb") as f:
                f.write(foto.getbuffer())

        registros.append({
        "data":date.today(),
        "funcionario":usuario,
        "mercado":row.mercado,
        "produto":row.produto,
        "status":status,
        "foto":caminho
        })

    if st.button("Enviar relatório"):

        relatorio2 = pd.concat([
        relatorio,
        pd.DataFrame(registros)
        ],ignore_index=True)

        relatorio2.to_excel("relatorio.xlsx",index=False)

        st.success("Relatório enviado")
