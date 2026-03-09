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
    height:62px; align-items:center; justify-content:space-around; padding:0 8px;
}
.mob-nav-btn {
    display:flex; flex-direction:column; align-items:center; gap:3px;
    color:#444; font-size:10px; font-weight:600; letter-spacing:0.5px;
    text-transform:uppercase; background:none; border:none; cursor:pointer;
    padding:6px 16px; border-radius:10px; transition:all 0.15s;
}
.mob-nav-btn.active, .mob-nav-btn:hover { color:#ff2b2b; }
.mob-nav-btn .ico { font-size:20px; }
@media (max-width:768px) {
    .mob-nav { display:flex !important; }
    .block-container { padding-bottom:80px !important; }
    [data-testid="stSidebar"] { display:none !important; }
}

/* ── STATUS BADGES ── */
.badge-ok    { background:#0a2b14; color:#22c55e; border:1px solid #22c55e44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-falta { background:#2b1f0a; color:#f59e0b; border:1px solid #f59e0b44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-fecha { background:#2b0a0a; color:#ff4444; border:1px solid #ff444444; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }

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
    id INTEGER PRIMARY KEY AUTOINCREMENT, mercado TEXT, endereco TEXT UNIQUE)""")
c.execute("""CREATE TABLE IF NOT EXISTS produtos (mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS agenda (
    funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS relatorio (
    data TEXT, funcionario TEXT, mercado TEXT, produto TEXT, status TEXT, foto TEXT)""")
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

    _, col_center, _ = st.columns([1, 1.2, 1])

    with col_center:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

        # Logo
        if os.path.exists("el_kam_logo.png"):
            st.image("el_kam_logo.png", use_container_width=True)
        else:
            st.markdown("""
            <div style='text-align:center;margin-bottom:28px'>
                <div style='display:inline-flex;align-items:center;justify-content:center;
                            width:72px;height:72px;background:#1a0000;border:1px solid #ff2b2b33;
                            border-radius:18px;font-size:32px;margin-bottom:16px'>🏪</div>
                <div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:3px;
                            text-transform:uppercase;margin-bottom:6px'>El Kam</div>
                <div style='color:#ffffff;font-size:26px;font-weight:900;line-height:1.1'>
                    Sistema de Promotores</div>
                <div style='color:#333;font-size:12px;margin-top:8px'>
                    Acesse com suas credenciais</div>
            </div>
            """, unsafe_allow_html=True)

        # ── TELA: LOGIN ──
        if st.session_state["tela_login"] == "login":
            st.markdown("""
            <div style='background:#111;border:1px solid #1c1c1c;border-radius:16px;padding:28px 28px 24px'>
            """, unsafe_allow_html=True)

            usuario_input = st.text_input("Usuário", placeholder="seu.login", key="li_user")
            senha_input   = st.text_input("Senha", type="password", placeholder="••••••••", key="li_pass")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

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

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("🔑 Esqueci minha senha", use_container_width=True):
                st.session_state["tela_login"] = "recuperar"
                st.rerun()

        # ── TELA: RECUPERAR ──
        elif st.session_state["tela_login"] == "recuperar":
            st.markdown("""
            <div style='background:#111;border:1px solid #1c1c1c;border-radius:16px;padding:28px'>
            """, unsafe_allow_html=True)
            st.markdown(
                "<div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2px;"
                "text-transform:uppercase;margin-bottom:8px'>Recuperar acesso</div>"
                "<div style='color:#fff;font-size:16px;font-weight:700;margin-bottom:4px'>Digite seu usuário</div>"
                "<div style='color:#444;font-size:12px;margin-bottom:16px'>Um código será enviado para o email cadastrado.</div>",
                unsafe_allow_html=True)

            rec_user = st.text_input("Usuário", key="rec_user", placeholder="admin")
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
                            🔗 Link do sistema: <a href='https://elkam-merchandising.streamlit.app'
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

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("← Voltar ao login", use_container_width=True):
                st.session_state["tela_login"] = "login"; st.rerun()

        # ── TELA: CÓDIGO ──
        elif st.session_state["tela_login"] == "codigo":
            st.markdown("""
            <div style='background:#111;border:1px solid #1c1c1c;border-radius:16px;padding:28px'>
            """, unsafe_allow_html=True)
            em = st.session_state.get("rec_email_mascarado","seu email")
            st.markdown(
                f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2px;"
                f"text-transform:uppercase;margin-bottom:8px'>Verificação</div>"
                f"<div style='color:#fff;font-size:16px;font-weight:700;margin-bottom:4px'>Código enviado</div>"
                f"<div style='color:#444;font-size:12px;margin-bottom:16px'>Verifique {em}</div>",
                unsafe_allow_html=True)

            codigo_input  = st.text_input("Código de 6 dígitos", key="cod_input",
                                          placeholder="000000", max_chars=6)
            nova_senha_r  = st.text_input("Nova senha", type="password", key="nova_rec")
            confirma_r    = st.text_input("Confirmar senha", type="password", key="conf_rec")

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

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
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

    menu = st.sidebar.selectbox(
        "MENU",
        ["Dashboard", "Funcionários", "Mercados", "Agenda", "Relatórios", "Fotos",
         "Chat", "Empresa", "Destinatários", "⚙️ Configurações"]
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

        if mdf.empty:
            st.info("Nenhum mercado cadastrado.")
        else:
            for _, row in mdf.iterrows():
                col_i, col_ed, col_ex = st.columns([5, 1, 1])
                with col_i:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;padding:10px 0'>"
                        f"🏪 <b>{row['mercado']}</b>"
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

                # Formulário de edição inline
                if st.session_state.get(f"editando_{row['id']}", False):
                    with st.container():
                        st.markdown(
                            f"<div style='background:#141414;border:1px solid #ff2b2b33;"
                            f"border-radius:10px;padding:16px;margin-bottom:12px'>",
                            unsafe_allow_html=True)
                        ea, eb = st.columns(2)
                        with ea:
                            novo_nome = st.text_input("Novo nome", value=row["mercado"],
                                                      key=f"edit_nome_{row['id']}")
                        with eb:
                            novo_end = st.text_input("Novo endereço", value=row["endereco"],
                                                     key=f"edit_end_{row['id']}")
                        ec, ed = st.columns([1, 1])
                        with ec:
                            if st.button("✅ Salvar", key=f"save_merc_{row['id']}"):
                                if not novo_nome.strip() or not novo_end.strip():
                                    st.warning("Preencha nome e endereço.")
                                else:
                                    nome_antigo = row["mercado"]
                                    c.execute("UPDATE mercados SET mercado=?, endereco=? WHERE id=?",
                                              (novo_nome.strip(), novo_end.strip(), int(row["id"])))
                                    # Atualiza referências na agenda
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
                        st.markdown("</div>", unsafe_allow_html=True)

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
                    fazer_backup()
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
                    fazer_backup()
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

                # ── CHECK-IN ──
                checkin_hoje = pd.read_sql(
                    "SELECT * FROM checkin WHERE funcionario=? AND mercado=? AND data=?",
                    conn, params=(usuario, merc, str(date.today())))

                if checkin_hoje.empty:
                    if st.button(f"📍 Fazer check-in", key=f"cin_{merc}_{dia_sel}"):
                        now = datetime.now()
                        c.execute("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                                  (str(date.today()), now.strftime("%H:%M"), "", usuario, merc, "em_visita"))
                        conn.commit()
                        st.success(f"✅ Check-in às {now.strftime('%H:%M')}!")
                        st.rerun()
                else:
                    ci_row = checkin_hoje.iloc[0]
                    hora_entrada = ci_row["hora_entrada"]
                    hora_saida   = ci_row["hora_saida"]
                    status_ci    = ci_row["status"]

                    if status_ci == "em_visita":
                        st.markdown(
                            f"<div style='background:#0a1a0a;border:1px solid #22c55e33;"
                            f"border-radius:10px;padding:10px 14px;margin-bottom:12px;'>"
                            f"<span style='color:#22c55e;font-size:12px;font-weight:700'>● EM VISITA</span>"
                            f"<span style='color:#444;font-size:12px'> · Entrada às {hora_entrada}</span>"
                            f"</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"<div style='background:#111;border:1px solid #1c1c1c;"
                            f"border-radius:10px;padding:10px 14px;margin-bottom:12px;'>"
                            f"<span style='color:#555;font-size:12px'>✓ Visita concluída · "
                            f"{hora_entrada} → {hora_saida}</span>"
                            f"</div>", unsafe_allow_html=True)

                # ── PRODUTOS ──
                prods = dados_dia[dados_dia["mercado"]==merc]
                st.markdown(
                    "<div style='margin:10px 0 6px;color:#444;font-size:10px;"
                    "text-transform:uppercase;letter-spacing:1px'>Produtos</div>",
                    unsafe_allow_html=True)
                for i, r in prods.iterrows():
                    st.checkbox(r["produto"], key=f"ck_{dia_sel}_{i}")

                # ── STATUS DA VISITA ──
                st.markdown(
                    "<div style='margin:14px 0 8px;color:#444;font-size:10px;"
                    "text-transform:uppercase;letter-spacing:1px'>Status da visita</div>",
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
                    horizontal=True
                )

                # ── FOTO (câmera ou arquivo) ──
                st.markdown(
                    "<div style='margin:14px 0 8px;color:#444;font-size:10px;"
                    "text-transform:uppercase;letter-spacing:1px'>📷 Foto da gôndola</div>",
                    unsafe_allow_html=True)
                modo_foto = st.radio("Origem", ["📸 Câmera", "📁 Arquivo"],
                                     key=f"modo_{merc}_{dia_sel}", horizontal=True,
                                     label_visibility="collapsed")
                caminho = ""
                pasta = f"fotos/{usuario}"
                os.makedirs(pasta, exist_ok=True)
                nome_foto = f"{pasta}/{merc}_{dia_sel}_{date.today()}.jpg".replace(" ","_")

                if modo_foto == "📸 Câmera":
                    foto_cam = st.camera_input("Tirar foto", key=f"cam_{merc}_{dia_sel}",
                                               label_visibility="collapsed")
                    if foto_cam:
                        with open(nome_foto, "wb") as f: f.write(foto_cam.getbuffer())
                        caminho = nome_foto
                else:
                    foto_arq = st.file_uploader("Selecionar foto",
                                                key=f"arq_{merc}_{dia_sel}", type=["jpg","jpeg","png"],
                                                label_visibility="collapsed")
                    if foto_arq:
                        with open(nome_foto, "wb") as f: f.write(foto_arq.getbuffer())
                        caminho = nome_foto
                        st.image(nome_foto, width=280)

                # ── CONFIRMAÇÃO ──
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                confirmado = st.checkbox(
                    "✔️ Confirmo que a visita foi realizada",
                    key=f"conf_{merc}_{dia_sel}")

                # ── ENVIAR ──
                col_env, col_pdf = st.columns(2)
                with col_env:
                    if st.button("✅ Enviar relatório", key=f"btn_{merc}_{dia_sel}",
                                 disabled=not confirmado):
                        status_val = status_opcoes[status_sel]

                        pd.DataFrame([{"data":str(date.today()),"funcionario":usuario,
                                       "mercado":merc,"produto":"varios",
                                       "status":status_val,"foto":caminho}])\
                          .to_sql("relatorio", conn, if_exists="append", index=False)

                        now = datetime.now()
                        if not checkin_hoje.empty and checkin_hoje.iloc[0]["status"] == "em_visita":
                            c.execute("UPDATE checkin SET hora_saida=?, status=? WHERE id=?",
                                      (now.strftime("%H:%M"), "concluido", int(checkin_hoje.iloc[0]["id"])))
                        elif checkin_hoje.empty:
                            c.execute("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                                      (str(date.today()), now.strftime("%H:%M"), now.strftime("%H:%M"), usuario, merc, "concluido"))
                        conn.commit()

                        badge = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")
                        st.success(f"Relatório de {merc} enviado! {badge}")

                with col_pdf:
                    if st.button("📄 Gerar e enviar PDF", key=f"pdf_{merc}_{dia_sel}",
                                 disabled=not confirmado):
                        status_val = status_opcoes[status_sel]
                        # Gera HTML do relatório para compartilhar via WhatsApp
                        foto_tag = f'<img src="{caminho}" style="width:100%;border-radius:8px;margin-top:10px">' \
                                   if caminho and os.path.exists(caminho) else ""
                        relatorio_html = f"""
                        <html><head><meta charset='utf-8'>
                        <style>body{{font-family:Arial;background:#fff;padding:20px;color:#222}}
                        .header{{background:#ff2b2b;color:#fff;padding:16px;border-radius:8px;margin-bottom:16px}}
                        .row{{margin:8px 0;font-size:14px}}
                        .badge{{display:inline-block;padding:4px 12px;border-radius:4px;font-weight:bold;font-size:13px}}
                        .ok{{background:#d1fae5;color:#065f46}}
                        .falta{{background:#fef3c7;color:#92400e}}
                        .fecha{{background:#fee2e2;color:#991b1b}}
                        </style></head><body>
                        <div class='header'><b>El Kam Merchandising</b><br>Relatório de Visita</div>
                        <div class='row'><b>Funcionário:</b> {usuario}</div>
                        <div class='row'><b>Mercado:</b> {merc}</div>
                        <div class='row'><b>Data:</b> {date.today().strftime('%d/%m/%Y')}</div>
                        <div class='row'><b>Dia:</b> {dia_sel}</div>
                        <div class='row'><b>Status:</b>
                          <span class='badge {"ok" if status_val=="abastecido" else "falta" if status_val=="falta" else "fecha"}'>
                          {badge}</span></div>
                        {foto_tag}
                        </body></html>
                        """
                        # Salva HTML temporário para download
                        html_path = f"fotos/{usuario}/relatorio_{merc}_{date.today()}.html".replace(" ","_")
                        with open(html_path, "w", encoding="utf-8") as hf:
                            hf.write(relatorio_html)

                        # Botão download do relatório
                        with open(html_path, "rb") as hf:
                            st.download_button(
                                "⬇️ Baixar relatório",
                                data=hf,
                                file_name=f"relatorio_{merc}_{date.today()}.html".replace(" ","_"),
                                mime="text/html",
                                key=f"dl_{merc}_{dia_sel}"
                            )

                        # Links WhatsApp para destinatários
                        dests = pd.read_sql("SELECT * FROM destinatarios", conn)
                        msg_rel = (
                            f"📋 *Relatório El Kam*\n"
                            f"👤 {usuario}\n🏪 {merc}\n📅 {date.today().strftime('%d/%m/%Y')}\n"
                            f"Status: {badge}\n\n_Relatório anexado._"
                        )
                        import urllib.parse
                        if not dests.empty:
                            st.markdown("<div style='margin-top:8px;color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px'>Enviar para:</div>", unsafe_allow_html=True)
                            for _, d in dests.iterrows():
                                wa = f"https://wa.me/55{d['telefone']}?text={urllib.parse.quote(msg_rel)}"
                                st.markdown(
                                    f"<a href='{wa}' target='_blank'>"
                                    f"<button style='background:#25D366;color:#fff;border:none;"
                                    f"border-radius:8px;padding:8px 14px;font-size:12px;"
                                    f"font-weight:600;cursor:pointer;margin:4px 0;width:100%'>"
                                    f"📲 Enviar para {d['nome']}</button></a>",
                                    unsafe_allow_html=True)

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
