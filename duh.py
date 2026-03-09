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
    tipo TEXT,
    primeiro_acesso INTEGER DEFAULT 1
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

# ---------------- MIGRAÇÃO DO BANCO ----------------

agenda_cols = [row[1] for row in c.execute("PRAGMA table_info(agenda)").fetchall()]
if "dia" not in agenda_cols:
    c.execute("ALTER TABLE agenda RENAME TO agenda_backup")
    c.execute("""
        CREATE TABLE agenda (
            funcionario TEXT,
            dia TEXT,
            mercado TEXT,
            produto TEXT
        )
    """)
    try:
        c.execute("INSERT INTO agenda SELECT funcionario, 'Segunda', mercado, produto FROM agenda_backup")
    except Exception:
        pass
    c.execute("DROP TABLE IF EXISTS agenda_backup")
    conn.commit()

usuarios_cols = [row[1] for row in c.execute("PRAGMA table_info(usuarios)").fetchall()]
if "primeiro_acesso" not in usuarios_cols:
    c.execute("ALTER TABLE usuarios ADD COLUMN primeiro_acesso INTEGER DEFAULT 0")
    conn.commit()

# ---------------- ADMIN PADRÃO ----------------

admin = pd.read_sql("SELECT * FROM usuarios", conn)

if admin.empty:
    c.execute("INSERT INTO usuarios VALUES('admin','123','admin', 0)")
    conn.commit()

# ---------------- SESSION ----------------

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# ---------------- LOGIN ----------------

