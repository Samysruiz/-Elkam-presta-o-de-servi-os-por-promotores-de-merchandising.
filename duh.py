import streamlit as st
import pandas as pd
import os
from datetime import date

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

st.title("Sistema EL KAM")

# ---------------- FUNÇÃO GARANTIR ARQUIVOS ----------------

def garantir(nome,colunas):

    if not os.path.exists(nome):

        df = pd.DataFrame(columns=colunas)

        df.to_excel(nome,index=False)

# ---------------- CRIAR PLANILHAS ----------------

garantir("usuarios.xlsx",["usuario","senha","tipo"])
garantir("funcionarios.xlsx",["funcionario"])
garantir("mercados.xlsx",["mercado","item","lat","lon"])
garantir("agenda.xlsx",["funcionario","dia","mercado","item"])
garantir("relatorio.xlsx",["data","funcionario","mercado","item","status"])
garantir("faltas.xlsx",["data","funcionario","mercado","produto","motivo"])

# ---------------- CARREGAR ----------------

usuarios = pd.read_excel("usuarios.xlsx")
funcionarios = pd.read_excel("funcionarios.xlsx")
mercados = pd.read_excel("mercados.xlsx")
agenda = pd.read_excel("agenda.xlsx")
relatorio = pd.read_excel("relatorio.xlsx")
faltas = pd.read_excel("faltas.xlsx")

# ---------------- CRIAR ADMIN AUTOMÁTICO ----------------

if usuarios.empty:

    usuarios = pd.DataFrame({

        "usuario":["admin"],
        "senha":["123"],
        "tipo":["admin"]

    })

    usuarios.to_excel("usuarios.xlsx",index=False)

# ---------------- LOGIN ----------------

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.tipo = None
    st.session_state.usuario = None

if not st.session_state.logado:

    with st.sidebar.form("login"):

        st.subheader("Login")

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        entrar = st.form_submit_button("Entrar")

        if entrar:

            login = usuarios[
                (usuarios.usuario == usuario) &
                (usuarios.senha == senha)
            ]

            if len(login) > 0:

                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.session_state.tipo = login.iloc[0]["tipo"]

                st.rerun()

            else:

                st.error("Usuário ou senha incorretos")

    st.stop()

tipo = st.session_state.tipo
usuario = st.session_state.usuario
#-------------------RECUPERAR SENHA-------------
if st.sidebar.button("Recuperar senha"):

    st.sidebar.write("Digite seu usuário")

    user_rec = st.sidebar.text_input("Usuário para recuperar")

    nova = st.sidebar.text_input("Nova senha", type="password")

    if st.sidebar.button("Resetar senha"):

        if user_rec in usuarios["usuario"].values:

            usuarios.loc[
                usuarios["usuario"]==user_rec,
                "senha"
            ] = nova

            usuarios.to_excel("usuarios.xlsx",index=False)

            st.sidebar.success("Senha atualizada")

        else:

            st.sidebar.error("Usuário não encontrado")
# ================= ADMIN =================

if tipo=="admin":

    menu = st.sidebar.selectbox(
    "Menu",
    ["funcionários","Dashboard","Mercados","Mapa","Relatórios","Falta de Produtos","Alterar Senha"]
    )
#-----------------FUNCIONÁRIOS--------------
elif menu == "Funcionários":

    st.header("Cadastrar funcionário")

    nome = st.text_input("Nome do funcionário")
    usuario_novo = st.text_input("Usuário")
    senha_nova = st.text_input("Senha", type="password")

    if st.button("Cadastrar funcionário"):

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

            funcionarios2 = pd.concat([
                funcionarios,
                pd.DataFrame({
                    "funcionario":[usuario_novo]
                })
            ],ignore_index=True)

            funcionarios2.to_excel("funcionarios.xlsx",index=False)

            st.success("Funcionário cadastrado")

# ---------------- DASHBOARD ----------------

    if menu=="Dashboard":

        st.header("Dashboard")

        total = len(relatorio)

        feitos = len(relatorio[relatorio["status"]=="feito"])

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

        st.header("Mapa")

        if len(mercados)>0:

            st.map(mercados[["lat","lon"]])

# ---------------- RELATORIOS ----------------

    elif menu=="Relatórios":

        st.dataframe(relatorio)

# ---------------- FALTAS ----------------

    elif menu=="Falta de Produtos":

        st.header("Produtos não abastecidos")

        st.dataframe(faltas)

# ================= FUNCIONARIO =================

else:

    st.header("Minhas tarefas")

    tarefas = agenda[agenda.funcionario==usuario]

    registros_falta=[]

    for i,row in tarefas.iterrows():

        st.markdown(f"### {row.mercado} - {row.item}")

        abastecido = st.checkbox("Produto abastecido",key=f"a{i}")

        nao = st.checkbox("Não foi possível abastecer",key=f"n{i}")

        if nao:

            motivo = st.selectbox(
            "Motivo",
            ["Produto em falta","Produto não entregue","Sem espaço","Outro"],
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
#------------------alterar senha------------------------
     elif menu == "Alterar Senha":

    st.header("Alterar senha")

    usuario_sel = st.selectbox(
        "Usuário",
        usuarios["usuario"]
    )

    nova_senha = st.text_input(
        "Nova senha",
        type="password"
    )

    confirmar = st.text_input(
        "Confirmar senha",
        type="password"
    )

    if st.button("Salvar nova senha"):

        if nova_senha != confirmar:

            st.error("As senhas não coincidem")

        else:

            usuarios.loc[
                usuarios["usuario"] == usuario_sel,
                "senha"
            ] = nova_senha

            usuarios.to_excel(
                "usuarios.xlsx",
                index=False
            )

            st.success("Senha atualizada")
