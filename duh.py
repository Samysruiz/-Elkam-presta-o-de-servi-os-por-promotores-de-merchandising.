
import streamlit as st
import pandas as pd
from datetime import date
import os
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import streamlit as st
import pandas as pd

# 1. Configuração ÚNICA e no topo
st.set_page_config(page_title="EL KAM", layout="centered")

# 2. CSS para Fundo Preto e Títulos Vermelhos
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .titulo-vermelho {
        color: #FF0000;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    h1, h2, h3, .stSubheader, label, p {
        color: #FF0000 !important;
    }
    .stButton>button {
        background-color: #FF0000;
        color: white;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Exibição do Logo e Título
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # Ajustado para o nome comum de arquivo
        st.image("el_kam_logo.png.png", width=200) 
    except:
        st.write("Logo não encontrado")

    st.markdown('<p class="titulo-vermelho">EL KAM - Prestação de Serviço e Merchandising</p>', unsafe_allow_html=True)

st.divider()

#----------------LOGIN---------
usuarios = pd.read_excel("usuarios.xlsx")
funcionarios = pd.read_excel("funcionarios.xlsx")
mercados = pd.read_excel("mercados.xlsx")
agenda = pd.read_excel("agenda.xlsx")
relatorio = pd.read_excel("relatorio.xlsx")
with st.sidebar.form("login_form"):

    st.subheader("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    entrar = st.form_submit_button("Entrar")
if not entrar:
    st.stop()

login = usuarios[(usuarios.usuario == usuario) & (usuarios.senha == senha)]

if len(login) == 0:
    st.error("Usuário ou senha incorretos")
    st.stop()

tipo = login.iloc[0]["tipo"]

# ---------------- ADMIN ----------------
if tipo == "admin":

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard","Funcionários","Mercados","Agenda","Mapa","Relatórios"]
    )

    if menu == "Dashboard":

        st.header("Dashboard")

        total = len(relatorio)
        feitos = len(relatorio[relatorio["status"]=="feito"])

        c1,c2 = st.columns(2)
        c1.metric("Tarefas registradas", total)
        c2.metric("Tarefas concluídas", feitos)

        if len(relatorio) > 0:
            prod = relatorio.groupby("funcionario").size()
            st.bar_chart(prod)

elif menu == "Funcionários":

    st.header("Funcionários")

    with st.form("novo"):
        nome = st.text_input("Nome do funcionário")
        user = st.text_input("Usuário de login")
        senha_nova = st.text_input("Senha", type="password")

        ok = st.form_submit_button("Cadastrar")

        if ok:

            # verificar duplicidade
            nome_existe = nome.lower() in funcionarios["funcionario"].str.lower().values
            user_existe = user.lower() in usuarios["usuario"].str.lower().values

            if nome_existe or user_existe:

                st.error("⚠ Funcionário ou usuário já cadastrado!")

            else:

                funcionarios = pd.concat([
                    funcionarios,
                    pd.DataFrame({"funcionario":[nome]})
                ], ignore_index=True)

                funcionarios.to_excel("funcionarios.xlsx", index=False)

                usuarios = pd.concat([
                    usuarios,
                    pd.DataFrame({
                        "usuario":[user],
                        "senha":[senha_nova],
                        "tipo":["funcionario"]
                    })
                ], ignore_index=True)

                usuarios.to_excel("usuarios.xlsx", index=False)

                st.success("✅ Funcionário cadastrado com sucesso")

        st.dataframe(funcionarios)

elif menu == "Mercados":

        st.header("Mercados")

        with st.form("merc"):
            mercado = st.text_input("Mercado")
            item = st.text_input("Item")
            lat = st.number_input("Latitude")
            lon = st.number_input("Longitude")
            ok = st.form_submit_button("Adicionar")

            if ok:
                mercados = pd.concat([mercados,pd.DataFrame({
                    "mercado":[mercado],
                    "item":[item],
                    "lat":[lat],
                    "lon":[lon]
                })])
                mercados.to_excel("mercados.xlsx", index=False)

                st.success("Cadastrado")

        st.dataframe(mercados)
    
elif menu == "Agenda":

        st.header("Criar agenda")

        func = st.selectbox("Funcionário", funcionarios.funcionario)

        dia = st.selectbox(
            "Dia",
            ["segunda","terca","quarta","quinta","sexta"]
        )

        mercados_sel = st.multiselect(
            "Mercados",
            mercados.mercado.unique()
        )

        produtos_sel = st.multiselect(
            "Produtos",
            mercados.item.unique()
        )

        if st.button("Gerar agenda"):

            novas_tarefas = []

            for m in mercados_sel:
                for p in produtos_sel:

                    novas_tarefas.append({
                        "funcionario": func,
                        "dia": dia,
                        "mercado": m,
                        "item": p
                    })

            if novas_tarefas:

                agenda = pd.concat(
                    [agenda, pd.DataFrame(novas_tarefas)],
                    ignore_index=True
                )

                agenda.to_excel("agenda.xlsx", index=False)

                st.success("Agenda criada com sucesso")

        st.dataframe(agenda)

    
    
elif menu == "Mapa":

        st.header("Mapa de mercados")

        if "lat" in mercados.columns:
            st.map(mercados[["lat","lon"]])

elif menu == "Relatórios":

        st.header("Relatórios")

        st.dataframe(relatorio)

        if st.button("Exportar PDF"):

            styles = getSampleStyleSheet()
            data = [relatorio.columns.tolist()] + relatorio.values.tolist()

            table = Table(data)

            doc = SimpleDocTemplate("relatorio.pdf")
            doc.build([Paragraph("Relatório EL KAM", styles["Title"]), table])

            st.success("PDF gerado")

# ---------------- FUNCIONARIO ----------------
else:

    st.header("Minhas tarefas")

    tarefas = agenda[agenda.funcionario == usuario]

    if len(tarefas) == 0:
        st.info("Nenhuma tarefa")
    else:

        for i,row in tarefas.iterrows():

            feito = st.checkbox(f"{row.dia} - {row.mercado} - {row.item}")

            if feito:

                foto = st.camera_input("Foto da prateleira")

                if foto:

                    nome = f"fotos/{usuario}_{date.today()}.jpg"

                    with open(nome,"wb") as f:
                        f.write(foto.getbuffer())

                relatorio = pd.concat([relatorio,pd.DataFrame({
                    "data":[date.today()],
                    "funcionario":[usuario],
                    "mercado":[row.mercado],
                    "item":[row.item],
                    "status":["feito"]
                })])

        if st.button("Salvar tarefas"):
            relatorio.to_excel("relatorio.xlsx", index=False)
            st.success("Salvo")