if not st.session_state["logado"]:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("## 🔑 Acesso El Kam")

        usuario_input = st.text_input("Usuário").strip()
        senha_input = st.text_input("Senha", type="password")

        if st.button("ENTRAR", use_container_width=True):

            c.execute(
                "SELECT * FROM usuarios WHERE LOWER(usuario)=LOWER(?) AND senha=?",
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

# ---------------- PRIMEIRO ACESSO ----------------

c.execute("SELECT primeiro_acesso FROM usuarios WHERE usuario=?", (usuario,))
row_pa = c.fetchone()
primeiro_acesso = row_pa[0] if row_pa else 0

if primeiro_acesso == 1:
    st.title("🔐 Bem-vindo! Defina sua nova senha")
    st.info("É seu primeiro acesso. Por segurança, crie uma senha pessoal para continuar.")

    nova_senha = st.text_input("Nova senha", type="password")
    confirma_senha = st.text_input("Confirme a nova senha", type="password")

    if st.button("Salvar senha e entrar", use_container_width=True):
        if not nova_senha or not confirma_senha:
            st.error("Preencha os dois campos.")
        elif nova_senha != confirma_senha:
            st.error("As senhas não coincidem.")
        elif len(nova_senha) < 4:
            st.error("A senha deve ter pelo menos 4 caracteres.")
        else:
            c.execute(
                "UPDATE usuarios SET senha=?, primeiro_acesso=0 WHERE usuario=?",
                (nova_senha, usuario)
            )
            conn.commit()
            st.success("Senha definida com sucesso! Entrando...")
            st.rerun()
    st.stop()

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
            col_n, col_s = st.columns(2)
            with col_n:
                nome = st.text_input("Nome")
            with col_s:
                sobrenome = st.text_input("Sobrenome")
            st.caption("Login será **nome.sobrenome** em minúsculo. Senha padrão: **elkam** (alterada no primeiro acesso).")

            if st.button("Cadastrar funcionário"):
                if not nome.strip() or not sobrenome.strip():
                    st.error("Preencha nome e sobrenome.")
                else:
                    user_lower = f"{nome.strip().lower()}.{sobrenome.strip().lower()}"
                    c.execute("SELECT usuario FROM usuarios WHERE usuario=?", (user_lower,))
                    if c.fetchone():
                        st.error(f"Já existe um funcionário com o login '{user_lower}'.")
                    else:
                        c.execute(
                            "INSERT INTO usuarios VALUES(?,?,?,?)",
                            (user_lower, "elkam", "funcionario", 1)
                        )
                        conn.commit()
                        st.success(f"Funcionário criado! Login: **{user_lower}** | Senha padrão: **elkam**")
                        st.rerun()

        st.subheader("Lista de funcionários")
        funcs = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)

        if funcs.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            for _, row in funcs.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"👤 {row['usuario']}")
                with col2:
                    if st.button("🗑️ Excluir", key=f"del_{row['usuario']}"):
                        c.execute("DELETE FROM usuarios WHERE usuario=? AND tipo='funcionario'", (row["usuario"],))
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (row["usuario"],))
                        conn.commit()
                        st.success(f"Funcionário '{row['usuario']}' excluído.")
                        st.rerun()

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

        with st.expander("🔁 Copiar agenda de outro funcionário"):
            funcs_copy = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)

            if funcs_copy.empty:
                st.warning("Nenhum funcionário cadastrado.")
            else:
                lista_funcs = funcs_copy["usuario"].tolist()

                col_orig, col_dest = st.columns(2)
                with col_orig:
                    func_origem = st.selectbox("Copiar DE", lista_funcs, key="copy_origem")
                with col_dest:
                    func_destino = st.selectbox("Copiar PARA", lista_funcs, key="copy_destino")

                # Preview da agenda de origem
                agenda_origem = pd.read_sql(
                    "SELECT dia, mercado, produto FROM agenda WHERE funcionario=?",
                    conn, params=(func_origem,)
                )

                if agenda_origem.empty:
                    st.warning(f"'{func_origem}' não tem agenda cadastrada para copiar.")
                else:
                    st.write(f"**Agenda de {func_origem} ({len(agenda_origem)} tarefas):**")
                    st.dataframe(agenda_origem, use_container_width=True, hide_index=True)

                    substituir = st.checkbox("⚠️ Apagar agenda atual do destino antes de copiar", value=True)

                    if st.button("🔁 Copiar agenda agora"):
                        if func_origem == func_destino:
                            st.error("Origem e destino não podem ser o mesmo funcionário.")
                        else:
                            try:
                                if substituir:
                                    c.execute("DELETE FROM agenda WHERE funcionario=?", (func_destino,))

                                inseridos = 0
                                ignorados = 0
                                for _, row in agenda_origem.iterrows():
                                    c.execute(
                                        "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                        (func_destino, row["dia"], row["mercado"], row["produto"])
                                    )
                                    if c.fetchone()[0] == 0:
                                        c.execute(
                                            "INSERT INTO agenda (funcionario, dia, mercado, produto) VALUES (?,?,?,?)",
                                            (func_destino, row["dia"], row["mercado"], row["produto"])
                                        )
                                        inseridos += 1
                                    else:
                                        ignorados += 1

                                conn.commit()
                                st.success(f"✅ {inseridos} tarefas copiadas para '{func_destino}'!" +
                                           (f" ({ignorados} já existiam e foram ignoradas)" if ignorados else ""))
                                st.rerun()
                            except Exception as e:
                                conn.rollback()
                                st.error(f"Erro ao copiar agenda: {e}")

        st.subheader("Agenda atual")
        agenda_df = pd.read_sql(
            "SELECT rowid, funcionario, dia, mercado, produto FROM agenda",
            conn
        )
        if agenda_df.empty:
            st.info("Nenhuma tarefa cadastrada.")
        else:
            # Filtro por funcionário
            funcs_agenda = ["Todos"] + sorted(agenda_df["funcionario"].unique().tolist())
            filtro_ag = st.selectbox("Filtrar por funcionário", funcs_agenda, key="filtro_agenda")
            if filtro_ag != "Todos":
                agenda_df = agenda_df[agenda_df["funcionario"] == filtro_ag]

            st.caption("Marque os itens que deseja excluir e clique em **Excluir selecionados**.")

            selecionados = []
            dias_ordem_exib = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            dias_exib = [d for d in dias_ordem_exib if d in agenda_df["dia"].values]

            for dia_exib in dias_exib:
                st.markdown(f"**📅 {dia_exib}**")
                df_dia = agenda_df[agenda_df["dia"] == dia_exib]

                for _, row in df_dia.iterrows():
                    col_check, col_info = st.columns([1, 8])
                    with col_check:
                        marcado = st.checkbox(
                            "", 
                            key=f"del_item_{row['rowid']}",
                            label_visibility="collapsed"
                        )
                    with col_info:
                        st.write(f"🏪 **{row['mercado']}** — {row['produto']} — `{row['funcionario']}`")
                    if marcado:
                        selecionados.append(int(row["rowid"]))

            st.markdown("---")
            col_btn1, col_btn2 = st.columns([2, 1])

            with col_btn1:
                if selecionados:
                    st.warning(f"{len(selecionados)} item(ns) selecionado(s) para exclusão.")

            with col_btn2:
                if st.button("🗑️ Excluir selecionados", disabled=len(selecionados) == 0):
                    for rid in selecionados:
                        c.execute("DELETE FROM agenda WHERE rowid=?", (rid,))
                    conn.commit()
                    st.success(f"✅ {len(selecionados)} item(ns) excluído(s).")
                    st.rerun()

            st.markdown("---")
            with st.expander("⚠️ Limpar agenda completa"):
                st.warning("Isso apaga todos os itens do filtro selecionado. Sem recuperação.")
                if st.button("Confirmar limpeza total"):
                    if filtro_ag == "Todos":
                        c.execute("DELETE FROM agenda")
                        st.success("Toda a agenda foi limpa.")
                    else:
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (filtro_ag,))
                        st.success(f"Agenda de '{filtro_ag}' limpa.")
                    conn.commit()
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

    st.title(f"📋 Agenda da Semana — {usuario}")

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

    # ---- TABELA VISUAL IGUAL À PLANILHA ----

    st.markdown("""
    <style>
    .tabela-agenda {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        margin-bottom: 30px;
    }
    .tabela-agenda th {
        background-color: #1a1a1a;
        color: #ff2b2b;
        text-align: center;
        padding: 10px;
        border: 1px solid #333;
        font-size: 15px;
        text-transform: uppercase;
    }
    .tabela-agenda td {
        padding: 6px 10px;
        border: 1px solid #2a2a2a;
        color: white;
        vertical-align: top;
        text-align: left;
    }
    .mercado-nome {
        color: #ff2b2b;
        font-weight: bold;
        font-size: 13px;
        padding-top: 8px;
    }
    .produto-item {
        color: #cccccc;
        font-size: 13px;
        padding-left: 4px;
    }
    .celula-vazia {
        background-color: #0d0d0d;
    }
    </style>
    """, unsafe_allow_html=True)

    # Monta estrutura: { mercado: { dia: [produtos] } }
    estrutura = {}
    for _, row in tarefas.iterrows():
        m = row["mercado"]
        d = row["dia"]
        p = row["produto"]
        if m not in estrutura:
            estrutura[m] = {}
        if d not in estrutura[m]:
            estrutura[m][d] = []
        estrutura[m][d].append(p)

    mercados_semana = list(estrutura.keys())

    # Calcula quantas linhas cada mercado precisa (máx de produtos por dia)
    html = '<table class="tabela-agenda"><thead><tr>'
    for d in dias_presentes:
        html += f"<th>{d}</th>"
    html += "</tr></thead><tbody>"

    # Agrupa por mercado — cada mercado é um bloco de linhas
    for mercado in mercados_semana:
        max_produtos = max(
            len(estrutura[mercado].get(d, [])) for d in dias_presentes
        )
        # Linha do nome do mercado
        html += "<tr>"
        for d in dias_presentes:
            if estrutura[mercado].get(d):
                html += f'<td class="mercado-nome">🏪 {mercado}</td>'
            else:
                html += '<td class="celula-vazia"></td>'
        html += "</tr>"

        # Linhas dos produtos
        for idx in range(max_produtos):
            html += "<tr>"
            for d in dias_presentes:
                prods = estrutura[mercado].get(d, [])
                if idx < len(prods):
                    html += f'<td class="produto-item">• {prods[idx]}</td>'
                else:
                    html += '<td class="celula-vazia"></td>'
            html += "</tr>"

    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

    # ---- DETALHES POR DIA (clicável) ----

    st.markdown("---")
    st.subheader("📍 Detalhes por dia")

    dia_sel = st.selectbox("Selecione o dia", dias_presentes)

    dados_dia = tarefas[tarefas["dia"] == dia_sel]
    mercados_dia = dados_dia["mercado"].unique()

    for mercado in mercados_dia:

        with st.expander(f"🏪 {mercado}", expanded=True):

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
                st.checkbox(row["produto"], key=f"check_{dia_sel}_{i}")

            foto = st.file_uploader(
                "📷 Foto da gôndola",
                key=f"foto_{mercado}_{dia_sel}",
                type=["jpg", "jpeg", "png"]
            )

            caminho = ""
            if foto:
                caminho = f"fotos/{usuario}_{mercado}_{dia_sel}.jpg".replace(" ", "_")
                with open(caminho, "wb") as f:
                    f.write(foto.getbuffer())
                st.image(caminho, caption="Foto enviada", width=300)

            if st.button(f"✅ Enviar relatório", key=f"btn_{mercado}_{dia_sel}"):
                df_rel = pd.DataFrame([{
                    "data": str(date.today()),
                    "funcionario": usuario,
                    "mercado": mercado,
                    "produto": "varios",
                    "status": "ok",
                    "foto": caminho
                }])
                df_rel.to_sql("relatorio", conn, if_exists="append", index=False)
                st.success(f"✅ Relatório de {mercado} enviado!")
