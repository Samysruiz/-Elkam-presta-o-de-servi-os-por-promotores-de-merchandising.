import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="DUH Sistema",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: black;
}
h1, h2, h3 {
    color: #ff2b2b;
}
label {
    color: white !important;
}
input {
    background-color: white !important;
    color: black !important;
}
.stButton button {
    background-color: #ff2b2b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PASTA FOTO ----------------

if not os.path.exists("fotos"):
    os.makedirs("fotos")

# ---------------- BANCO ----------------

conn = sqlite3.connect("duh.db", check_same_thread=False)
c = conn.cursor()

# ---------------- TABELAS ----------------

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT,
    senha TEXT,
    tipo TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS mercados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mercado TEXT,
    endereco TEXT UNIQUE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    mercado TEXT,
    produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS agenda (
    funcionario TEXT,
    dia TEXT,
    mercado TEXT,
    produto TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS relatorio (
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

# ---------------- SESSION ----------------

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# ---------------- LOGIN ----------------

if not st.session_state["logado"]:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("## 🔑 Acesso El Kam")

        usuario_input = st.text_input("Usuário").strip().lower()
        senha_input = st.text_input("Senha", type="password")

        if st.button("ENTRAR", use_container_width=True):

            c.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
                (usuario_input, senha_input)
            )
            user = c.fetchone()

            if user:
                st.session_state["logado"] = True
                st.session_state["usuario"] = user[0]
                st.session_state["tipo"] = user[2]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

    with col2:
        if os.path.exists("el_kam_logo.png"):
            st.image("el_kam_logo.png", use_container_width=True)

    st.stop()

# ---------------- VARIÁVEIS ----------------

usuario = st.session_state["usuario"]
tipo = st.session_state["tipo"]

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.write(f"👤 {usuario}")

    if st.button("🚪 Logout"):
        st.session_state["logado"] = False
        st.rerun()

    with st.expander("🔐 Alterar senha"):
        nova = st.text_input("Nova senha", type="password")
        if st.button("Atualizar senha"):
            if nova:
                c.execute(
                    "UPDATE usuarios SET senha=? WHERE usuario=?",
                    (nova, usuario)
                )
                conn.commit()
                st.success("Senha alterada")

# =====================================================
# ==================== ADMIN ==========================
# =====================================================

if tipo == "admin":

    st.title(f"👑 Painel ADM - {usuario}")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Funcionários", "Mercados", "Agenda", "Relatórios", "Fotos"]
    )

    # ---------------- DASHBOARD ----------------

    if menu == "Dashboard":

        st.header("📊 Dashboard")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        st.metric("Relatórios enviados", len(rel))

        if len(rel) > 0:
            st.subheader("Status dos relatórios")
            graf = rel.groupby("status").size()
            st.bar_chart(graf)

            st.subheader("🏆 Ranking Promotores")
            rank = rel.groupby("funcionario").size().sort_values(ascending=False).reset_index()
            rank.columns = ["Funcionário", "Relatórios"]
            st.dataframe(rank, use_container_width=True)
        else:
            st.info("Nenhum relatório enviado ainda.")

    # ---------------- FUNCIONÁRIOS ----------------

    elif menu == "Funcionários":

        st.header("👷 Funcionários")

        with st.expander("➕ Cadastrar novo funcionário"):
            user_novo = st.text_input("Usuário")
            senha_nova = st.text_input("Senha", key="senha_func")

            if st.button("Cadastrar funcionário"):
                if user_novo.strip() == "" or senha_nova.strip() == "":
                    st.error("Preencha usuário e senha")
                else:
                    c.execute(
                        "INSERT INTO usuarios VALUES(?,?,?)",
                        (user_novo.strip().lower(), senha_nova, "funcionario")
                    )
                    conn.commit()
                    st.success(f"Funcionário '{user_novo}' criado com sucesso!")
                    st.rerun()

        st.subheader("Lista de funcionários")
        funcs = pd.read_sql("SELECT usuario, tipo FROM usuarios", conn)
        st.dataframe(funcs, use_container_width=True)

    # ---------------- MERCADOS ----------------

    elif menu == "Mercados":

        st.header("🏪 Mercados")

        with st.expander("➕ Cadastrar novo mercado"):
            mercado = st.text_input("Nome do mercado")
            endereco = st.text_input("Endereço")

            if st.button("Cadastrar mercado"):
                if not mercado or not endereco:
                    st.warning("Preencha mercado e endereço")
                else:
                    try:
                        c.execute("SELECT mercado FROM mercados WHERE endereco = ?", (endereco.strip(),))
                        resultado = c.fetchone()

                        if resultado:
                            st.error(f"Esse endereço já está cadastrado para o mercado '{resultado[0]}'.")
                        else:
                            c.execute(
                                "INSERT INTO mercados (mercado, endereco) VALUES (?,?)",
                                (mercado.strip(), endereco.strip())
                            )
                            conn.commit()
                            st.success("Mercado criado com sucesso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar mercado: {e}")

        st.subheader("Lista de mercados")
        mercados_df = pd.read_sql("SELECT id, mercado, endereco FROM mercados", conn)
        st.dataframe(mercados_df, use_container_width=True)

    # ---------------- AGENDA ----------------

    elif menu == "Agenda":

        st.header("📅 Agenda")

        with st.expander("➕ Adicionar tarefa na agenda"):
            funcs = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)
            mercados_lista = pd.read_sql("SELECT mercado FROM mercados", conn)

            if funcs.empty:
                st.warning("Nenhum funcionário cadastrado.")
            elif mercados_lista.empty:
                st.warning("Nenhum mercado cadastrado.")
            else:
                func_sel = st.selectbox("Funcionário", funcs["usuario"].tolist())
                dia_sel = st.selectbox("Dia da semana", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
                mercado_sel = st.selectbox("Mercado", mercados_lista["mercado"].tolist())
                produto_sel = st.text_input("Produto")

                if st.button("Adicionar à agenda"):
                    if not produto_sel:
                        st.warning("Informe o produto.")
                    else:
                        try:
                            # Verifica se essa combinação já existe
                            c.execute(
                                "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                (func_sel, dia_sel, mercado_sel, produto_sel)
                            )
                            ja_existe = c.fetchone()[0] > 0

                            if ja_existe:
                                st.warning("Essa tarefa já está cadastrada na agenda.")
                            else:
                                c.execute(
                                    "INSERT INTO agenda (funcionario, dia, mercado, produto) VALUES (?,?,?,?)",
                                    (func_sel, dia_sel, mercado_sel, produto_sel)
                                )
                                conn.commit()
                                st.success("Tarefa adicionada!")
                                st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Erro ao adicionar tarefa: {e}")

        st.subheader("Agenda atual")
        agenda_df = pd.read_sql("SELECT * FROM agenda", conn)
        if agenda_df.empty:
            st.info("Nenhuma tarefa cadastrada.")
        else:
            st.dataframe(agenda_df, use_container_width=True)

            if st.button("🗑️ Limpar toda a agenda"):
                c.execute("DELETE FROM agenda")
                conn.commit()
                st.success("Agenda limpa.")
                st.rerun()

    # ---------------- RELATÓRIOS ----------------

    elif menu == "Relatórios":

        st.header("📋 Relatórios")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)

        if rel.empty:
            st.info("Nenhum relatório enviado ainda.")
        else:
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                filtro_func = st.selectbox(
                    "Filtrar por funcionário",
                    ["Todos"] + rel["funcionario"].unique().tolist()
                )
            with col2:
                filtro_mercado = st.selectbox(
                    "Filtrar por mercado",
                    ["Todos"] + rel["mercado"].unique().tolist()
                )

            df_filtrado = rel.copy()
            if filtro_func != "Todos":
                df_filtrado = df_filtrado[df_filtrado["funcionario"] == filtro_func]
            if filtro_mercado != "Todos":
                df_filtrado = df_filtrado[df_filtrado["mercado"] == filtro_mercado]

            st.dataframe(df_filtrado, use_container_width=True)

    # ---------------- FOTOS ----------------

    elif menu == "Fotos":

        st.header("📸 Fotos das gôndolas")

        rel = pd.read_sql("SELECT * FROM relatorio WHERE foto != ''", conn)

        if rel.empty:
            st.info("Nenhuma foto enviada ainda.")
        else:
            for _, row in rel.iterrows():
                if row["foto"] and os.path.exists(row["foto"]):
                    st.write(f"**{row['funcionario']}** — {row['mercado']} — {row['data']}")
                    st.image(row["foto"])
                    st.divider()

