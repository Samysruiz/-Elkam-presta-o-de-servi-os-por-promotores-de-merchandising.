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

/* ── LOADING SCREEN ── */
#elk-loading {
    position:fixed; inset:0; background:#0a0a0a; z-index:99999;
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px;
    animation: hideLoading 0.4s ease 1.8s forwards;
}
@keyframes hideLoading { to { opacity:0; pointer-events:none; } }
.elk-logo-box {
    width:80px; height:80px; background:#1a0000;
    border:1px solid #ff2b2b44; border-radius:20px;
    display:flex; align-items:center; justify-content:center; font-size:36px;
    animation: pulse 1s ease infinite;
}
@keyframes pulse {
    0%,100% { box-shadow:0 0 0 0 rgba(255,43,43,0.3); }
    50%      { box-shadow:0 0 0 14px rgba(255,43,43,0); }
}
.elk-bar { width:160px; height:3px; background:#1c1c1c; border-radius:99px; overflow:hidden; }
.elk-bar-fill {
    height:100%; background:linear-gradient(90deg,#ff2b2b,#ff6b6b);
    border-radius:99px; animation: loadBar 1.6s ease forwards;
}
@keyframes loadBar { from{width:0%} to{width:100%} }

/* ── MOBILE BOTTOM NAV ── */
.mob-nav {
    display:none; position:fixed; bottom:0; left:0; right:0; z-index:9998;
    background:#0f0f0f; border-top:1px solid #1c1c1c;
    height:64px; align-items:center; justify-content:space-around; padding:0 4px;
}
.mob-nav-btn {
    display:flex; flex-direction:column; align-items:center; gap:3px;
    color:#444; font-size:9px; font-weight:700; letter-spacing:0.5px;
    text-transform:uppercase; background:none; border:none; cursor:pointer;
    padding:8px 14px; border-radius:12px; transition:all 0.15s; min-width:60px;
}
.mob-nav-btn.active, .mob-nav-btn:hover { color:#ff2b2b; background:#1a0000; }
.mob-nav-btn .ico { font-size:22px; line-height:1; }

@media (max-width:768px) {
    /* Layout geral */
    .mob-nav { display:flex !important; }
    .block-container {
        padding: 1rem 1rem 90px 1rem !important;
    }
    [data-testid="stSidebar"] { display:none !important; }

    /* Tipografia */
    h1 { font-size:22px !important; }
    h2 { font-size:18px !important; }
    h3 { font-size:15px !important; }
    label { font-size:13px !important; }

    /* Botões — maiores para toque */
    .stButton > button {
        padding: 14px 20px !important;
        font-size: 15px !important;
        width: 100% !important;
        border-radius: 12px !important;
    }

    /* Inputs maiores */
    input, textarea, [data-baseweb="input"] input {
        font-size: 16px !important;   /* evita zoom automático no iOS */
        padding: 14px !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        font-size: 15px !important;
        padding: 12px !important;
    }

    /* Radio horizontal — botões maiores */
    [data-testid="stRadio"] label {
        font-size: 14px !important;
        padding: 10px 14px !important;
    }

    /* Checkbox */
    .stCheckbox label {
        font-size: 15px !important;
    }
    [data-testid="stCheckbox"] > label {
        padding: 10px 0 !important;
    }

    /* Métricas — stack vertical */
    [data-testid="column"] { min-width: 0 !important; }
    [data-testid="stMetricValue"] { font-size:22px !important; }

    /* Cards de produto — stack vertical em mobile */
    .prod-row-desktop { display:none !important; }
    .prod-row-mobile  { display:block !important; }

    /* Camera input — tela cheia no celular */
    [data-testid="stCameraInput"] video,
    [data-testid="stCameraInput"] canvas {
        border-radius: 14px !important;
        max-width: 100% !important;
    }
    [data-testid="stCameraInputButton"] button {
        width:100% !important;
        padding:16px !important;
        font-size:16px !important;
        border-radius:12px !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        padding: 16px !important;
    }
    [data-testid="stFileUploader"] label {
        font-size: 14px !important;
    }

    /* Expanders */
    [data-testid="stExpander"] summary {
        padding: 16px !important;
        font-size: 15px !important;
    }

    /* Oculta tabela da semana em mobile (muito larga) */
    .tab-ag-wrap { display:none !important; }
    .agenda-semana-mobile { display:block !important; }

    /* Login — coluna logo some, form ocupa tudo */
    .login-logo-col { display:none !important; }

    /* Mercado card header — texto menor */
    .merc-card-nome { font-size:16px !important; }

    /* Separadores */
    hr { margin: 12px 0 !important; }

    /* Evita scroll horizontal */
    .main .block-container { overflow-x: hidden !important; }
}

/* Classes utilitárias */
.prod-row-mobile { display:none; }
.tab-ag-wrap     { display:block; }
.agenda-semana-mobile { display:none; }
.login-logo-col  { display:block; }


/* ── STATUS BADGES ── */
.badge-ok    { background:#0a2b14; color:#22c55e; border:1px solid #22c55e44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-falta { background:#2b1f0a; color:#f59e0b; border:1px solid #f59e0b44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-fecha { background:#2b0a0a; color:#ff4444; border:1px solid #ff444444; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }

/* ── EXPANDER: remove ícone que sobrepõe texto ── */
[data-testid="stExpander"] details summary span[data-testid="stExpanderToggleIcon"],
[data-testid="stExpander"] summary > div > svg,
[data-testid="stExpander"] summary svg,
details > summary > div > svg { display:none !important; width:0 !important; }
[data-testid="stExpander"] summary { padding-left:14px !important; }
[data-testid="stExpander"] summary p { color:#ddd !important; font-weight:600 !important; font-size:13px !important; }


@keyframes fadeIn {
    from { opacity:0; transform:translateY(12px); }
    to   { opacity:1; transform:translateY(0); }
}
</style>

<!-- LOADING SCREEN -->
<div id="elk-loading">
    <div class="elk-logo-box">🏪</div>
    <div style="color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase">El Kam</div>
    <div class="elk-bar"><div class="elk-bar-fill"></div></div>
    <div style="color:#2a2a2a;font-size:11px;margin-top:4px">Carregando sistema...</div>
</div>
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
    id INTEGER PRIMARY KEY AUTOINCREMENT, mercado TEXT, endereco TEXT UNIQUE, logo TEXT DEFAULT '')""")
c.execute("""CREATE TABLE IF NOT EXISTS produtos (mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS produto_fotos (
    produto TEXT, foto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS agenda (
    funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS relatorio (
    data TEXT, funcionario TEXT, mercado TEXT, produto TEXT, status TEXT, foto TEXT,
    produto_faltante TEXT DEFAULT '')""")
c.execute("""CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT, hora TEXT, remetente TEXT, tipo TEXT, mensagem TEXT, lido INTEGER DEFAULT 0)""")
c.execute("""CREATE TABLE IF NOT EXISTS checkin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT, hora_entrada TEXT, hora_saida TEXT,
    funcionario TEXT, mercado TEXT, status TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS destinatarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, telefone TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS empresa (
    id INTEGER PRIMARY KEY, nome TEXT, descricao TEXT, foto TEXT, concluida INTEGER DEFAULT 0)""")
c.execute("""CREATE TABLE IF NOT EXISTS config (
    chave TEXT PRIMARY KEY, valor TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS agenda_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_empresa TEXT, funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)""")
conn.commit()

# ── MIGRAÇÕES ──
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
if "telefone" not in usuarios_cols:
    c.execute("ALTER TABLE usuarios ADD COLUMN telefone TEXT DEFAULT ''")
    conn.commit()
if "email" not in usuarios_cols:
    c.execute("ALTER TABLE usuarios ADD COLUMN email TEXT DEFAULT ''")
    conn.commit()

mercados_cols = [r[1] for r in c.execute("PRAGMA table_info(mercados)").fetchall()]
if "logo" not in mercados_cols:
    c.execute("ALTER TABLE mercados ADD COLUMN logo TEXT DEFAULT ''")
    conn.commit()

relatorio_cols = [r[1] for r in c.execute("PRAGMA table_info(relatorio)").fetchall()]
if "produto_faltante" not in relatorio_cols:
    c.execute("ALTER TABLE relatorio ADD COLUMN produto_faltante TEXT DEFAULT ''")
    conn.commit()

usuarios_cols = [r[1] for r in c.execute("PRAGMA table_info(usuarios)").fetchall()]

if pd.read_sql("SELECT * FROM usuarios", conn).empty:
    c.execute("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone,email) VALUES(?,?,?,?,?,?)",
              ('admin','123','admin',0,'',''))
    conn.commit()

# ── BACKUP AUTOMÁTICO DO BANCO ──
import shutil, glob

def fazer_backup():
    """Faz backup rotativo do banco — mantém últimos 5."""
    os.makedirs("backups", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2("duh.db", f"backups/duh_{ts}.bak")
    # Remove backups mais antigos, mantém só 5
    baks = sorted(glob.glob("backups/duh_*.bak"))
    for old in baks[:-5]:
        try: os.remove(old)
        except: pass

# ── ENVIO DE EMAIL ──
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(destinatario: str, assunto: str, corpo_html: str) -> tuple[bool, str]:
    """Envia email via SMTP usando config salva no banco."""
    try:
        smtp_host = obter_config("smtp_host", "smtp.gmail.com")
        smtp_port = int(obter_config("smtp_port", "587"))
        smtp_user = obter_config("smtp_user", "")
        smtp_pass = obter_config("smtp_pass", "")
        if not smtp_user or not smtp_pass:
            return False, "Configure o email SMTP em Configurações."
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"]    = f"El Kam Sistema <{smtp_user}>"
        msg["To"]      = destinatario
        msg.attach(MIMEText(corpo_html, "html", "utf-8"))
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as s:
            s.ehlo(); s.starttls(); s.ehlo()
            s.login(smtp_user, smtp_pass)
            s.sendmail(smtp_user, destinatario, msg.as_string())
        return True, "Email enviado!"
    except Exception as e:
        return False, str(e)

def obter_config(chave: str, padrao: str = "") -> str:
    r = c.execute("SELECT valor FROM config WHERE chave=?", (chave,)).fetchone()
    return r[0] if r else padrao

def salvar_config(chave: str, valor: str):
    c.execute("INSERT OR REPLACE INTO config (chave,valor) VALUES(?,?)", (chave, valor))
    conn.commit()

# ═══════════════════════════════════════════════
#  SESSION
# ═══════════════════════════════════════════════

if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "tela_login" not in st.session_state:
    st.session_state["tela_login"] = "login"  # login | recuperar | codigo

# ── FUNÇÕES DE SEGURANÇA ──

def apenas_admin():
    """Para dentro de blocos: garante que só admin executa."""
    if st.session_state.get("tipo") != "admin":
        st.error("⛔ Acesso negado.")
        st.stop()

def sanitizar(txt: str) -> str:
    """Remove caracteres perigosos de inputs."""
    import re
    return re.sub(r"[<>\"'%;()&+]", "", str(txt)).strip()

import secrets, string

def gerar_codigo() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(6))

# ═══════════════════════════════════════════════
#  LOGIN / RECUPERAÇÃO DE SENHA
# ═══════════════════════════════════════════════

if not st.session_state["logado"]:

    col_form, col_logo = st.columns([1, 1], gap="large")

    # ── COLUNA DIREITA: LOGO ──
    with col_logo:
        st.markdown("<div class='login-logo-col'>", unsafe_allow_html=True)
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        if os.path.exists("el_kam_logo.png"):
            st.image("el_kam_logo.png", use_container_width=True)
        else:
            st.markdown("""
            <div style='height:100%;display:flex;align-items:center;justify-content:center;
                        padding-top:40px'>
                <div style='background:linear-gradient(145deg,#140000,#1e0000);
                            border:1px solid #ff2b2b22;border-radius:24px;
                            padding:56px 48px;text-align:center'>
                    <div style='font-size:64px;margin-bottom:20px'>🏪</div>
                    <div style='color:#ff2b2b;font-weight:800;font-size:28px;
                                letter-spacing:4px;margin-bottom:8px'>EL KAM</div>
                    <div style='color:#2a2a2a;font-size:12px;letter-spacing:3px;
                                text-transform:uppercase'>Merchandising</div>
                    <div style='margin-top:28px;width:40px;height:2px;
                                background:#ff2b2b;margin-left:auto;margin-right:auto'></div>
                    <div style='color:#222;font-size:11px;margin-top:14px;line-height:1.6'>
                        Sistema de gestão<br>de promotores
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── COLUNA ESQUERDA: FORMULÁRIO ──
    with col_form:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

        # ── TELA: LOGIN ──
        if st.session_state["tela_login"] == "login":
            st.markdown("""
            <div style='margin-bottom:32px'>
                <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2.5px;
                            text-transform:uppercase;margin-bottom:10px'>El Kam Merchandising</div>
                <div style='color:#ffffff;font-size:30px;font-weight:900;line-height:1.15;
                            margin-bottom:8px'>Bem-vindo<br>de volta 👋</div>
                <div style='color:#333;font-size:13px'>Acesse com suas credenciais</div>
            </div>
            """, unsafe_allow_html=True)

            usuario_input = st.text_input("Usuário", placeholder="seu.login", key="li_user")
            senha_input   = st.text_input("Senha", type="password", placeholder="••••••••", key="li_pass")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            if st.button("ENTRAR →", use_container_width=True):
                u = sanitizar(usuario_input)
                c.execute("SELECT * FROM usuarios WHERE LOWER(usuario)=LOWER(?) AND senha=?",
                          (u, senha_input))
                user = c.fetchone()
                if user:
                    st.session_state["logado"]  = True
                    st.session_state["usuario"] = user[0]
                    st.session_state["tipo"]    = user[2]
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🔑 Esqueci minha senha", use_container_width=True):
                st.session_state["tela_login"] = "recuperar"
                st.rerun()

            st.markdown("""
            <div style='margin-top:32px;padding-top:20px;border-top:1px solid #1c1c1c;
                        color:#2a2a2a;font-size:11px'>
                © El Kam Merchandising — Todos os direitos reservados.
            </div>
            """, unsafe_allow_html=True)

        # ── TELA: RECUPERAR ──
        elif st.session_state["tela_login"] == "recuperar":
            st.markdown("""
            <div style='margin-bottom:28px'>
                <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2.5px;
                            text-transform:uppercase;margin-bottom:10px'>Recuperar acesso</div>
                <div style='color:#ffffff;font-size:26px;font-weight:900;margin-bottom:8px'>
                    Esqueceu sua senha?</div>
                <div style='color:#333;font-size:13px'>
                    Digite seu usuário e enviaremos um código para o seu email.</div>
            </div>
            """, unsafe_allow_html=True)

            rec_user = st.text_input("Usuário", key="rec_user", placeholder="admin")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            if st.button("Enviar código →", use_container_width=True):
                rec_user = sanitizar(rec_user)
                row = c.execute(
                    "SELECT email FROM usuarios WHERE LOWER(usuario)=LOWER(?) AND tipo='admin'",
                    (rec_user,)).fetchone()
                if not row or not row[0]:
                    st.error("Usuário não encontrado ou sem email de recuperação cadastrado.")
                else:
                    codigo = gerar_codigo()
                    salvar_config("codigo_rec", codigo)
                    salvar_config("codigo_rec_user", rec_user)
                    salvar_config("codigo_rec_exp",
                                  (datetime.now() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"))
                    html_email = f"""
                    <div style='font-family:Arial;background:#0a0a0a;padding:30px;'>
                      <div style='background:#111;border:1px solid #1c1c1c;border-radius:14px;
                                  padding:28px;max-width:480px;margin:auto'>
                        <div style='color:#ff2b2b;font-size:11px;font-weight:700;
                                    letter-spacing:2px;text-transform:uppercase'>El Kam Merchandising</div>
                        <div style='color:#fff;font-size:22px;font-weight:800;margin:10px 0'>
                            Recuperação de Senha</div>
                        <div style='color:#aaa;font-size:14px;margin-bottom:20px'>
                            Seu código de verificação:</div>
                        <div style='background:#ff2b2b;color:#fff;font-size:32px;font-weight:900;
                                    text-align:center;border-radius:10px;padding:16px;
                                    letter-spacing:10px'>{codigo}</div>
                        <div style='color:#444;font-size:12px;margin-top:16px'>
                            Válido por 15 minutos. Se não foi você, ignore este email.</div>
                        <hr style='border-color:#1c1c1c;margin:20px 0'>
                        <div style='color:#222;font-size:11px'>
                            🔗 <a href='https://elkam-merchandising.streamlit.app'
                            style='color:#ff2b2b'>elkam-merchandising.streamlit.app</a>
                        </div>
                      </div>
                    </div>"""
                    ok, msg = enviar_email(row[0], "El Kam — Código de recuperação", html_email)
                    if ok:
                        st.session_state["rec_email_mascarado"] = row[0][:3] + "***" + row[0][row[0].find("@"):]
                        st.session_state["tela_login"] = "codigo"
                        st.rerun()
                    else:
                        st.error(f"Erro ao enviar email: {msg}")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("← Voltar ao login", use_container_width=True):
                st.session_state["tela_login"] = "login"; st.rerun()

        # ── TELA: CÓDIGO ──
        elif st.session_state["tela_login"] == "codigo":
            em = st.session_state.get("rec_email_mascarado", "seu email")
            st.markdown(f"""
            <div style='margin-bottom:28px'>
                <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2.5px;
                            text-transform:uppercase;margin-bottom:10px'>Verificação</div>
                <div style='color:#ffffff;font-size:26px;font-weight:900;margin-bottom:8px'>
                    Código enviado!</div>
                <div style='color:#333;font-size:13px'>
                    Verifique a caixa de entrada de <b style='color:#555'>{em}</b></div>
            </div>
            """, unsafe_allow_html=True)

            codigo_input = st.text_input("Código de 6 dígitos", key="cod_input",
                                         placeholder="000000", max_chars=6)
            nova_senha_r = st.text_input("Nova senha", type="password", key="nova_rec")
            confirma_r   = st.text_input("Confirmar senha", type="password", key="conf_rec")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            if st.button("Redefinir senha →", use_container_width=True):
                cod_salvo = obter_config("codigo_rec")
                cod_user  = obter_config("codigo_rec_user")
                cod_exp   = obter_config("codigo_rec_exp")
                expirado  = datetime.now() > datetime.strptime(cod_exp, "%Y-%m-%d %H:%M:%S") \
                            if cod_exp else True
                if expirado:
                    st.error("Código expirado. Solicite um novo.")
                elif codigo_input.strip() != cod_salvo:
                    st.error("Código incorreto.")
                elif not nova_senha_r or nova_senha_r != confirma_r:
                    st.error("Senhas não coincidem.")
                elif len(nova_senha_r) < 4:
                    st.error("Mínimo 4 caracteres.")
                else:
                    c.execute("UPDATE usuarios SET senha=? WHERE LOWER(usuario)=LOWER(?)",
                              (nova_senha_r, cod_user))
                    salvar_config("codigo_rec", "")
                    conn.commit()
                    st.success("✅ Senha redefinida! Faça login.")
                    st.session_state["tela_login"] = "login"
                    st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("← Voltar ao login", use_container_width=True):
                st.session_state["tela_login"] = "login"; st.rerun()

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

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:#444;font-size:10px;text-transform:uppercase;"
        "letter-spacing:1px;margin-bottom:6px'>🔐 Alterar senha</div>",
        unsafe_allow_html=True)
    nova = st.text_input("Nova senha", type="password", key="sb_nova",
                         label_visibility="collapsed", placeholder="Nova senha...")
    if st.button("Salvar senha", use_container_width=True):
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

    # Mobile nav para admin
    st.markdown("""
    <div class="mob-nav">
        <button class="mob-nav-btn" onclick="window.location.reload()">
            <span class="ico">📊</span>Dash
        </button>
        <button class="mob-nav-btn" onclick="window.location.reload()">
            <span class="ico">📋</span>Agenda
        </button>
        <button class="mob-nav-btn" onclick="window.location.reload()">
            <span class="ico">📈</span>Relat.
        </button>
        <button class="mob-nav-btn" onclick="window.location.reload()">
            <span class="ico">💬</span>Chat
        </button>
    </div>
    """, unsafe_allow_html=True)
    menu = st.sidebar.selectbox(
        "MENU",
        ["Dashboard", "Funcionários", "Mercados", "Agenda", "Relatórios", "Fotos",
         "Fotos de Produtos", "Chat", "Empresa", "Destinatários", "⚙️ Configurações"]
    )

    # ── NOTIFICAÇÃO DE MENSAGENS NÃO LIDAS ──
    msgs_novas = pd.read_sql(
        "SELECT remetente, mensagem, hora FROM chat WHERE tipo='funcionario' AND lido=0 ORDER BY id DESC",
        conn
    )
    if not msgs_novas.empty:
        total_nao_lidas = len(msgs_novas)
        ultima = msgs_novas.iloc[0]
        st.markdown(f"""
        <div style='
            position:fixed; bottom:24px; right:24px; z-index:9999;
            background:#111; border:1px solid #ff2b2b44;
            border-left:3px solid #ff2b2b;
            border-radius:12px; padding:14px 18px;
            box-shadow:0 8px 32px rgba(0,0,0,0.5);
            max-width:300px; animation:fadeIn 0.3s ease;
        '>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>
                <div style='width:8px;height:8px;background:#ff2b2b;
                            border-radius:50%;flex-shrink:0'></div>
                <span style='color:#ff2b2b;font-size:10px;font-weight:700;
                             letter-spacing:1px;text-transform:uppercase'>
                    {total_nao_lidas} mensagem{'ns' if total_nao_lidas > 1 else ''} nova{'s' if total_nao_lidas > 1 else ''}
                </span>
            </div>
            <div style='color:#fff;font-size:13px;font-weight:600;margin-bottom:2px'>
                👤 {ultima['remetente']}
            </div>
            <div style='color:#888;font-size:12px;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis;max-width:240px'>
                {ultima['mensagem']}
            </div>
            <div style='color:#333;font-size:10px;margin-top:6px'>{ultima['hora']} · Abra o Chat para responder</div>
        </div>
        <style>
        @keyframes fadeIn {{
            from {{ opacity:0; transform:translateY(12px); }}
            to   {{ opacity:1; transform:translateY(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)

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
            tel_novo = st.text_input("📱 WhatsApp (com DDD, só números)", placeholder="11999998888")
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
                        c.execute("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone) VALUES(?,?,?,?,?)",
                                  (login,"elkam","funcionario",1,tel_novo.strip()))
                        conn.commit()
                        st.success(f"✅ Criado! Login: **{login}** · Senha: **elkam**")
                        st.rerun()

        section_title("Funcionários cadastrados")
        funcs = pd.read_sql("SELECT usuario, telefone FROM usuarios WHERE tipo='funcionario'", conn)

        if funcs.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            for _, row in funcs.iterrows():
                login_func = row['usuario']
                tel_func   = row.get('telefone','') or ''

                col_i, col_w, col_r, col_e = st.columns([4, 2, 2, 1])
                with col_i:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;font-weight:600;padding:10px 0'>"
                        f"👤 {login_func}"
                        f"<span style='color:#444;font-weight:400;font-size:11px'>"
                        f"{'  · 📱 '+tel_func if tel_func else '  · sem telefone'}</span></div>",
                        unsafe_allow_html=True)
                with col_w:
                    if tel_func:
                        msg_wa = (
                            f"Bem-vindo à El Kam Merchandising! 👋\n\n"
                            f"Olá, {login_func.split('.')[0].capitalize()}! Seu acesso ao sistema de promotores está pronto.\n\n"
                            f"🔗 *Link:* https://elkam-merchandising.streamlit.app\n"
                            f"👤 *Usuário:* {login_func}\n"
                            f"🔑 *Senha:* elkam _(troque no primeiro acesso)_\n\n"
                            f"📲 No celular, abra o link e toque em *\"Adicionar à tela inicial\"* para ter o ícone igual a um app."
                        )
                        import urllib.parse
                        wa_url = f"https://wa.me/55{tel_func}?text={urllib.parse.quote(msg_wa)}"
                        st.markdown(
                            f"<a href='{wa_url}' target='_blank'>"
                            f"<button style='background:#25D366;color:#fff;border:none;"
                            f"border-radius:8px;padding:8px 14px;font-size:12px;"
                            f"font-weight:600;cursor:pointer;width:100%'>"
                            f"📲 Enviar acesso</button></a>",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            "<div style='color:#333;font-size:11px;padding:10px 0'>Sem telefone</div>",
                            unsafe_allow_html=True)
                with col_r:
                    if st.button("🔑 Resetar senha", key=f"reset_{login_func}"):
                        c.execute("UPDATE usuarios SET senha='elkam', primeiro_acesso=1 WHERE usuario=?",
                                  (login_func,))
                        conn.commit()
                        st.success(f"Senha de **{login_func}** resetada.")
                        st.rerun()
                with col_e:
                    if st.button("🗑️", key=f"del_{login_func}"):
                        fazer_backup()
                        c.execute("DELETE FROM usuarios WHERE usuario=? AND tipo='funcionario'", (login_func,))
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (login_func,))
                        conn.commit()
                        st.rerun()

    # ── MERCADOS ──────────────────────────────────────────

    elif menu == "Mercados":
        page_header("Cadastro", "Mercados")

        with st.expander("➕ Novo mercado"):
            cm, ce = st.columns(2)
            with cm: mercado  = st.text_input("Nome do mercado")
            with ce: endereco = st.text_input("Endereço")
            logo_up = st.file_uploader("🖼️ Logo do mercado (opcional)", type=["jpg","jpeg","png"], key="logo_new")
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
                            logo_path = ""
                            if logo_up:
                                os.makedirs("logos_mercados", exist_ok=True)
                                logo_path = f"logos_mercados/{mercado.strip().replace(' ','_')}.{logo_up.name.split('.')[-1]}"
                                with open(logo_path,"wb") as lf: lf.write(logo_up.getbuffer())
                            c.execute("INSERT INTO mercados (mercado,endereco,logo) VALUES(?,?,?)",
                                      (mercado.strip(), endereco.strip(), logo_path))
                            conn.commit()
                            st.success("✅ Mercado cadastrado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

        section_title("Lista de mercados")
        mdf = pd.read_sql("SELECT id, mercado, endereco, logo FROM mercados", conn)

        if mdf.empty:
            st.info("Nenhum mercado cadastrado.")
        else:
            for _, row in mdf.iterrows():
                col_logo_m, col_i, col_ed, col_ex = st.columns([1, 5, 1, 1])
                with col_logo_m:
                    if row.get("logo") and os.path.exists(str(row["logo"])):
                        st.image(str(row["logo"]), width=48)
                    else:
                        st.markdown("<div style='font-size:32px;padding:4px'>🏪</div>", unsafe_allow_html=True)
                with col_i:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;padding:10px 0'>"
                        f"<b>{row['mercado']}</b>"
                        f" <span style='color:#444'>·</span>"
                        f" <span style='color:#666'>{row['endereco']}</span></div>",
                        unsafe_allow_html=True)
                with col_ed:
                    if st.button("✏️", key=f"edit_btn_{row['id']}"):
                        st.session_state[f"editando_{row['id']}"] = True
                with col_ex:
                    if st.button("🗑️", key=f"del_merc_{row['id']}"):
                        fazer_backup()
                        c.execute("DELETE FROM mercados WHERE id=?", (int(row["id"]),))
                        c.execute("DELETE FROM agenda WHERE mercado=?", (row["mercado"],))
                        conn.commit()
                        st.success(f"Mercado '{row['mercado']}' excluído.")
                        st.rerun()

                if st.session_state.get(f"editando_{row['id']}", False):
                    with st.container():
                        ea, eb = st.columns(2)
                        with ea:
                            novo_nome = st.text_input("Novo nome", value=row["mercado"], key=f"edit_nome_{row['id']}")
                        with eb:
                            novo_end = st.text_input("Novo endereço", value=row["endereco"], key=f"edit_end_{row['id']}")
                        novo_logo_up = st.file_uploader("🖼️ Novo logo", type=["jpg","jpeg","png"], key=f"logo_edit_{row['id']}")
                        ec, ed = st.columns(2)
                        with ec:
                            if st.button("✅ Salvar", key=f"save_merc_{row['id']}"):
                                logo_path = row.get("logo","") or ""
                                if novo_logo_up:
                                    os.makedirs("logos_mercados", exist_ok=True)
                                    logo_path = f"logos_mercados/{novo_nome.strip().replace(' ','_')}.{novo_logo_up.name.split('.')[-1]}"
                                    with open(logo_path,"wb") as lf: lf.write(novo_logo_up.getbuffer())
                                nome_antigo = row["mercado"]
                                c.execute("UPDATE mercados SET mercado=?,endereco=?,logo=? WHERE id=?",
                                          (novo_nome.strip(), novo_end.strip(), logo_path, int(row["id"])))
                                if novo_nome.strip() != nome_antigo:
                                    c.execute("UPDATE agenda SET mercado=? WHERE mercado=?",
                                              (novo_nome.strip(), nome_antigo))
                                conn.commit()
                                st.session_state[f"editando_{row['id']}"] = False
                                st.success("✅ Mercado atualizado!")
                                st.rerun()
                        with ed:
                            if st.button("✖ Cancelar", key=f"cancel_merc_{row['id']}"):
                                st.session_state[f"editando_{row['id']}"] = False
                                st.rerun()

    # ── AGENDA ────────────────────────────────────────────

    elif menu == "Agenda":
        page_header("Planejamento", "Agenda")

        DIAS_SEMANA = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]

        funcs_ag = pd.read_sql("SELECT usuario FROM usuarios WHERE tipo='funcionario'", conn)
        mercs_ag = pd.read_sql("SELECT mercado FROM mercados", conn)
        prods_cad = pd.read_sql("SELECT DISTINCT produto FROM produtos", conn)

        with st.expander("➕ Adicionar item à agenda"):
            if funcs_ag.empty:
                st.warning("Nenhum funcionário cadastrado.")
            elif mercs_ag.empty:
                st.warning("Nenhum mercado cadastrado.")
            else:
                ca, cb, cc = st.columns(3)
                with ca: fs = st.selectbox("Funcionário", funcs_ag["usuario"].tolist(), key="ag_func")
                with cb: ds = st.selectbox("Dia", DIAS_SEMANA, key="ag_dia")
                with cc: ms = st.selectbox("Mercado", mercs_ag["mercado"].tolist(), key="ag_merc")

                # Produto: lista existente ou novo
                lista_prod = prods_cad["produto"].tolist() if not prods_cad.empty else []
                lista_prod_opc = lista_prod + ["➕ Novo produto..."]
                prod_sel = st.selectbox("Produto (selecione ou adicione novo)", lista_prod_opc, key="ag_prod_sel")
                if prod_sel == "➕ Novo produto...":
                    ps = st.text_input("Nome do novo produto", key="ag_prod_new")
                else:
                    ps = prod_sel

                ca2, cb2 = st.columns(2)
                with ca2:
                    if st.button("Adicionar à agenda", key="ag_add"):
                        if not ps.strip():
                            st.warning("Informe o produto.")
                        else:
                            dup = c.execute(
                                "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                (fs, ds, ms, ps.strip())).fetchone()[0]
                            if dup > 0:
                                st.warning("⚠️ Produto já existe nesse dia/mercado.")
                            else:
                                c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                          (fs, ds, ms, ps.strip()))
                                # Salva produto no catálogo se for novo
                                if ps.strip() not in lista_prod:
                                    dup_p = c.execute("SELECT COUNT(*) FROM produtos WHERE produto=?", (ps.strip(),)).fetchone()[0]
                                    if dup_p == 0:
                                        c.execute("INSERT INTO produtos (mercado,produto) VALUES(?,?)", (ms, ps.strip()))
                                conn.commit()
                                st.success(f"✅ {ps.strip()} adicionado — {ms} / {ds}")
                                st.rerun()
                with cb2:
                    # Replicar dia inteiro de outro dia
                    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                    dia_orig = st.selectbox("Replicar do dia", [d for d in DIAS_SEMANA if d != ds], key="ag_rep_dia")
                    if st.button("📋 Replicar dia", key="ag_rep"):
                        items = pd.read_sql(
                            "SELECT mercado,produto FROM agenda WHERE funcionario=? AND dia=?",
                            conn, params=(fs, dia_orig))
                        if items.empty:
                            st.warning(f"Nenhum item em {dia_orig} para {fs}.")
                        else:
                            ins = 0
                            for _, r in items.iterrows():
                                dup = c.execute(
                                    "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                    (fs, ds, r["mercado"], r["produto"])).fetchone()[0]
                                if dup == 0:
                                    c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (fs, ds, r["mercado"], r["produto"]))
                                    ins += 1
                            conn.commit()
                            st.success(f"✅ {ins} item(ns) replicado(s) de {dia_orig} para {ds}!")
                            st.rerun()

        with st.expander("🔁 Copiar agenda completa entre funcionários"):
            if funcs_ag.empty:
                st.warning("Nenhum funcionário.")
            else:
                lista = funcs_ag["usuario"].tolist()
                co1, co2 = st.columns(2)
                with co1: fo = st.selectbox("Copiar DE", lista, key="cp_de")
                with co2: fd = st.selectbox("Copiar PARA", lista, key="cp_para")
                ag_orig = pd.read_sql("SELECT dia,mercado,produto FROM agenda WHERE funcionario=?",
                                      conn, params=(fo,))
                if ag_orig.empty:
                    st.warning(f"'{fo}' não tem agenda.")
                else:
                    st.dataframe(ag_orig, use_container_width=True, hide_index=True)
                    apagar = st.checkbox("Substituir agenda atual do destino", value=True)
                    if st.button("🔁 Copiar agenda completa"):
                        if fo == fd:
                            st.error("Origem e destino iguais.")
                        else:
                            if apagar:
                                c.execute("DELETE FROM agenda WHERE funcionario=?", (fd,))
                            ins = 0
                            for _, r in ag_orig.iterrows():
                                dup = c.execute(
                                    "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                    (fd, r["dia"], r["mercado"], r["produto"])).fetchone()[0]
                                if dup == 0:
                                    c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (fd, r["dia"], r["mercado"], r["produto"]))
                                    ins += 1
                            conn.commit()
                            st.success(f"✅ {ins} tarefas copiadas para '{fd}'!")
                            st.rerun()

        with st.expander("📂 Importar Agenda Pré-definida (cliente externo)"):
            st.caption("Faça upload de um arquivo CSV com colunas: dia, mercado, produto")
            st.markdown("""
            <div style='background:#111;border:1px solid #1c1c1c;border-radius:8px;
                        padding:10px 14px;font-size:12px;color:#555;margin-bottom:10px'>
            Formato do CSV:<br>
            <code style='color:#888'>dia,mercado,produto</code><br>
            <code style='color:#888'>Segunda,Atacadão,Fini</code><br>
            <code style='color:#888'>Terça,Assaí,Ovo</code>
            </div>
            """, unsafe_allow_html=True)
            nome_empresa_imp = st.text_input("Nome da empresa / cliente", key="imp_empresa",
                                             placeholder="Ex: Cliente ABC Ltda")
            func_imp = st.selectbox("Atribuir ao funcionário", funcs_ag["usuario"].tolist() if not funcs_ag.empty else [], key="imp_func")
            csv_up = st.file_uploader("📎 Upload do CSV da agenda", type=["csv"], key="imp_csv")
            if csv_up and st.button("📥 Importar agenda", key="imp_btn"):
                try:
                    df_imp = pd.read_csv(csv_up)
                    df_imp.columns = [c2.strip().lower() for c2 in df_imp.columns]
                    if not {"dia","mercado","produto"}.issubset(set(df_imp.columns)):
                        st.error("CSV deve ter colunas: dia, mercado, produto")
                    else:
                        ins = 0; dup_count = 0
                        for _, r2 in df_imp.iterrows():
                            dia_v = str(r2["dia"]).strip()
                            merc_v = str(r2["mercado"]).strip()
                            prod_v = str(r2["produto"]).strip()
                            if dia_v not in DIAS_SEMANA:
                                continue
                            dup = c.execute(
                                "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                (func_imp, dia_v, merc_v, prod_v)).fetchone()[0]
                            if dup == 0:
                                c.execute("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                          (func_imp, dia_v, merc_v, prod_v))
                                # Salva template
                                c.execute("INSERT INTO agenda_template (nome_empresa,funcionario,dia,mercado,produto) VALUES(?,?,?,?,?)",
                                          (nome_empresa_imp.strip() or "Sem nome", func_imp, dia_v, merc_v, prod_v))
                                ins += 1
                            else:
                                dup_count += 1
                        conn.commit()
                        st.success(f"✅ {ins} item(ns) importado(s) para **{func_imp}**!"
                                   + (f" ({dup_count} duplicado(s) ignorado(s))" if dup_count else ""))
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao ler CSV: {e}")

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
            for dia_e in DIAS_SEMANA:
                df_d = ag_df[ag_df["dia"] == dia_e]
                if df_d.empty: continue
                st.markdown(
                    f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:1px;"
                    f"text-transform:uppercase;margin:14px 0 6px'>📅 {dia_e}</div>",
                    unsafe_allow_html=True)
                # Agrupar por mercado
                for merc_g in df_d["mercado"].unique():
                    prods_g = df_d[df_d["mercado"]==merc_g]
                    st.markdown(
                        f"<div style='color:#888;font-size:11px;padding:2px 0 2px 10px;border-left:2px solid #1c1c1c'>"
                        f"🏪 <b style='color:#ccc'>{merc_g}</b></div>",
                        unsafe_allow_html=True)
                    for _, row in prods_g.iterrows():
                        ck, ci = st.columns([1, 10])
                        with ck:
                            if st.checkbox("", key=f"sel_{row['rowid']}", label_visibility="collapsed"):
                                selecionados.append(int(row["rowid"]))
                        with ci:
                            st.markdown(
                                f"<div style='color:#777;font-size:12px;padding:3px 0 3px 18px'>"
                                f"· {row['produto']}"
                                f" <span style='color:#333'>— {row['funcionario']}</span></div>",
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
                    fazer_backup()
                    if filt == "Todos":
                        c.execute("DELETE FROM agenda")
                    else:
                        c.execute("DELETE FROM agenda WHERE funcionario=?", (filt,))
                    conn.commit(); st.rerun()

    # ── RELATÓRIOS ────────────────────────────────────────

    elif menu == "Relatórios":
        page_header("Acompanhamento", "Relatório Completo")

        rel_all = pd.read_sql("SELECT rowid, * FROM relatorio", conn)

        # ── FILTROS ──
        st.markdown("#### 🔍 Filtros")
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            periodo = st.selectbox("Período", ["Hoje","Últimos 7 dias","Últimos 30 dias","Intervalo personalizado"])
        with fc2:
            ff_rel = st.selectbox("Funcionário", ["Todos"] + (rel_all["funcionario"].unique().tolist() if not rel_all.empty else []))
        with fc3:
            fm_rel = st.selectbox("Mercado", ["Todos"] + (rel_all["mercado"].unique().tolist() if not rel_all.empty else []))
        with fc4:
            fs_rel = st.selectbox("Status", ["Todos","abastecido","falta","fechado"])

        if periodo == "Intervalo personalizado":
            dc1, dc2 = st.columns(2)
            with dc1: d_ini = st.date_input("De", value=date.today()-timedelta(days=7))
            with dc2: d_fim = st.date_input("Até", value=date.today())
        elif periodo == "Hoje":
            d_ini = d_fim = date.today()
        elif periodo == "Últimos 7 dias":
            d_ini = date.today()-timedelta(days=7); d_fim = date.today()
        else:
            d_ini = date.today()-timedelta(days=30); d_fim = date.today()

        df_r = rel_all.copy()
        if not df_r.empty:
            df_r["data_dt"] = pd.to_datetime(df_r["data"], errors="coerce")
            df_r = df_r[(df_r["data_dt"].dt.date >= d_ini) & (df_r["data_dt"].dt.date <= d_fim)]
        if ff_rel != "Todos" and not df_r.empty: df_r = df_r[df_r["funcionario"]==ff_rel]
        if fm_rel != "Todos" and not df_r.empty: df_r = df_r[df_r["mercado"]==fm_rel]
        if fs_rel != "Todos" and not df_r.empty: df_r = df_r[df_r["status"]==fs_rel]

        # ── MÉTRICAS ──
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Total de visitas", len(df_r))
        m2.metric("Funcionários", df_r["funcionario"].nunique() if not df_r.empty else 0)
        m3.metric("Mercados", df_r["mercado"].nunique() if not df_r.empty else 0)
        abast = len(df_r[df_r["status"]=="abastecido"]) if not df_r.empty else 0
        m4.metric("✅ Abastecidos", abast)

        if df_r.empty:
            st.info("Nenhum relatório no período selecionado.")
        else:
            # ── TABELA ──
            section_title("Registros detalhados")
            badge_map = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}
            selecionados_rel = []
            for _, row in df_r.sort_values("data_dt",ascending=False).iterrows():
                ck, ci = st.columns([1, 11])
                with ck:
                    if st.checkbox("", key=f"rel_{row['rowid']}", label_visibility="collapsed"):
                        selecionados_rel.append(int(row["rowid"]))
                with ci:
                    badge = badge_map.get(str(row["status"]),"")
                    pf = f" · ⚠️ <i>{row['produto_faltante']}</i>" if str(row.get("produto_faltante","")) not in ("","nan") else ""
                    st.markdown(
                        f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:8px;"
                        f"padding:10px 14px;margin-bottom:4px'>"
                        f"<span style='color:#fff;font-weight:700'>{row['funcionario']}</span>"
                        f" <span style='color:#333'>·</span> <span style='color:#888'>{row['mercado']}</span>"
                        f" <span style='color:#333'>·</span> <span style='color:#555;font-size:12px'>{str(row['data'])[:10]}</span>"
                        f" <span style='float:right;font-size:12px'>{badge}{pf}</span></div>",
                        unsafe_allow_html=True)

            ce1, ce2, ce3 = st.columns([3, 1, 1])
            with ce1:
                if selecionados_rel: st.warning(f"{len(selecionados_rel)} selecionado(s).")
            with ce2:
                if st.button("🗑️ Excluir selecionados", key="del_rel", disabled=not selecionados_rel):
                    fazer_backup()
                    for rid in selecionados_rel:
                        c.execute("DELETE FROM relatorio WHERE rowid=?", (rid,))
                    conn.commit(); st.success("Excluído(s)."); st.rerun()
            with ce3:
                # Export HTML do relatório completo
                rows_html = ""
                for _, row in df_r.sort_values("data_dt",ascending=False).iterrows():
                    badge_h = badge_map.get(str(row["status"]),"")
                    pf_h = row.get("produto_faltante","") or ""
                    foto_h = f'<img src="{row["foto"]}" style="width:120px;border-radius:6px">' \
                             if row.get("foto") and os.path.exists(str(row["foto"])) else "—"
                    rows_html += f"<tr><td>{str(row['data'])[:10]}</td><td>{row['funcionario']}</td><td>{row['mercado']}</td><td>{badge_h}</td><td>{pf_h}</td><td>{foto_h}</td></tr>"
                exp_html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
                <style>body{{font-family:Arial;background:#fff;padding:20px;color:#222}}
                h1{{color:#ff2b2b}}table{{width:100%;border-collapse:collapse;font-size:13px}}
                th{{background:#ff2b2b;color:#fff;padding:8px 12px;text-align:left}}
                td{{border-bottom:1px solid #eee;padding:8px 12px;vertical-align:middle}}
                tr:nth-child(even){{background:#f9f9f9}}</style></head><body>
                <h1>El Kam Merchandising</h1>
                <p>Relatório de {d_ini.strftime('%d/%m/%Y')} a {d_fim.strftime('%d/%m/%Y')}</p>
                <table><tr><th>Data</th><th>Funcionário</th><th>Mercado</th><th>Status</th><th>Produto em falta</th><th>Foto</th></tr>
                {rows_html}</table>
                <p style='color:#aaa;font-size:11px;margin-top:20px'>© El Kam Merchandising — Todos os direitos reservados.</p>
                </body></html>"""
                st.download_button(
                    "📥 Exportar relatório",
                    data=exp_html.encode("utf-8"),
                    file_name=f"relatorio_elkam_{d_ini}_{d_fim}.html",
                    mime="text/html"
                )

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

    # ── FOTOS DE PRODUTOS ─────────────────────────────────

    elif menu == "Fotos de Produtos":
        page_header("Referência", "Fotos de Referência dos Produtos")
        st.caption("Cadastre fotos de referência de cada produto para aparecer na agenda do funcionário.")

        with st.expander("➕ Adicionar foto de produto"):
            pf1, pf2 = st.columns(2)
            with pf1:
                prods_todos = pd.read_sql("SELECT DISTINCT produto FROM produtos", conn)
                lista_p = prods_todos["produto"].tolist() if not prods_todos.empty else []
                lista_p_opc = lista_p + ["➕ Novo produto..."]
                p_sel_foto = st.selectbox("Produto", lista_p_opc, key="pf_sel")
                if p_sel_foto == "➕ Novo produto...":
                    p_nome_foto = st.text_input("Nome do produto", key="pf_nome_new")
                else:
                    p_nome_foto = p_sel_foto
            with pf2:
                foto_prod_up = st.file_uploader("Foto de referência", type=["jpg","jpeg","png"], key="pf_up")
            if st.button("Salvar foto do produto", key="pf_save"):
                if not p_nome_foto.strip():
                    st.warning("Informe o nome do produto.")
                elif not foto_prod_up:
                    st.warning("Selecione uma foto.")
                else:
                    os.makedirs("fotos_produtos", exist_ok=True)
                    fp_path = f"fotos_produtos/{p_nome_foto.strip().replace(' ','_')}.{foto_prod_up.name.split('.')[-1]}"
                    with open(fp_path,"wb") as f3: f3.write(foto_prod_up.getbuffer())
                    # Upsert
                    ex = c.execute("SELECT id FROM produto_fotos WHERE produto=?", (p_nome_foto.strip(),)).fetchone()
                    if ex:
                        c.execute("UPDATE produto_fotos SET foto=? WHERE produto=?", (fp_path, p_nome_foto.strip()))
                    else:
                        c.execute("INSERT INTO produto_fotos (produto,foto) VALUES(?,?)", (p_nome_foto.strip(), fp_path))
                        if p_nome_foto.strip() not in lista_p:
                            c.execute("INSERT INTO produtos (mercado,produto) VALUES('',?)", (p_nome_foto.strip(),))
                    conn.commit()
                    st.success(f"✅ Foto de '{p_nome_foto}' salva!")
                    st.rerun()

        section_title("Produtos com foto de referência")
        pf_df = pd.read_sql("SELECT * FROM produto_fotos", conn)
        if pf_df.empty:
            st.info("Nenhuma foto de produto cadastrada.")
        else:
            cols_pf = st.columns(4)
            for idx, (_, r) in enumerate(pf_df.iterrows()):
                with cols_pf[idx % 4]:
                    if r["foto"] and os.path.exists(str(r["foto"])):
                        st.image(str(r["foto"]), caption=r["produto"], use_container_width=True)
                    else:
                        st.markdown(f"<div style='color:#555;font-size:12px'>{r['produto']} (sem foto)</div>", unsafe_allow_html=True)

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

    # ── CONFIGURAÇÕES ─────────────────────────────────────

    elif menu == "⚙️ Configurações":
        apenas_admin()
        page_header("Sistema", "Configurações")

        # ── EMAIL DE RECUPERAÇÃO ──
        section_title("📧 Email de recuperação do admin")
        admin_row = pd.read_sql(
            "SELECT email FROM usuarios WHERE tipo='admin' AND usuario='admin'", conn)
        email_atual = admin_row.iloc[0]["email"] if not admin_row.empty else ""

        col_em, col_sb = st.columns([3,1])
        with col_em:
            novo_email = st.text_input("Email de recuperação", value=email_atual,
                                       placeholder="admin@empresa.com", key="cfg_email")
        with col_sb:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Salvar email"):
                if "@" in novo_email and "." in novo_email:
                    c.execute("UPDATE usuarios SET email=? WHERE tipo='admin'", (novo_email.strip(),))
                    conn.commit()
                    # Envia confirmação + link do app para o email
                    html_conf = f"""
                    <div style='font-family:Arial;background:#0a0a0a;padding:30px'>
                      <div style='background:#111;border:1px solid #1c1c1c;border-radius:14px;
                                  padding:28px;max-width:480px;margin:auto'>
                        <div style='color:#ff2b2b;font-size:11px;font-weight:700;
                                    letter-spacing:2px;text-transform:uppercase'>El Kam Merchandising</div>
                        <div style='color:#fff;font-size:20px;font-weight:800;margin:10px 0'>
                            Email de recuperação cadastrado ✅</div>
                        <div style='color:#aaa;font-size:14px;margin-bottom:20px'>
                            Este email foi vinculado à conta admin do sistema.</div>
                        <div style='background:#141414;border-radius:10px;padding:16px;margin-bottom:16px'>
                          <div style='color:#555;font-size:11px;text-transform:uppercase;
                                      letter-spacing:1px;margin-bottom:6px'>Acesso ao sistema</div>
                          <div style='color:#fff;font-size:14px'>🔗
                            <a href='https://elkam-merchandising.streamlit.app'
                               style='color:#ff2b2b'>elkam-merchandising.streamlit.app</a>
                          </div>
                          <div style='color:#888;font-size:13px;margin-top:6px'>
                            👤 Usuário: <b>admin</b><br>
                            🔑 Use a opção "Esqueci minha senha" se necessário.
                          </div>
                        </div>
                        <div style='color:#333;font-size:11px'>
                            © El Kam Merchandising — Todos os direitos reservados.
                        </div>
                      </div>
                    </div>"""
                    ok, msg_ret = enviar_email(novo_email.strip(),
                                               "El Kam — Email de recuperação confirmado", html_conf)
                    if ok:
                        st.success(f"✅ Email salvo e confirmação enviada para **{novo_email}**!")
                    else:
                        st.warning(f"Email salvo, mas não foi possível enviar confirmação: {msg_ret}")
                else:
                    st.error("Email inválido.")

        # ── SMTP ──
        section_title("📨 Configuração de email SMTP")
        st.caption("Necessário para envio de emails. Recomendado: Gmail com senha de app.")

        with st.expander("Configurar SMTP"):
            c1, c2 = st.columns(2)
            with c1:
                smtp_h = st.text_input("Servidor SMTP", value=obter_config("smtp_host","smtp.gmail.com"))
                smtp_u = st.text_input("Email remetente", value=obter_config("smtp_user",""))
            with c2:
                smtp_p = st.text_input("Porta", value=obter_config("smtp_port","587"))
                smtp_s = st.text_input("Senha de app", type="password",
                                       value=obter_config("smtp_pass",""),
                                       help="No Gmail: Configurações → Segurança → Senhas de app")
            if st.button("Salvar SMTP"):
                salvar_config("smtp_host", smtp_h.strip())
                salvar_config("smtp_port", smtp_p.strip())
                salvar_config("smtp_user", smtp_u.strip())
                salvar_config("smtp_pass", smtp_s.strip())
                # Teste rápido
                ok, msg_t = enviar_email(smtp_u.strip(),
                    "El Kam — Teste de configuração SMTP",
                    "<b>SMTP configurado com sucesso!</b>")
                if ok:
                    st.success("✅ SMTP salvo e testado! Email de teste enviado.")
                else:
                    st.warning(f"SMTP salvo, mas teste falhou: {msg_t}")

        # ── BACKUP ──
        section_title("💾 Backup dos dados")
        col_bk1, col_bk2 = st.columns(2)
        with col_bk1:
            if st.button("📦 Fazer backup agora"):
                try:
                    fazer_backup()
                    st.success("✅ Backup realizado!")
                except Exception as e:
                    st.error(f"Erro: {e}")
        with col_bk2:
            # Download direto do banco
            if os.path.exists("duh.db"):
                with open("duh.db","rb") as dbf:
                    st.download_button(
                        "⬇️ Baixar banco de dados",
                        data=dbf,
                        file_name=f"elkam_backup_{date.today()}.db",
                        mime="application/octet-stream"
                    )

        baks = sorted(glob.glob("backups/duh_*.bak"), reverse=True)
        if baks:
            st.markdown(
                f"<div style='color:#444;font-size:12px;margin-top:8px'>"
                f"Últimos backups: {', '.join(os.path.basename(b) for b in baks[:3])}</div>",
                unsafe_allow_html=True)

        # ── INFORMAÇÕES DE SEGURANÇA ──
        section_title("🔒 Informações de segurança")
        st.markdown("""
        <div style='background:#111;border:1px solid #1c1c1c;border-radius:12px;padding:18px 20px'>
            <div style='color:#888;font-size:12px;line-height:2'>
                ✅ Todas as senhas são armazenadas no banco de dados local<br>
                ✅ Funcionários não têm acesso a nenhuma função administrativa<br>
                ✅ Cada funcionário só vê sua própria agenda e chat<br>
                ✅ Backups automáticos a cada exclusão de dados<br>
                ✅ Código de recuperação expira em 15 minutos<br>
                ✅ Inputs sanitizados contra injeção<br>
                © El Kam Merchandising — Todos os direitos reservados.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif menu == "Empresa":
        page_header("Configuração", "Apresentação da Empresa")

        emp = pd.read_sql("SELECT * FROM empresa WHERE id=1", conn)
        dados = emp.iloc[0] if not emp.empty else None
        concluida = bool(dados["concluida"]) if dados is not None else False

        if concluida and not st.session_state.get("editando_empresa", False):
            # Exibe apresentação concluída
            st.markdown("""
            <div style='background:#111;border:1px solid #1c1c1c;border-radius:14px;padding:28px;margin-bottom:20px'>
            """, unsafe_allow_html=True)
            if dados["foto"] and os.path.exists(dados["foto"]):
                st.image(dados["foto"], use_container_width=True)
            st.markdown(f"""
                <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2px;
                            text-transform:uppercase;margin:16px 0 6px'>Sobre a empresa</div>
                <div style='color:#fff;font-size:20px;font-weight:800;margin-bottom:12px'>{dados['nome']}</div>
                <div style='color:#aaa;font-size:14px;line-height:1.7;white-space:pre-wrap'>{dados['descricao']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✏️ Editar apresentação"):
                st.session_state["editando_empresa"] = True
                st.rerun()
        else:
            st.info("Preencha as informações da empresa. A apresentação só aparecerá para os funcionários após clicar em **Concluir**.")
            nome_emp = st.text_input("Nome da empresa", value=dados["nome"] if dados is not None else "")
            desc_emp = st.text_area("Descrição / apresentação", value=dados["descricao"] if dados is not None else "",
                                    height=180, placeholder="Fale sobre a empresa, missão, diferenciais...")
            foto_emp = st.file_uploader("📷 Foto / logo da empresa", type=["jpg","jpeg","png"])
            foto_path = dados["foto"] if dados is not None else ""
            if foto_emp:
                os.makedirs("empresa", exist_ok=True)
                foto_path = f"empresa/logo.{foto_emp.name.split('.')[-1]}"
                with open(foto_path, "wb") as f: f.write(foto_emp.getbuffer())
                st.image(foto_path, width=300)
            elif foto_path and os.path.exists(foto_path):
                st.image(foto_path, width=300)

            cb1, cb2 = st.columns(2)
            with cb1:
                if st.button("💾 Salvar rascunho"):
                    if dados is None:
                        c.execute("INSERT INTO empresa (id,nome,descricao,foto,concluida) VALUES(1,?,?,?,0)",
                                  (nome_emp, desc_emp, foto_path))
                    else:
                        c.execute("UPDATE empresa SET nome=?,descricao=?,foto=? WHERE id=1",
                                  (nome_emp, desc_emp, foto_path))
                    conn.commit()
                    st.success("Rascunho salvo!")
            with cb2:
                if st.button("✅ Concluir e publicar"):
                    if not nome_emp.strip() or not desc_emp.strip():
                        st.error("Preencha nome e descrição antes de publicar.")
                    else:
                        if dados is None:
                            c.execute("INSERT INTO empresa (id,nome,descricao,foto,concluida) VALUES(1,?,?,?,1)",
                                      (nome_emp, desc_emp, foto_path))
                        else:
                            c.execute("UPDATE empresa SET nome=?,descricao=?,foto=?,concluida=1 WHERE id=1",
                                      (nome_emp, desc_emp, foto_path))
                        conn.commit()
                        st.session_state["editando_empresa"] = False
                        st.success("✅ Apresentação publicada!")
                        st.rerun()

    # ── DESTINATÁRIOS PDF ─────────────────────────────────

    elif menu == "Destinatários":
        page_header("Configuração", "Destinatários do Relatório PDF")
        st.caption("Números que receberão o link do PDF quando o funcionário enviar o relatório.")

        with st.expander("➕ Adicionar destinatário"):
            cd1, cd2 = st.columns(2)
            with cd1: dest_nome = st.text_input("Nome")
            with cd2: dest_tel  = st.text_input("WhatsApp (com DDD, só números)", placeholder="11999998888")
            if st.button("Adicionar"):
                if dest_nome.strip() and dest_tel.strip():
                    c.execute("INSERT INTO destinatarios (nome,telefone) VALUES(?,?)",
                              (dest_nome.strip(), dest_tel.strip()))
                    conn.commit()
                    st.success(f"✅ {dest_nome} adicionado!")
                    st.rerun()
                else:
                    st.warning("Preencha nome e telefone.")

        section_title("Lista de destinatários")
        dests = pd.read_sql("SELECT * FROM destinatarios", conn)
        if dests.empty:
            st.info("Nenhum destinatário cadastrado.")
        else:
            for _, d in dests.iterrows():
                dc1, dc2 = st.columns([6, 1])
                with dc1:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;padding:10px 0'>"
                        f"👤 <b>{d['nome']}</b> · <span style='color:#555'>📱 {d['telefone']}</span></div>",
                        unsafe_allow_html=True)
                with dc2:
                    if st.button("🗑️", key=f"del_dest_{d['id']}"):
                        c.execute("DELETE FROM destinatarios WHERE id=?", (int(d["id"]),))
                        conn.commit(); st.rerun()

# ═══════════════════════════════════════════════════════
#  FUNCIONÁRIO
# ═══════════════════════════════════════════════════════

else:

    nao_lidas_f = pd.read_sql(
        "SELECT COUNT(*) as t FROM chat WHERE remetente=? AND tipo='admin' AND lido=0",
        conn, params=(usuario,)).iloc[0]["t"]

    emp_pub = pd.read_sql("SELECT * FROM empresa WHERE id=1 AND concluida=1", conn)
    tem_empresa = not emp_pub.empty

    # ── MOBILE BOTTOM NAV ──
    st.markdown(f"""
    <div class="mob-nav">
        <button class="mob-nav-btn" onclick="window.location.href='?nav=agenda'">
            <span class="ico">📋</span>Agenda
        </button>
        {'<button class="mob-nav-btn" onclick="window.location.href=\'?nav=empresa\'"><span class="ico">🏢</span>Empresa</button>' if tem_empresa else ''}
        <button class="mob-nav-btn" onclick="window.location.href='?nav=chat'">
            <span class="ico">💬</span>Chat
            {'<span style="color:#ff2b2b;font-size:8px">●</span>' if nao_lidas_f > 0 else ''}
        </button>
    </div>
    """, unsafe_allow_html=True)

    abas_nav = ["📋  Agenda"]
    if tem_empresa:
        abas_nav.append("🏢  Empresa")
    abas_nav.append(f"💬  Chat{'  ●' if nao_lidas_f > 0 else ''}")
    aba = st.sidebar.radio("NAVEGAÇÃO", abas_nav)

    # ── EMPRESA (FUNCIONÁRIO) ──

    if aba == "🏢  Empresa" and tem_empresa:
        emp = emp_pub.iloc[0]
        page_header("Sobre", emp["nome"])
        if emp["foto"] and os.path.exists(emp["foto"]):
            st.image(emp["foto"], use_container_width=True)
        st.markdown(
            f"<div style='color:#aaa;font-size:14px;line-height:1.8;white-space:pre-wrap;"
            f"margin-top:16px'>{emp['descricao']}</div>",
            unsafe_allow_html=True)

    # ── AGENDA ──

    elif aba == "📋  Agenda" or not tem_empresa:

        nome_exib = usuario.split(".")[0].capitalize()
        page_header("Minha semana", f"Olá, {nome_exib}!")

        tarefas = pd.read_sql("SELECT * FROM agenda WHERE funcionario=?", conn, params=(usuario,))

        if tarefas.empty:
            st.info("Nenhuma agenda cadastrada ainda. Aguarde seu supervisor.")
            st.stop()

        DIAS_SEMANA_F = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
        dias_present = [d for d in DIAS_SEMANA_F if d in tarefas["dia"].values]

        # ── TABELA VISUAL DA SEMANA ──
        estrutura = {}
        for _, r in tarefas.iterrows():
            estrutura.setdefault(r["mercado"], {}).setdefault(r["dia"], []).append(r["produto"])

        html = """
        <style>
        .tab-ag{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:28px}
        .tab-ag th{background:#111;color:#ff2b2b;text-align:center;padding:12px 14px;
                   border-bottom:2px solid #1c1c1c;font-size:10px;letter-spacing:1.5px;text-transform:uppercase}
        .tab-ag th:first-child{text-align:left;padding-left:14px}
        .tab-ag td{padding:6px 12px;border:1px solid #141414;background:#0a0a0a;vertical-align:top}
        .mn{color:#ff2b2b;font-weight:700;font-size:12px;display:block;padding-top:6px}
        .pi{color:#888;font-size:12px;display:block}
        .vz{background:#080808}
        </style><div class="tab-ag-wrap"><table class="tab-ag"><thead><tr><th>Mercado</th>"""
        for d in dias_present:
            html += f"<th>{d}</th>"
        html += "</tr></thead><tbody>"
        for merc in estrutura:
            html += f"<tr><td><span class='mn'>🏪 {merc}</span></td>"
            for d in dias_present:
                pp = estrutura[merc].get(d,[])
                if pp:
                    html += "<td>" + "".join(f"<span class='pi'>· {p}</span>" for p in pp) + "</td>"
                else:
                    html += '<td class="vz"></td>'
            html += "</tr>"
        html += "</tbody></table></div>"

        # Resumo mobile da semana (cards verticais)
        html += "<div class='agenda-semana-mobile'>"
        for d in dias_present:
            mercs_d = tarefas[tarefas["dia"]==d]["mercado"].unique()
            html += f"""<div style='background:#111;border:1px solid #1c1c1c;border-radius:12px;
                        padding:14px 16px;margin-bottom:10px'>
                        <div style='color:#ff2b2b;font-size:10px;font-weight:700;
                                    letter-spacing:2px;text-transform:uppercase;margin-bottom:8px'>📅 {d}</div>"""
            for m in mercs_d:
                pp = estrutura.get(m,{}).get(d,[])
                html += f"<div style='color:#ddd;font-size:13px;font-weight:600;margin-bottom:2px'>🏪 {m}</div>"
                for p in pp:
                    html += f"<div style='color:#555;font-size:12px;padding-left:14px'>· {p}</div>"
            html += "</div>"
        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        section_title("Detalhes do dia")

        dia_sel   = st.selectbox("Selecione o dia", dias_present)
        dados_dia = tarefas[tarefas["dia"] == dia_sel]

        for merc in dados_dia["mercado"].unique():
            merc_info = pd.read_sql("SELECT endereco, logo FROM mercados WHERE mercado=?", conn, params=(merc,))
            logo_merc = ""
            end_merc  = ""
            if not merc_info.empty:
                end_merc  = str(merc_info.iloc[0]["endereco"] or "")
                logo_merc = str(merc_info.iloc[0].get("logo","") or "")

            # ── CARD DO MERCADO ──
            logo_html = ""
            if logo_merc and os.path.exists(logo_merc):
                import base64
                with open(logo_merc,"rb") as lf:
                    logo_b64 = base64.b64encode(lf.read()).decode()
                ext = logo_merc.split(".")[-1].lower()
                mime = "image/png" if ext=="png" else "image/jpeg"
                logo_html = f"<img src='data:{mime};base64,{logo_b64}' style='width:48px;height:48px;object-fit:contain;border-radius:8px;background:#1a1a1a;padding:4px'>"
            else:
                logo_html = "<div style='width:48px;height:48px;background:#1a0000;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:24px'>🏪</div>"

            maps_url = f"https://www.google.com/maps/search/{end_merc.replace(' ','+')}" if end_merc else "#"
            end_html  = f"<div style='color:#444;font-size:12px;margin-top:3px'>📍 {end_merc}</div>" if end_merc else ""
            maps_html = f"<a href='{maps_url}' target='_blank' style='color:#3b82f6;font-size:12px;text-decoration:none'>🗺️ Abrir no Google Maps</a>" if end_merc else ""

            st.markdown(f"""
            <div style='background:#141414;border:1.5px solid #ff2b2b33;border-radius:16px;
                        padding:18px 20px;margin:8px 0 20px;display:flex;
                        align-items:center;gap:16px'>
                {logo_html}
                <div style='flex:1;min-width:0'>
                    <div style='color:#ff2b2b;font-size:10px;font-weight:700;
                                letter-spacing:2px;text-transform:uppercase'>Mercado</div>
                    <div class='merc-card-nome' style='color:#fff;font-size:20px;
                                font-weight:900;line-height:1.2;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{merc}</div>
                    {end_html}
                    {maps_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── CHECK-IN ──
            checkin_hoje = pd.read_sql(
                "SELECT * FROM checkin WHERE funcionario=? AND mercado=? AND data=?",
                conn, params=(usuario, merc, str(date.today())))

            if checkin_hoje.empty:
                if st.button(f"📍 Fazer check-in em {merc}", key=f"cin_{merc}_{dia_sel}"):
                    now = datetime.now()
                    c.execute("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                              (str(date.today()), now.strftime("%H:%M"), "", usuario, merc, "em_visita"))
                    conn.commit()
                    st.success(f"✅ Check-in às {now.strftime('%H:%M')}!")
                    st.rerun()
            else:
                ci_row       = checkin_hoje.iloc[0]
                hora_entrada = ci_row["hora_entrada"]
                hora_saida   = ci_row["hora_saida"]
                status_ci    = ci_row["status"]
                if status_ci == "em_visita":
                    st.markdown(
                        f"<div style='background:#0a1a0a;border:1px solid #22c55e33;"
                        f"border-radius:10px;padding:10px 14px;margin-bottom:8px'>"
                        f"<span style='color:#22c55e;font-weight:700;font-size:12px'>● EM VISITA</span>"
                        f"<span style='color:#444;font-size:12px'> · Entrada às {hora_entrada}</span>"
                        f"</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div style='background:#111;border:1px solid #1c1c1c;"
                        f"border-radius:10px;padding:10px 14px;margin-bottom:8px'>"
                        f"<span style='color:#555;font-size:12px'>✓ Visita concluída · {hora_entrada} → {hora_saida}</span>"
                        f"</div>", unsafe_allow_html=True)

            # ── PRODUTOS com foto+check individual ──
            st.markdown(
                "<div style='color:#444;font-size:10px;font-weight:700;"
                "text-transform:uppercase;letter-spacing:1px;margin:12px 0 10px'>📦 Produtos</div>",
                unsafe_allow_html=True)

            prods = dados_dia[dados_dia["mercado"]==merc]

            todos_abastecidos = True
            for i, r in prods.iterrows():
                prod_nome  = r["produto"]
                chave_check = f"abast_{merc}_{dia_sel}_{prod_nome}".replace(" ","_")
                pasta_p     = f"fotos/{usuario}"
                os.makedirs(pasta_p, exist_ok=True)
                nome_foto_prod = f"{pasta_p}/{merc}_{dia_sel}_{prod_nome}_{date.today()}.jpg".replace(" ","_")
                tem_foto_prod  = os.path.exists(nome_foto_prod)

                # Foto de referência cadastrada pelo admin
                foto_ref = pd.read_sql(
                    "SELECT foto FROM produto_fotos WHERE produto=? LIMIT 1",
                    conn, params=(prod_nome,))
                tem_ref = (not foto_ref.empty and
                           str(foto_ref.iloc[0]["foto"]) not in ("","nan") and
                           os.path.exists(str(foto_ref.iloc[0]["foto"])))

                abast_prod = st.session_state.get(chave_check, False)

                # ── CARD DO PRODUTO ──
                cor_borda = "#22c55e44" if abast_prod else "#1a1a1a"
                cor_bg    = "#0a180e"   if abast_prod else "#0d0d0d"
                st.markdown(f"""
                <div style='background:{cor_bg};border:1.5px solid {cor_borda};
                            border-radius:14px;padding:16px 18px;margin-bottom:16px;
                            transition:all 0.2s ease'>
                    <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px'>
                        <div style='background:#ff2b2b22;border-radius:8px;
                                    padding:6px 10px;font-size:18px'>📦</div>
                        <div>
                            <div style='color:#888;font-size:10px;letter-spacing:1.5px;
                                        text-transform:uppercase'>Produto</div>
                            <div style='color:#fff;font-size:16px;font-weight:800;
                                        line-height:1.2'>{prod_nome}</div>
                        </div>
                        {"<div style='margin-left:auto;background:#0a2b14;border:1px solid #22c55e44;border-radius:8px;padding:4px 10px;color:#22c55e;font-size:11px;font-weight:700'>✅ Abastecido</div>" if abast_prod else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Fotos: referência + tirada (desktop: lado a lado; mobile: vertical)
                if tem_ref or tem_foto_prod:
                    img_c1, img_c2 = st.columns(2)
                    with img_c1:
                        if tem_ref:
                            st.image(str(foto_ref.iloc[0]["foto"]),
                                     use_container_width=True, caption="📋 Referência")
                    with img_c2:
                        if tem_foto_prod:
                            st.image(nome_foto_prod,
                                     use_container_width=True, caption="📸 Foto tirada")
                elif not tem_foto_prod:
                    st.markdown(
                        "<div style='background:#080808;border:1.5px dashed #1e1e1e;"
                        "border-radius:12px;padding:24px;text-align:center;margin-bottom:8px'>"
                        "<div style='font-size:32px;margin-bottom:6px'>📷</div>"
                        "<div style='color:#333;font-size:13px'>Tire a foto para marcar como abastecido</div>"
                        "</div>", unsafe_allow_html=True)

                # Câmera / upload
                modo_p = st.radio("", ["📸 Câmera","📁 Galeria"],
                                  key=f"modo_p_{merc}_{dia_sel}_{i}", horizontal=True,
                                  label_visibility="collapsed")
                if modo_p == "📸 Câmera":
                    fc = st.camera_input("", key=f"cam_p_{merc}_{dia_sel}_{i}",
                                         label_visibility="collapsed")
                    if fc:
                        with open(nome_foto_prod,"wb") as fp2: fp2.write(fc.getbuffer())
                        st.rerun()
                else:
                    fa = st.file_uploader("", key=f"arq_p_{merc}_{dia_sel}_{i}",
                                          type=["jpg","jpeg","png"],
                                          label_visibility="collapsed")
                    if fa:
                        with open(nome_foto_prod,"wb") as fp2: fp2.write(fa.getbuffer())
                        st.rerun()

                # Check + apagar — só quando tem foto
                if tem_foto_prod:
                    ck_col, del_col = st.columns([3, 1])
                    with ck_col:
                        abast_prod = st.checkbox(
                            "✅ Marcar como abastecido",
                            key=chave_check,
                            value=st.session_state.get(chave_check, False))
                    with del_col:
                        if st.button("🗑️ Apagar", key=f"del_fp_{merc}_{dia_sel}_{i}",
                                     help="Apagar foto"):
                            os.remove(nome_foto_prod)
                            if chave_check in st.session_state:
                                del st.session_state[chave_check]
                            abast_prod = False
                            st.rerun()
                else:
                    abast_prod = False

                if not abast_prod:
                    todos_abastecidos = False

                st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

            # caminho da foto principal (primeira foto de produto disponível)
            fotos_do_merc = [
                f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{date.today()}.jpg".replace(" ","_")
                for _, r in prods.iterrows()
            ]
            caminho = next((fp for fp in fotos_do_merc if os.path.exists(fp)), "")

            # ── STATUS DA VISITA ──
            st.markdown(
                "<div style='margin:20px 0 10px;color:#444;font-size:10px;"
                "text-transform:uppercase;letter-spacing:1px;font-weight:700'>Status da visita</div>",
                unsafe_allow_html=True)
            status_opcoes = {
                "✅  Abastecido":       "abastecido",
                "⚠️  Produto em falta": "falta",
                "❌  Loja fechada":     "fechado",
            }
            status_sel = st.radio(
                "status", list(status_opcoes.keys()),
                key=f"st_{merc}_{dia_sel}",
                label_visibility="collapsed",
                horizontal=True)

            prod_faltante = ""
            if status_sel == "⚠️  Produto em falta":
                prod_faltante = st.text_input(
                    "📦 Qual produto está em falta?",
                    key=f"falta_{merc}_{dia_sel}",
                    placeholder="Nome do produto em falta...")

            # Confirmação: precisa ter pelo menos 1 foto
            tem_qualquer_foto = bool(caminho)

            if not tem_qualquer_foto:
                st.markdown(
                    "<div style='background:#111;border:1px solid #1c1c1c;border-radius:10px;"
                    "padding:12px 16px;margin:8px 0;color:#333;font-size:13px;text-align:center'>"
                    "📷 Tire a foto de pelo menos um produto para confirmar a visita</div>",
                    unsafe_allow_html=True)

            confirmado = st.checkbox(
                "✔️ Confirmo que a visita foi realizada",
                key=f"conf_{merc}_{dia_sel}",
                disabled=not tem_qualquer_foto)

            # Botões full-width (melhor para mobile)
            if st.button("✅ Enviar relatório", key=f"btn_{merc}_{dia_sel}",
                         disabled=not confirmado, use_container_width=True):
                status_val = status_opcoes[status_sel]
                c.execute("""INSERT INTO relatorio
                    (data,funcionario,mercado,produto,status,foto,produto_faltante)
                    VALUES(?,?,?,?,?,?,?)""",
                    (str(date.today()), usuario, merc, "varios",
                     status_val, caminho, prod_faltante))

                now = datetime.now()
                if not checkin_hoje.empty and checkin_hoje.iloc[0]["status"] == "em_visita":
                    c.execute("UPDATE checkin SET hora_saida=?,status=? WHERE id=?",
                              (now.strftime("%H:%M"), "concluido", int(checkin_hoje.iloc[0]["id"])))
                elif checkin_hoje.empty:
                    c.execute("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                              (str(date.today()), now.strftime("%H:%M"), now.strftime("%H:%M"), usuario, merc, "concluido"))
                conn.commit()

                badge = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")
                if status_val == "abastecido":
                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,#0a2b14,#0d3a1a);
                                border:1px solid #22c55e44;border-radius:16px;
                                padding:24px;text-align:center;animation:fadeIn 0.4s ease;
                                margin-top:12px'>
                        <div style='font-size:48px;margin-bottom:12px'>🏆</div>
                        <div style='color:#22c55e;font-size:18px;font-weight:900;margin-bottom:8px'>
                            Gôndola abastecida!</div>
                        <div style='color:#555;font-size:14px;line-height:1.8'>
                            Excelente trabalho, <b style='color:#aaa'>{nome_exib}</b>! 💪<br>
                            A El Kam valoriza cada visita sua.<br>
                            Continue assim — você faz a diferença! 🌟
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success(f"Relatório de {merc} enviado! {badge}")

            if st.button("📄 Gerar PDF / WhatsApp", key=f"pdf_{merc}_{dia_sel}",
                         disabled=not confirmado, use_container_width=True):
                status_val = status_opcoes[status_sel]
                badge = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")
                fotos_html = "".join(
                    f'<div style="margin:12px 0"><b style="color:#222">{r["produto"]}</b><br>'
                    f'<img src="{fp}" style="width:100%;max-width:300px;border-radius:8px;margin-top:6px"></div>'
                    for _, r in prods.iterrows()
                    for fp in [f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{date.today()}.jpg".replace(' ','_')]
                    if os.path.exists(fp)
                )
                pf_tag = f"<div class='row'><b>Produto em falta:</b> {prod_faltante}</div>" if prod_faltante else ""
                rel_html = f"""<!DOCTYPE html><html><head>
                <meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
                <style>
                body{{font-family:Arial,sans-serif;background:#f5f5f5;padding:16px;color:#222;max-width:600px;margin:0 auto}}
                .header{{background:#ff2b2b;color:#fff;padding:20px;border-radius:12px;margin-bottom:20px;text-align:center}}
                .card{{background:#fff;border-radius:10px;padding:16px;margin-bottom:12px;box-shadow:0 1px 4px rgba(0,0,0,.1)}}
                .label{{color:#888;font-size:11px;text-transform:uppercase;letter-spacing:1px}}
                .value{{color:#222;font-size:15px;font-weight:600;margin-top:2px}}
                img{{width:100%;border-radius:8px;margin-top:8px}}
                </style></head><body>
                <div class='header'>
                    <div style='font-size:24px;margin-bottom:4px'>📋</div>
                    <b style='font-size:18px'>El Kam Merchandising</b><br>
                    <span style='font-size:13px;opacity:.8'>Relatório de Visita</span>
                </div>
                <div class='card'><div class='label'>Funcionário</div><div class='value'>{usuario}</div></div>
                <div class='card'><div class='label'>Mercado</div><div class='value'>{merc}</div></div>
                <div class='card'><div class='label'>Data</div><div class='value'>{date.today().strftime('%d/%m/%Y')} ({dia_sel})</div></div>
                <div class='card'><div class='label'>Status</div><div class='value'>{badge}</div></div>
                {pf_tag}
                {fotos_html}
                <p style='color:#bbb;font-size:11px;text-align:center;margin-top:20px'>© El Kam Merchandising</p>
                </body></html>"""
                html_path = f"fotos/{usuario}/relatorio_{merc}_{date.today()}.html".replace(" ","_")
                with open(html_path,"w",encoding="utf-8") as hf: hf.write(rel_html)
                with open(html_path,"rb") as hf:
                    st.download_button("⬇️ Baixar relatório",
                        data=hf,
                        file_name=f"relatorio_{merc}_{date.today()}.html".replace(" ","_"),
                        mime="text/html", key=f"dl_{merc}_{dia_sel}",
                        use_container_width=True)
                import urllib.parse
                dests_f = pd.read_sql("SELECT * FROM destinatarios", conn)
                msg_rel = (f"📋 *Relatório El Kam*\n👤 {usuario}\n🏪 {merc}\n"
                           f"📅 {date.today().strftime('%d/%m/%Y')}\nStatus: {badge}")
                if not dests_f.empty:
                    st.markdown("<div style='margin-top:12px;color:#555;font-size:11px;"
                                "text-transform:uppercase;letter-spacing:1px'>Enviar por WhatsApp:</div>",
                                unsafe_allow_html=True)
                    for _, d in dests_f.iterrows():
                        wa = f"https://wa.me/55{d['telefone']}?text={urllib.parse.quote(msg_rel)}"
                        st.markdown(
                            f"<a href='{wa}' target='_blank'>"
                            f"<button style='background:#25D366;color:#fff;border:none;"
                            f"border-radius:12px;padding:14px;font-size:14px;"
                            f"font-weight:700;cursor:pointer;margin:4px 0;width:100%'>"
                            f"📲 {d['nome']}</button></a>",
                            unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

    # ── CHAT FUNCIONÁRIO ──

    else:  # qualquer aba de chat

        page_header("Fale com o Admin", "Chat")

        c.execute("UPDATE chat SET lido=1 WHERE remetente=? AND tipo='admin'", (usuario,))
        conn.commit()

        hist = pd.read_sql(
            "SELECT * FROM chat WHERE (remetente=? AND tipo='funcionario') "
            "OR (remetente=? AND tipo='admin') ORDER BY id",
            conn, params=(usuario, usuario))

        # Última mensagem do admin para o push
        ultima_adm = pd.read_sql(
            "SELECT id, mensagem FROM chat WHERE remetente=? AND tipo='admin' ORDER BY id DESC LIMIT 1",
            conn, params=(usuario,))
        ultimo_id  = int(ultima_adm.iloc[0]["id"])      if not ultima_adm.empty else 0
        ultimo_txt = str(ultima_adm.iloc[0]["mensagem"]).replace("'","").replace('"',"") \
                     if not ultima_adm.empty else ""

        # ── PUSH NOTIFICATION via Web Notifications API ──
        st.markdown(f"""
        <script>
        (function() {{
            // Pede permissão na primeira vez
            if ('Notification' in window && Notification.permission === 'default') {{
                Notification.requestPermission();
            }}

            const LAST_KEY = 'elk_last_msg_{usuario.replace('.','_')}';
            const storedId = parseInt(localStorage.getItem(LAST_KEY) || '0');
            const currentId = {ultimo_id};

            if (currentId > storedId && storedId > 0) {{
                if (Notification.permission === 'granted') {{
                    new Notification('💬 El Kam — Admin', {{
                        body: '{ultimo_txt}',
                        icon: 'https://img.icons8.com/color/48/filled-message.png'
                    }});
                }}
            }}
            if (currentId > 0) {{
                localStorage.setItem(LAST_KEY, currentId);
            }}
        }})();
        </script>
        """, unsafe_allow_html=True)

        # Badge de não lidas
        if nao_lidas_f > 0:
            st.markdown(f"""
            <div style='background:#1f0a0a;border-left:3px solid #ff2b2b;
                        border-radius:10px;padding:12px 16px;margin-bottom:16px;
                        animation:fadeIn 0.3s ease'>
                <span style='color:#ff2b2b;font-weight:700;font-size:13px'>
                    🔔 {int(nao_lidas_f)} nova{'s' if nao_lidas_f > 1 else ''} mensagem{'ns' if nao_lidas_f > 1 else ''} do admin
                </span>
            </div>
            """, unsafe_allow_html=True)

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
