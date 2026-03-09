import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date, datetime, timedelta

# ═══════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="El Kam | Sistema",
    page_icon="🔴",
    layout="wide"
)

# ═══════════════════════════════════════════════
#  DESIGN SYSTEM
# ═══════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap');

html, body, [class*="css"], * { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #0a0a0a; }
.block-container { padding: 2rem 2.5rem !important; }

[data-testid="stSidebar"] {
    background-color: #0f0f0f !important;
    border-right: 1px solid #1c1c1c !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #d0d0d0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio > label {
    color: #555 !important; font-size: 10px !important;
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600 !important;
}

h1,h2,h3,h4 { color: #ffffff !important; }
p, li { color: #aaaaaa; line-height: 1.6; }
label { color: #777 !important; font-size: 12px !important; font-weight: 500 !important; }

input, textarea, [data-baseweb="input"] input {
    background-color: #141414 !important; color: #ffffff !important;
    border: 1px solid #242424 !important; border-radius: 8px !important; font-size: 14px !important;
}
input:focus, textarea:focus {
    border-color: #ff2b2b !important;
    box-shadow: 0 0 0 3px rgba(255,43,43,0.15) !important;
}
.stSelectbox > div > div, [data-baseweb="select"] > div {
    background-color: #141414 !important; border: 1px solid #242424 !important;
    border-radius: 8px !important; color: #fff !important;
}
[data-baseweb="popover"] * { background-color: #1a1a1a !important; color: #fff !important; }

.stButton > button {
    background-color: #ff2b2b !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 13px !important;
    padding: 10px 20px !important; transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background-color: #e01f1f !important;
    box-shadow: 0 4px 16px rgba(255,43,43,0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background-color: #1f1f1f !important; color: #444 !important;
    box-shadow: none !important; transform: none !important;
}

[data-testid="metric-container"] {
    background: linear-gradient(145deg, #141414, #111);
    border: 1px solid #1c1c1c; border-radius: 14px; padding: 20px 22px !important;
}
[data-testid="metric-container"]:hover { border-color: #ff2b2b44; }
[data-testid="metric-container"] label {
    color: #555 !important; font-size: 11px !important;
    text-transform: uppercase; letter-spacing: 1px; font-weight: 600 !important;
}
[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 30px !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden; border: 1px solid #1c1c1c !important; }
.stDataFrame thead tr th {
    background-color: #111 !important; color: #555 !important;
    font-size: 10px !important; text-transform: uppercase; letter-spacing: 1px;
    border-bottom: 1px solid #1c1c1c !important; padding: 10px 14px !important;
}
.stDataFrame tbody tr td {
    background-color: #0d0d0d !important; color: #ccc !important;
    border-bottom: 1px solid #141414 !important; font-size: 13px !important;
}
.stDataFrame tbody tr:hover td { background-color: #141414 !important; }

[data-testid="stExpander"] {
    background-color: #111 !important; border: 1px solid #1c1c1c !important;
    border-radius: 10px !important; overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: #ddd !important; font-weight: 600 !important; font-size: 13px !important;
    padding: 14px 16px !important;
}
[data-testid="stExpander"] summary:hover { background-color: #161616 !important; }
[data-testid="stExpander"] > div > div { padding: 0 16px 16px 16px !important; }

.stSuccess { background-color: #0a1f13 !important; border-left: 3px solid #22c55e !important; border-radius: 10px !important; }
.stError   { background-color: #1f0a0a !important; border-left: 3px solid #ff2b2b !important; border-radius: 10px !important; }
.stWarning { background-color: #1f180a !important; border-left: 3px solid #f59e0b !important; border-radius: 10px !important; }
.stInfo    { background-color: #0a111f !important; border-left: 3px solid #3b82f6 !important; border-radius: 10px !important; }

.stProgress > div { background-color: #1c1c1c !important; border-radius: 99px !important; height: 6px !important; }
.stProgress > div > div { background: linear-gradient(90deg,#ff2b2b,#ff6b6b) !important; border-radius: 99px !important; }

.stCheckbox label { color: #bbb !important; font-size: 13px !important; }
[data-testid="stFileUploader"] {
    background-color: #111 !important; border: 1px dashed #242424 !important; border-radius: 10px !important;
}
hr { border: none !important; border-top: 1px solid #1c1c1c !important; margin: 20px 0 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #242424; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #ff2b2b; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════

def page_header(supertitle, title):
    st.markdown(f"""
    <div style='margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid #1c1c1c'>
        <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2px;
                    text-transform:uppercase;margin-bottom:4px'>{supertitle}</div>
        <div style='color:#ffffff;font-size:24px;font-weight:800'>{title}</div>
    </div>
    """, unsafe_allow_html=True)

def section_title(text):
    st.markdown(f"""
    <div style='color:#555;font-size:10px;font-weight:700;letter-spacing:1.5px;
                text-transform:uppercase;margin:20px 0 10px;
                padding-bottom:6px;border-bottom:1px solid #1c1c1c'>{text}</div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  BANCO
# ═══════════════════════════════════════════════

if not os.path.exists("fotos"):
    os.makedirs("fotos")

conn = sqlite3.connect("duh.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT, senha TEXT, tipo TEXT, primeiro_acesso INTEGER DEFAULT 1)""")
c.execute("""CREATE TABLE IF NOT EXISTS mercados (
    id INTEGER PRIMARY KEY AUTOINCREMENT, mercado TEXT, endereco TEXT UNIQUE)""")
c.execute("""CREATE TABLE IF NOT EXISTS produtos (mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS agenda (
    funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS relatorio (
    data TEXT, funcionario TEXT, mercado TEXT, produto TEXT, status TEXT, foto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT, hora TEXT, remetente TEXT, tipo TEXT, mensagem TEXT, lido INTEGER DEFAULT 0)""")
conn.commit()

# Migrações
agenda_cols = [r[1] for r in c.execute("PRAGMA table_info(agenda)").fetchall()]
if "dia" not in agenda_cols:
    c.execute("ALTER TABLE agenda RENAME TO agenda_bkp")
    c.execute("CREATE TABLE agenda (funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)")
    try: c.execute("INSERT INTO agenda SELECT funcionario,'Segunda',mercado,produto FROM agenda_bkp")
    except: pass
    c.execute("DROP TABLE IF EXISTS agenda_bkp")
    conn.commit()

usuarios_cols = [r[1] for r in c.execute("PRAGMA table_info(usuarios)").fetchall()]
if "primeiro_acesso" not in usuarios_cols:
    c.execute("ALTER TABLE usuarios ADD COLUMN primeiro_acesso INTEGER DEFAULT 0")
    conn.commit()

if pd.read_sql("SELECT * FROM usuarios", conn).empty:
    c.execute("INSERT INTO usuarios VALUES('admin','123','admin',0)")
    conn.commit()

# ═══════════════════════════════════════════════
#  SESSION
# ═══════════════════════════════════════════════

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# ═══════════════════════════════════════════════
#  LOGIN
# ═══════════════════════════════════════════════

if not st.session_state["logado"]:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='margin-bottom:36px'>
            <div style='color:#ff2b2b;font-size:11px;font-weight:700;letter-spacing:2.5px;
                        text-transform:uppercase;margin-bottom:10px'>El Kam Merchandising</div>
            <div style='color:#ffffff;font-size:34px;font-weight:900;line-height:1.1;
                        margin-bottom:10px'>Sistema de<br>Promotores</div>
            <div style='color:#333;font-size:13px'>Acesse com suas credenciais</div>
        </div>
        """, unsafe_allow_html=True)

        usuario_input = st.text_input("Usuário")
        senha_input   = st.text_input("Senha", type="password")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("ENTRAR →", use_container_width=True):
            c.execute("SELECT * FROM usuarios WHERE LOWER(usuario)=LOWER(?) AND senha=?",
                      (usuario_input.strip(), senha_input))
            user = c.fetchone()
            if user:
                st.session_state["logado"]  = True
                st.session_state["usuario"] = user[0]
                st.session_state["tipo"]    = user[2]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

        st.markdown("""
        <div style='margin-top:16px;color:#2a2a2a;font-size:12px'>
            Esqueceu sua senha? Fale com o administrador.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)
        if os.path.exists("el_kam_logo.png"):
            st.image("el_kam_logo.png", use_container_width=True)
        else:
            st.markdown("""
            <div style='background:linear-gradient(135deg,#140000,#1e0000);
                        border:1px solid #ff2b2b22;border-radius:20px;height:320px;
                        display:flex;align-items:center;justify-content:center;
                        flex-direction:column;gap:14px'>
                <div style='font-size:56px'>🏪</div>
                <div style='color:#ff2b2b;font-weight:800;font-size:24px;letter-spacing:3px'>EL KAM</div>
                <div style='color:#2a2a2a;font-size:11px;letter-spacing:2px'>MERCHANDISING</div>
            </div>
            """, unsafe_allow_html=True)

    st.stop()

# ═══════════════════════════════════════════════
#  VARIÁVEIS
# ═══════════════════════════════════════════════

usuario = st.session_state["usuario"]
tipo    = st.session_state["tipo"]

# ═══════════════════════════════════════════════
#  PRIMEIRO ACESSO
# ═══════════════════════════════════════════════

c.execute("SELECT primeiro_acesso FROM usuarios WHERE usuario=?", (usuario,))
row_pa = c.fetchone()
if row_pa and row_pa[0] == 1:
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    col_pa, _ = st.columns([1, 2])
    with col_pa:
        st.markdown("""
        <div style='margin-bottom:28px'>
            <div style='color:#ff2b2b;font-size:11px;font-weight:700;letter-spacing:2px;
                        text-transform:uppercase;margin-bottom:8px'>Primeiro acesso</div>
            <div style='color:#fff;font-size:26px;font-weight:800;margin-bottom:8px'>Crie sua senha</div>
            <div style='color:#444;font-size:13px'>Por segurança, defina uma senha pessoal para continuar.</div>
        </div>
        """, unsafe_allow_html=True)
        nova_s = st.text_input("Nova senha", type="password", key="pa_nova")
        conf_s = st.text_input("Confirme a senha", type="password", key="pa_conf")
        if st.button("Salvar e entrar →", use_container_width=True):
            if not nova_s or not conf_s:
                st.error("Preencha os dois campos.")
            elif nova_s != conf_s:
                st.error("As senhas não coincidem.")
            elif len(nova_s) < 4:
                st.error("Mínimo de 4 caracteres.")
            else:
                c.execute("UPDATE usuarios SET senha=?, primeiro_acesso=0 WHERE usuario=?", (nova_s, usuario))
                conn.commit()
                st.success("Senha definida! Entrando...")
                st.rerun()
    st.stop()

# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"""
    <div style='padding:20px 16px 16px;border-bottom:1px solid #1c1c1c;margin-bottom:16px'>
        <div style='color:#ff2b2b;font-size:9px;font-weight:700;letter-spacing:2.5px;
                    text-transform:uppercase;margin-bottom:3px'>El Kam</div>
        <div style='color:#fff;font-size:15px;font-weight:700'>Merchandising</div>
    </div>
    <div style='padding:0 16px 16px'>
        <div style='color:#333;font-size:10px;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:3px'>Logado como</div>
        <div style='color:#ddd;font-weight:600;font-size:13px'>👤 {usuario}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sair", use_container_width=True):
        st.session_state["logado"] = False
        st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    with st.expander("🔐 Alterar senha"):
        nova = st.text_input("Nova senha", type="password", key="sb_nova")
        if st.button("Salvar senha"):
            if nova.strip():
                c.execute("UPDATE usuarios SET senha=? WHERE usuario=?", (nova, usuario))
                conn.commit()
                st.success("Senha alterada!")
            else:
                st.error("Digite uma senha.")

# ═══════════════════════════════════════════════════════
#  ADMIN
# ═══════════════════════════════════════════════════════

if tipo == "admin":

    menu = st.sidebar.selectbox(
        "MENU",
        ["Dashboard", "Funcionários", "Mercados", "Agenda", "Relatórios", "Fotos", "Chat"]
    )

    # ── DASHBOARD ─────────────────────────────────────────

    if menu == "Dashboard":
        page_header("Visão Geral", "Dashboard")

        rel = pd.read_sql("SELECT * FROM relatorio", conn)
        hoje         = date.today()
        ini_sem      = hoje - timedelta(days=hoje.weekday())
        ini_ant      = ini_sem - timedelta(days=7)
        fim_ant      = ini_sem - timedelta(days=1)

        cols_rel = ["data","funcionario","mercado","produto","status","foto"]
        if not rel.empty:
            rel["data"] = pd.to_datetime(rel["data"])
            rel_sem = rel[rel["data"] >= pd.Timestamp(ini_sem)]
            rel_ant = rel[(rel["data"] >= pd.Timestamp(ini_ant)) & (rel["data"] <= pd.Timestamp(fim_ant))]
        else:
            rel_sem = pd.DataFrame(columns=cols_rel)
            rel_ant = pd.DataFrame(columns=cols_rel)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Relatórios esta semana", len(rel_sem),
                  delta=f"{len(rel_sem)-len(rel_ant):+d} vs anterior")
        fa = rel_sem["funcionario"].nunique() if not rel_sem.empty else 0
        fb = rel_ant["funcionario"].nunique() if not rel_ant.empty else 0
        c2.metric("Funcionários ativos", fa, delta=f"{fa-fb:+d}")
        ma = rel_sem["mercado"].nunique() if not rel_sem.empty else 0
        mb = rel_ant["mercado"].nunique() if not rel_ant.empty else 0
        c3.metric("Mercados visitados", ma, delta=f"{ma-mb:+d}")
        c4.metric("Total histórico", len(rel))

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        section_title("Comparativo semana atual vs anterior")
        dias_label = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
        def por_dia(df):
            if df.empty: return [0]*7
            df = df.copy(); df["wd"] = df["data"].dt.weekday
            return [len(df[df["wd"]==i]) for i in range(7)]
        st.bar_chart(pd.DataFrame({
            "Semana atual": por_dia(rel_sem),
            "Semana anterior": por_dia(rel_ant)
        }, index=dias_label))

        section_title("Quem mais trabalhou esta semana")
        if not rel_sem.empty:
            rank = (rel_sem.groupby("funcionario")
                    .agg(rel=("mercado","count"), merc=("mercado","nunique"))
                    .sort_values("rel", ascending=False).reset_index())
            mx = rank["rel"].max()
            for _, r in rank.iterrows():
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
                    f"<span style='color:#ddd;font-size:13px;font-weight:600'>{r['funcionario']}</span>"
                    f"<span style='color:#444;font-size:12px'>{r['rel']} relatórios · {r['merc']} mercados</span>"
                    f"</div>", unsafe_allow_html=True)
                st.progress(int(r["rel"]/mx*100))
        else:
            st.info("Nenhum relatório esta semana.")

        col_a, col_b = st.columns(2)
        with col_a:
            section_title("Mercados mais visitados")
            if not rel_sem.empty:
                mv = (rel_sem.groupby("mercado")
                      .agg(v=("funcionario","count"), p=("funcionario","nunique"))
                      .sort_values("v",ascending=False).reset_index())
                mv.columns = ["Mercado","Visitas","Promotores"]
                st.dataframe(mv, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados.")

        with col_b:
            section_title("Histórico geral")
            if not rel.empty:
                hist = rel.groupby(rel["data"].dt.date).size().reset_index()
                hist.columns = ["Data","Qtd"]
                st.line_chart(hist.set_index("Data"))
            else:
                st.info("Sem dados.")

        nao_lidas = pd.read_sql(
            "SELECT COUNT(*) as t FROM chat WHERE tipo='funcionario' AND lido=0", conn).iloc[0]["t"]
        if nao_lidas > 0:
            st.warning(f"💬 **{int(nao_lidas)}** mensagem(ns) não lida(s) no Chat.")

    # ── FUNCIONÁRIOS ──────────────────────────────────────

    elif menu == "Funcionários":
        page_header("Gestão", "Funcionários")

        with st.expander("➕ Cadastrar novo funcionário"):
            cn, cs = st.columns(2)
            with cn: nome      = st.text_input("Nome")
            with cs: sobrenome = st.text_input("Sobrenome")
            st.caption("Login: **nome.sobrenome** · Senha padrão: **elkam** (trocada no 1º acesso)")
            if st.button("Cadastrar funcionário"):
                if not nome.strip() or not sobrenome.strip():
                    st.error("Preencha nome e sobrenome.")
                else:
                    login = f"{nome.strip().lower()}.{sobrenome.strip().lower()}"
                    c.execute("SELECT usuario FROM usuarios WHERE usuario=?", (login,))
                    if c.fetchone():
                        st.error(f"Login '{login}' já existe.")
                    else:
                        c.execute("INSERT INTO usuarios VALUES(?,?,?,?)", (login,"elkam","funcionario",1))
                        conn.commit()
                        st.success(f"✅ Criado! Login: **{login}** · Senha: **elkam**")
                        st.rerun()

        section_title("Funcionários cadastrados")
        funcs = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)

        if funcs.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            for _, row in funcs.iterrows():
                col_i, col_r, col_e = st.columns([5, 2, 1])
                with col_i:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;font-weight:600;padding:10px 0'>"
                        f"👤 {row['usuario']}</div>", unsafe_allow_html=True)
                with col_r:
                    if st.button("🔑 Resetar senha", key=f"reset_{row['usuario']}",
                                 help="Reseta para 'elkam' e força troca no próximo acesso"):
                        c.execute("UPDATE usuarios SET senha='elkam', primeiro_acesso=1 WHERE usuario=?",
                                  (row["usuario"],))
                        conn.commit()
                        st.success(f"Senha de **{row['usuario']}** resetada para **elkam**.")
                        st.rerun()
                with col_e:
                    if st.button("🗑️", key=f"del_{row['usuario']}"):
                        c.execute("DELETE FROM usuarios WHERE usuario=? AND tipo='funcionario'", (row["usuario"],))
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (row["usuario"],))
                        conn.commit()
                        st.rerun()

    # ── MERCADOS ──────────────────────────────────────────

    elif menu == "Mercados":
        page_header("Cadastro", "Mercados")

        with st.expander("➕ Novo mercado"):
            cm, ce = st.columns(2)
            with cm: mercado  = st.text_input("Nome do mercado")
            with ce: endereco = st.text_input("Endereço")
            if st.button("Cadastrar mercado"):
                if not mercado.strip() or not endereco.strip():
                    st.warning("Preencha nome e endereço.")
                else:
                    c.execute("SELECT mercado FROM mercados WHERE endereco=?", (endereco.strip(),))
                    dup = c.fetchone()
                    if dup:
                        st.error(f"Endereço já cadastrado para '{dup[0]}'.")
                    else:
                        try:
                            c.execute("INSERT INTO mercados (mercado,endereco) VALUES(?,?)",
                                      (mercado.strip(), endereco.strip()))
                            conn.commit()
                            st.success("✅ Mercado cadastrado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

        section_title("Lista de mercados")
        mdf = pd.read_sql("SELECT id, mercado, endereco FROM mercados", conn)
        st.dataframe(mdf, use_container_width=True, hide_index=True)

    # ── AGENDA ────────────────────────────────────────────

    elif menu == "Agenda":
        page_header("Planejamento", "Agenda")

        with st.expander("➕ Adicionar tarefa"):
            funcs_ag = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)
            mercs_ag = pd.read_sql("SELECT mercado FROM mercados", conn)
            if funcs_ag.empty:
                st.warning("Nenhum funcionário cadastrado.")
            elif mercs_ag.empty:
                st.warning("Nenhum mercado cadastrado.")
            else:
                ca, cb, cc, cd = st.columns(4)
                with ca: fs = st.selectbox("Funcionário", funcs_ag["usuario"].tolist())
                with cb: ds = st.selectbox("Dia", ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado"])
                with cc: ms = st.selectbox("Mercado", mercs_ag["mercado"].tolist())
                with cd: ps = st.text_input("Produto")
                if st.button("Adicionar"):
                    if not ps.strip():
                        st.warning("Informe o produto.")
                    else:
                        try:
                            c.execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                      (fs, ds, ms, ps))
                            if c.fetchone()[0] > 0:
                                st.warning("Tarefa já existe.")
                            else:
                                c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                          (fs, ds, ms, ps.strip()))
                                conn.commit()
                                st.success("✅ Adicionado!")
                                st.rerun()
                        except Exception as e:
                            conn.rollback(); st.error(f"Erro: {e}")

        with st.expander("🔁 Copiar agenda entre funcionários"):
            funcs_cp = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)
            if funcs_cp.empty:
                st.warning("Nenhum funcionário.")
            else:
                lista = funcs_cp["usuario"].tolist()
                co1, co2 = st.columns(2)
                with co1: fo = st.selectbox("Copiar DE",   lista, key="cp_de")
                with co2: fd = st.selectbox("Copiar PARA", lista, key="cp_para")
                ag_orig = pd.read_sql("SELECT dia,mercado,produto FROM agenda WHERE funcionario=?",
                                      conn, params=(fo,))
                if ag_orig.empty:
                    st.warning(f"'{fo}' não tem agenda.")
                else:
                    st.dataframe(ag_orig, use_container_width=True, hide_index=True)
                    apagar = st.checkbox("Apagar agenda atual do destino antes de copiar", value=True)
                    if st.button("🔁 Copiar"):
                        if fo == fd:
                            st.error("Origem e destino iguais.")
                        else:
                            if apagar:
                                c.execute("DELETE FROM agenda WHERE funcionario=?", (fd,))
                            ins = 0
                            for _, r in ag_orig.iterrows():
                                c.execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                          (fd, r["dia"], r["mercado"], r["produto"]))
                                if c.fetchone()[0] == 0:
                                    c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (fd, r["dia"], r["mercado"], r["produto"]))
                                    ins += 1
                            conn.commit()
                            st.success(f"✅ {ins} tarefas copiadas para '{fd}'!")
                            st.rerun()

        section_title("Agenda atual")
        ag_df = pd.read_sql("SELECT rowid, funcionario, dia, mercado, produto FROM agenda", conn)

        if ag_df.empty:
            st.info("Nenhuma tarefa cadastrada.")
        else:
            funcs_filt = ["Todos"] + sorted(ag_df["funcionario"].unique().tolist())
            filt = st.selectbox("Filtrar por funcionário", funcs_filt, key="filt_ag")
            if filt != "Todos":
                ag_df = ag_df[ag_df["funcionario"] == filt]

            st.caption("Marque os itens e clique em **Excluir selecionados**.")
            selecionados = []
            for dia_e in ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado"]:
                df_d = ag_df[ag_df["dia"] == dia_e]
                if df_d.empty: continue
                st.markdown(
                    f"<div style='color:#444;font-size:10px;font-weight:700;letter-spacing:1px;"
                    f"text-transform:uppercase;margin:14px 0 6px'>📅 {dia_e}</div>",
                    unsafe_allow_html=True)
                for _, row in df_d.iterrows():
                    ck, ci = st.columns([1, 10])
                    with ck:
                        if st.checkbox("", key=f"sel_{row['rowid']}", label_visibility="collapsed"):
                            selecionados.append(int(row["rowid"]))
                    with ci:
                        st.markdown(
                            f"<div style='color:#ccc;font-size:13px;padding:6px 0'>"
                            f"🏪 <b style='color:#ddd'>{row['mercado']}</b>"
                            f" <span style='color:#666'>·</span> {row['produto']}"
                            f" <span style='color:#333'>· {row['funcionario']}</span></div>",
                            unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            ce1, ce2 = st.columns([3, 1])
            with ce1:
                if selecionados:
                    st.warning(f"{len(selecionados)} item(ns) selecionado(s).")
            with ce2:
                if st.button("🗑️ Excluir selecionados", disabled=not selecionados):
                    for rid in selecionados:
                        c.execute("DELETE FROM agenda WHERE rowid=?", (rid,))
                    conn.commit()
                    st.success(f"✅ {len(selecionados)} excluído(s).")
                    st.rerun()

            with st.expander("⚠️ Limpar agenda completa"):
                st.warning("Apaga todos os itens do filtro. Irreversível.")
                if st.button("Confirmar limpeza"):
                    if filt == "Todos":
                        c.execute("DELETE FROM agenda")
                    else:
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (filt,))
                    conn.commit(); st.rerun()

    # ── RELATÓRIOS ────────────────────────────────────────

    elif menu == "Relatórios":
        page_header("Acompanhamento", "Relatórios")

        rel = pd.read_sql("SELECT rowid, * FROM relatorio", conn)
        if rel.empty:
            st.info("Nenhum relatório enviado ainda.")
        else:
            cf, cm2 = st.columns(2)
            with cf: ff = st.selectbox("Funcionário", ["Todos"]+rel["funcionario"].unique().tolist())
            with cm2: fm = st.selectbox("Mercado", ["Todos"]+rel["mercado"].unique().tolist())
            df_f = rel.copy()
            if ff != "Todos": df_f = df_f[df_f["funcionario"]==ff]
            if fm != "Todos": df_f = df_f[df_f["mercado"]==fm]

            st.caption("Marque os relatórios que deseja excluir e clique em **Excluir selecionados**.")
            selecionados_rel = []
            for _, row in df_f.iterrows():
                ck, ci = st.columns([1, 10])
                with ck:
                    if st.checkbox("", key=f"rel_{row['rowid']}", label_visibility="collapsed"):
                        selecionados_rel.append(int(row["rowid"]))
                with ci:
                    st.markdown(
                        f"<div style='color:#ccc;font-size:13px;padding:6px 0'>"
                        f"<b style='color:#ddd'>{row['funcionario']}</b>"
                        f" <span style='color:#444'>·</span> {row['mercado']}"
                        f" <span style='color:#444'>·</span> {row['data']}"
                        f" <span style='color:#333'>· status: {row['status']}</span></div>",
                        unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            cr1, cr2 = st.columns([3, 1])
            with cr1:
                if selecionados_rel:
                    st.warning(f"{len(selecionados_rel)} relatório(s) selecionado(s).")
            with cr2:
                if st.button("🗑️ Excluir selecionados", key="del_rel", disabled=not selecionados_rel):
                    for rid in selecionados_rel:
                        c.execute("DELETE FROM relatorio WHERE rowid=?", (rid,))
                    conn.commit()
                    st.success(f"✅ {len(selecionados_rel)} relatório(s) excluído(s).")
                    st.rerun()

    # ── FOTOS ─────────────────────────────────────────────

    elif menu == "Fotos":
        page_header("Registros", "Fotos das Gôndolas")

        rel = pd.read_sql("SELECT * FROM relatorio WHERE foto != ''", conn)
        if rel.empty:
            st.info("Nenhuma foto enviada ainda.")
        else:
            for _, row in rel.iterrows():
                if row["foto"] and os.path.exists(row["foto"]):
                    st.markdown(
                        f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:10px;"
                        f"padding:12px 16px;margin-bottom:8px'>"
                        f"<span style='color:#fff;font-weight:600'>{row['funcionario']}</span>"
                        f"<span style='color:#333'> · </span><span style='color:#888'>{row['mercado']}</span>"
                        f"<span style='color:#333'> · {row['data']}</span></div>",
                        unsafe_allow_html=True)
                    st.image(row["foto"], width=420)
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── CHAT ADMIN ────────────────────────────────────────

    elif menu == "Chat":
        page_header("Comunicação", "Chat com Funcionários")

        c.execute("UPDATE chat SET lido=1 WHERE tipo='funcionario'")
        conn.commit()

        funcs_ch = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)

        if funcs_ch.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            func_sel = st.selectbox("Conversa com:", funcs_ch["usuario"].tolist())

            hist = pd.read_sql(
                "SELECT * FROM chat WHERE (remetente=? AND tipo='funcionario') "
                "OR (remetente=? AND tipo='admin') ORDER BY id",
                conn, params=(func_sel, func_sel))

            st.markdown("""
            <style>
            .chat-wrap{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:14px;
                       padding:20px;min-height:320px;max-height:440px;overflow-y:auto;margin-bottom:14px}
            .bm-adm{background:#ff2b2b;color:#fff;border-radius:14px 14px 2px 14px;
                    padding:9px 14px;margin:5px 0 2px;max-width:66%;float:right;clear:both;font-size:13px;line-height:1.5}
            .bm-fun{background:#1a1a1a;color:#ddd;border-radius:14px 14px 14px 2px;
                    padding:9px 14px;margin:5px 0 2px;max-width:66%;float:left;clear:both;font-size:13px;line-height:1.5}
            .bm-hora{font-size:10px;color:#2a2a2a;clear:both;margin-bottom:5px}
            .bm-hr{text-align:right}
            </style>
            """, unsafe_allow_html=True)

            html = '<div class="chat-wrap">'
            if hist.empty:
                html += '<p style="color:#2a2a2a;text-align:center;padding-top:120px">Nenhuma mensagem ainda.</p>'
            else:
                for _, msg in hist.iterrows():
                    if msg["tipo"] == "admin":
                        html += f'<div class="bm-adm">{msg["mensagem"]}</div>'
                        html += f'<div class="bm-hora bm-hr">{msg["hora"]}</div>'
                    else:
                        html += f'<div class="bm-fun">{msg["mensagem"]}</div>'
                        html += f'<div class="bm-hora">{msg["hora"]}</div>'
            html += '<div style="clear:both"></div></div>'
            st.markdown(html, unsafe_allow_html=True)

            ci, cb = st.columns([6, 1])
            with ci:
                msg_a = st.text_input("msg_a", label_visibility="collapsed",
                                      placeholder=f"Mensagem para {func_sel}...", key="chat_adm")
            with cb:
                if st.button("Enviar", key="send_adm"):
                    if msg_a.strip():
                        now = datetime.now()
                        c.execute("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                                  (str(now.date()), now.strftime("%H:%M"), func_sel, "admin", msg_a.strip(), 1))
                        conn.commit(); st.rerun()

# ═══════════════════════════════════════════════════════
#  FUNCIONÁRIO
# ═══════════════════════════════════════════════════════

else:

    nao_lidas_f = pd.read_sql(
        "SELECT COUNT(*) as t FROM chat WHERE remetente=? AND tipo='admin' AND lido=0",
        conn, params=(usuario,)).iloc[0]["t"]

    aba_ag   = "📋  Agenda"
    aba_chat = f"💬  Chat{'  ●' if nao_lidas_f > 0 else ''}"
    aba = st.sidebar.radio("NAVEGAÇÃO", [aba_ag, aba_chat])

    # ── AGENDA ──

    if aba == aba_ag:

        nome_exib = usuario.split(".")[0].capitalize()
        page_header("Minha semana", f"Olá, {nome_exib}!")

        tarefas = pd.read_sql("SELECT * FROM agenda WHERE funcionario=?", conn, params=(usuario,))

        if tarefas.empty:
            st.info("Nenhuma agenda cadastrada ainda. Aguarde seu supervisor.")
            st.stop()

        dias_ordem   = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado"]
        dias_present = [d for d in dias_ordem if d in tarefas["dia"].values]

        estrutura = {}
        for _, r in tarefas.iterrows():
            estrutura.setdefault(r["mercado"], {}).setdefault(r["dia"], []).append(r["produto"])

        html = """
        <style>
        .tab-ag{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:28px}
        .tab-ag th{background:#111;color:#ff2b2b;text-align:center;padding:12px 14px;
                   border-bottom:2px solid #1c1c1c;font-size:10px;letter-spacing:1.5px;text-transform:uppercase}
        .tab-ag td{padding:6px 12px;border:1px solid #141414;background:#0a0a0a;vertical-align:top}
        .mn{color:#ff2b2b;font-weight:700;font-size:12px;padding-top:8px}
        .pi{color:#888;font-size:12px}
        .vz{background:#080808}
        </style><table class="tab-ag"><thead><tr>"""
        for d in dias_present:
            html += f"<th>{d}</th>"
        html += "</tr></thead><tbody>"
        for merc in estrutura:
            mx = max(len(estrutura[merc].get(d,[])) for d in dias_present)
            html += "<tr>"
            for d in dias_present:
                html += f'<td class="mn">🏪 {merc}</td>' if estrutura[merc].get(d) else '<td class="vz"></td>'
            html += "</tr>"
            for i in range(mx):
                html += "<tr>"
                for d in dias_present:
                    pp = estrutura[merc].get(d,[])
                    html += f'<td class="pi">· {pp[i]}</td>' if i < len(pp) else '<td class="vz"></td>'
                html += "</tr>"
        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        section_title("Detalhes do dia")

        dia_sel   = st.selectbox("Selecione o dia", dias_present)
        dados_dia = tarefas[tarefas["dia"] == dia_sel]

        for merc in dados_dia["mercado"].unique():
            with st.expander(f"🏪  {merc}", expanded=True):
                info = pd.read_sql("SELECT endereco FROM mercados WHERE mercado=?", conn, params=(merc,))
                if not info.empty:
                    end = info.iloc[0]["endereco"]
                    st.markdown(
                        f"<div style='color:#555;font-size:12px;margin-bottom:6px'>📍 {end}</div>",
                        unsafe_allow_html=True)
                    st.markdown(f"[🗺️ Abrir no Google Maps](https://www.google.com/maps/search/{end.replace(' ','+')})")

                prods = dados_dia[dados_dia["mercado"]==merc]
                st.markdown(
                    "<div style='margin:10px 0 6px;color:#444;font-size:10px;"
                    "text-transform:uppercase;letter-spacing:1px'>Produtos</div>",
                    unsafe_allow_html=True)
                for i, r in prods.iterrows():
                    st.checkbox(r["produto"], key=f"ck_{dia_sel}_{i}")

                foto = st.file_uploader("📷 Foto da gôndola",
                                        key=f"f_{merc}_{dia_sel}", type=["jpg","jpeg","png"])
                caminho = ""
                if foto:
                    pasta = f"fotos/{usuario}"
                    os.makedirs(pasta, exist_ok=True)
                    caminho = f"{pasta}/{merc}_{dia_sel}_{date.today()}.jpg".replace(" ","_")
                    with open(caminho,"wb") as f: f.write(foto.getbuffer())
                    st.image(caminho, width=280)

                if st.button("✅ Enviar relatório", key=f"btn_{merc}_{dia_sel}"):
                    pd.DataFrame([{"data":str(date.today()),"funcionario":usuario,
                                   "mercado":merc,"produto":"varios","status":"ok","foto":caminho}])\
                      .to_sql("relatorio", conn, if_exists="append", index=False)
                    st.success(f"Relatório de {merc} enviado!")

    # ── CHAT FUNCIONÁRIO ──

    else:

        page_header("Fale com o Admin", "Chat")

        c.execute("UPDATE chat SET lido=1 WHERE remetente=? AND tipo='admin'", (usuario,))
        conn.commit()

        hist = pd.read_sql(
            "SELECT * FROM chat WHERE (remetente=? AND tipo='funcionario') "
            "OR (remetente=? AND tipo='admin') ORDER BY id",
            conn, params=(usuario, usuario))

        st.markdown("""
        <style>
        .chat-wrap{background:#0d0d0d;border:1px solid #1c1c1c;border-radius:14px;
                   padding:20px;min-height:320px;max-height:440px;overflow-y:auto;margin-bottom:14px}
        .bm-adm{background:#ff2b2b;color:#fff;border-radius:14px 14px 2px 14px;
                padding:9px 14px;margin:5px 0 2px;max-width:66%;float:left;clear:both;font-size:13px;line-height:1.5}
        .bm-fun{background:#1a1a1a;color:#ddd;border-radius:14px 14px 14px 2px;
                padding:9px 14px;margin:5px 0 2px;max-width:66%;float:right;clear:both;font-size:13px;line-height:1.5}
        .bm-hora{font-size:10px;color:#2a2a2a;clear:both;margin-bottom:5px}
        .bm-hr{text-align:right}
        </style>
        """, unsafe_allow_html=True)

        html = '<div class="chat-wrap">'
        if hist.empty:
            html += '<p style="color:#2a2a2a;text-align:center;padding-top:120px">Nenhuma mensagem ainda.</p>'
        else:
            for _, msg in hist.iterrows():
                if msg["tipo"] == "admin":
                    html += f'<div class="bm-adm">🔴 Admin: {msg["mensagem"]}</div>'
                    html += f'<div class="bm-hora">{msg["hora"]}</div>'
                else:
                    html += f'<div class="bm-fun">{msg["mensagem"]}</div>'
                    html += f'<div class="bm-hora bm-hr">{msg["hora"]}</div>'
        html += '<div style="clear:both"></div></div>'
        st.markdown(html, unsafe_allow_html=True)

        ci, cb = st.columns([6, 1])
        with ci:
            msg_f = st.text_input("msg_f", label_visibility="collapsed",
                                  placeholder="Digite uma mensagem...", key="chat_func")
        with cb:
            if st.button("Enviar", key="send_func"):
                if msg_f.strip():
                    now = datetime.now()
                    c.execute("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                              (str(now.date()), now.strftime("%H:%M"), usuario, "funcionario", msg_f.strip(), 0))
                    conn.commit(); st.rerun()