# =====================================================
# ================= FUNCIONARIO =======================
# =====================================================

else:

    st.title(f"📋 Minha Agenda — {usuario}")

    tarefas = pd.read_sql(
        "SELECT * FROM agenda WHERE funcionario=?",
        conn,
        params=(usuario,)
    )

    if tarefas.empty:
        st.info("Nenhuma agenda cadastrada ainda. Aguarde seu supervisor.")
        st.stop()

    dias_ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    dias_presentes = [d for d in dias_ordem if d in tarefas["dia"].values]

    for dia in dias_presentes:

        dados_dia = tarefas[tarefas["dia"] == dia]

        st.header(f"📅 {dia.upper()}")

        mercados_dia = dados_dia["mercado"].unique()

        for mercado in mercados_dia:

            st.subheader(f"🏪 {mercado}")

            info = pd.read_sql(
                "SELECT endereco FROM mercados WHERE mercado=?",
                conn,
                params=(mercado,)
            )

            if not info.empty:
                endereco = info.iloc[0]["endereco"]
                st.write("📍", endereco)
                mapa = "https://www.google.com/maps/search/" + endereco.replace(" ", "+")
                st.markdown(f"[🗺️ Abrir rota no Google Maps]({mapa})")

            produtos_mercado = dados_dia[dados_dia["mercado"] == mercado]

            st.write("**Produtos a verificar:**")
            for i, row in produtos_mercado.iterrows():
                st.checkbox(row["produto"], key=f"check_{i}")

            foto = st.file_uploader(
                "📷 Foto da gôndola",
                key=f"foto_{mercado}_{dia}",
                type=["jpg", "jpeg", "png"]
            )

            caminho = ""
            if foto:
                caminho = f"fotos/{usuario}_{mercado}_{dia}.jpg".replace(" ", "_")
                with open(caminho, "wb") as f:
                    f.write(foto.getbuffer())
                st.image(caminho, caption="Foto enviada", width=300)

            if st.button(f"✅ Enviar relatório — {mercado}", key=f"btn_{mercado}_{dia}"):
                df_rel = pd.DataFrame([{
                    "data": str(date.today()),
                    "funcionario": usuario,
                    "mercado": mercado,
                    "produto": "varios",
                    "status": "ok",
                    "foto": caminho
                }])
                df_rel.to_sql("relatorio", conn, if_exists="append", index=False)
                st.success(f"✅ Relatório de {mercado} enviado com sucesso!")

            st.divider()
