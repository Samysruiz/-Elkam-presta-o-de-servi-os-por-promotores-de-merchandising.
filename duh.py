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


/* ── TABELA AGENDA ── */
.tab-ag{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:28px}
.tab-ag th{background:#111;color:#ff2b2b;text-align:center;padding:12px 14px;
           border-bottom:2px solid #1c1c1c;font-size:10px;letter-spacing:1.5px;text-transform:uppercase}
.tab-ag th:first-child{text-align:left;padding-left:14px}
.tab-ag td{padding:6px 12px;border:1px solid #141414;background:#0a0a0a;vertical-align:top}
.mn{color:#ff2b2b;font-weight:700;font-size:12px;display:block;padding-top:6px}
.pi{color:#888;font-size:12px;display:block}
.vz{background:#080808}

/* ── STATUS BADGES ── */
.badge-ok    { background:#0a2b14; color:#22c55e; border:1px solid #22c55e44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-falta { background:#2b1f0a; color:#f59e0b; border:1px solid #f59e0b44; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }
.badge-fecha { background:#2b0a0a; color:#ff4444; border:1px solid #ff444444; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:700; }

/* ── NAV BUTTONS: mobile-topnav — esconde no desktop, mostra no celular ── */
.mobile-topnav { display: block; }

@media (min-width: 769px) {
    /* Esconde os botões de nav rápida no desktop — sidebar já cuida da navegação */
    .mobile-topnav { display: none !important; }
}

/* Estilo dos botões quando visível no celular */
@media (max-width: 768px) {
    .mobile-topnav button {
        background: #111 !important;
        border: 1px solid #1e1e1e !important;
        border-radius: 12px !important;
        color: #888 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        padding: 8px 2px !important;
        white-space: pre-wrap !important;
        text-align: center !important;
        line-height: 1.3 !important;
        height: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        overflow: hidden !important;
    }
    .mobile-topnav button:hover,
    .mobile-topnav button:active {
        color: #ff2b2b !important;
        border-color: #ff2b2b44 !important;
        background: #1a0000 !important;
    }
}
/* Desktop: mesma altura para todos os botões da nav lateral */
.mobile-topnav button {
    height: 56px !important;
    min-height: 56px !important;
    overflow: hidden !important;
}
[data-testid="stButton"] button[kind="secondary"] {
    background-color: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 10px !important;
    color: #ddd !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
    width: 100% !important;
    padding: 14px 16px !important;
    margin-bottom: 2px !important;
    transition: background 0.15s !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background-color: #161616 !important;
    border-color: #ff2b2b44 !important;
}

/* ── ESCONDE BOTÃO DE RECOLHER SIDEBAR (keyboard_double_arrow) ── */
[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"],
button[aria-label="collapse sidebar"],
button[aria-label="expand sidebar"],
.st-emotion-cache-dvne4q,
.st-emotion-cache-1rtdyuf,
.eyeqlp53,
section[data-testid="stSidebar"] > div > div > button:first-child {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* ── ELIMINA TODOS OS ÍCONES MATERIAL QUE VAZAM COMO TEXTO ── */
/* Zera o tamanho de fonte de qualquer elemento usando Material Symbols/Icons */
.material-symbols-rounded,
.material-symbols-outlined,
.material-symbols-sharp,
.material-icons,
.material-icons-outlined,
.material-icons-round,
.material-icons-sharp,
[class*="material-symbols"],
[class*="material-icons"] {
    font-size: 0 !important;
    line-height: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    display: inline-block !important;
    color: transparent !important;
}
/* Esconde SVGs do expander (caso algum ainda exista) */
[data-testid="stExpander"] summary svg,
[data-testid="stExpander"] summary > div > svg { display: none !important; }
[data-testid="stExpander"] summary { padding: 14px 16px !important; }
[data-testid="stExpander"] summary p {
    color: #ddd !important; font-weight: 600 !important;
    font-size: 13px !important; font-family: 'Inter', sans-serif !important;
}


@keyframes fadeIn {
    from { opacity:0; transform:translateY(12px); }
    to   { opacity:1; transform:translateY(0); }
}
</style>

<!-- JS: elimina QUALQUER texto de ícone Material que vaze no DOM -->
<script>
(function(){
    var BAD = ["keyboard_double_arrow_right","keyboard_double_arrow_left",
               "keyboard_double_arrow_up","keyboard_double_arrow_down",
               "keyboard_arrow_right","keyboard_arrow_left",
               "keyboard_arrow_up","keyboard_arrow_down",
               "expand_more","expand_less","chevron_right","chevron_left",
               "arrow_forward_ios","arrow_back_ios","menu","close"];
    function scrub(){
        var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        var node;
        while((node = walker.nextNode())){
            if(BAD.indexOf(node.textContent.trim()) !== -1){
                node.textContent = '';
            }
        }
        // Also zero-out any element with Material font
        document.querySelectorAll('*').forEach(function(el){
            try {
                var ff = window.getComputedStyle(el).fontFamily || '';
                if(ff.indexOf('Material') !== -1 && el.textContent.trim().length < 40){
                    el.style.cssText += ';font-size:0!important;color:transparent!important;width:0!important;overflow:hidden!important';
                }
            } catch(e){}
        });
        // Esconde botão de colapso da sidebar (keyboard_double_arrow nativo do Streamlit)
        document.querySelectorAll('[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"]').forEach(function(el){
            el.style.cssText += ';display:none!important;visibility:hidden!important;pointer-events:none!important';
        });
        // Botão dentro da sidebar com SVG de seta
        document.querySelectorAll('section[data-testid="stSidebar"] button').forEach(function(btn){
            var svg = btn.querySelector('svg');
            if(svg && !btn.textContent.trim()){
                btn.style.cssText += ';display:none!important';
            }
        });
    }
    var obs = new MutationObserver(scrub);
    obs.observe(document.body, {childList:true, subtree:true, characterData:true});
    [200, 800, 2000, 4000].forEach(function(t){ setTimeout(scrub, t); });
})();
</script>

<!-- JS: força câmera frontal (facingMode: user) no st.camera_input -->
<script>
(function(){
    var _origGetUserMedia = navigator.mediaDevices && navigator.mediaDevices.getUserMedia
        ? navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices) : null;
    if(_origGetUserMedia){
        navigator.mediaDevices.getUserMedia = function(constraints){
            if(constraints && constraints.video){
                if(typeof constraints.video === 'object'){
                    constraints.video.facingMode = {ideal: 'user'};
                } else {
                    constraints.video = {facingMode: {ideal: 'user'}};
                }
            }
            return _origGetUserMedia(constraints);
        };
    }
})();
</script>

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
#  BANCO — conexão segura, WAL, cache por sessão
# ═══════════════════════════════════════════════

import threading, time as _time

for _d in ["fotos","logos_mercados","fotos_produtos","empresa","backups"]:
    os.makedirs(_d, exist_ok=True)

# Limpa fotos órfãs com mais de 2 dias (caso func não tenha enviado relatório)
def _limpar_fotos_antigas():
    limite = _time.time() - 2 * 86400  # 2 dias
    for root, _, files in os.walk("fotos"):
        for fname in files:
            if fname.endswith((".jpg",".jpeg",".png")):
                fpath = os.path.join(root, fname)
                try:
                    if os.path.getmtime(fpath) < limite:
                        os.remove(fpath)
                except Exception:
                    pass

_limpar_fotos_antigas()

@st.cache_resource
def get_conn():
    """Conexão única cacheada por processo — thread-safe com WAL."""
    _conn = sqlite3.connect(
        "duh.db",
        check_same_thread=False,   # gerenciamos o lock manualmente
        timeout=30,                # espera até 30s por lock
        isolation_level=None,      # autocommit desativado; usamos BEGIN/COMMIT explícitos
    )
    _conn.execute("PRAGMA journal_mode=WAL")      # múltiplos leitores simultâneos
    _conn.execute("PRAGMA synchronous=NORMAL")    # mais rápido, ainda seguro
    _conn.execute("PRAGMA foreign_keys=ON")
    _conn.execute("PRAGMA cache_size=-8000")      # 8 MB de cache
    _conn.execute("PRAGMA busy_timeout=30000")    # 30s antes de "database is locked"
    return _conn

conn = get_conn()
_db_lock = threading.Lock()   # lock Python para serializar escritas

def db_exec(sql: str, params=(), retries: int = 5) -> sqlite3.Cursor:
    """Executa SQL com retry automático em caso de lock."""
    for attempt in range(retries):
        try:
            with _db_lock:
                cur = conn.cursor()
                cur.execute(sql, params)
                # committed by db_exec
                return cur
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < retries - 1:
                _time.sleep(0.2 * (attempt + 1))
            else:
                raise

def db_many(sql: str, data: list, retries: int = 5):
    """executemany com retry automático."""
    for attempt in range(retries):
        try:
            with _db_lock:
                cur = conn.cursor()
                cur.executemany(sql, data)
                # committed by db_exec
                return cur
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < retries - 1:
                _time.sleep(0.2 * (attempt + 1))
            else:
                raise

def db_read(sql: str, params=()) -> pd.DataFrame:
    """Leitura segura — não precisa de lock pois WAL permite leitores simultâneos."""
    try:
        return pd.read_sql(sql, conn, params=list(params))
    except Exception:
        return pd.DataFrame()

# Cursor simples para uso nas migrações (só na inicialização, sem concorrência ainda)
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
# committed by db_exec

# ── MIGRAÇÕES ──
agenda_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(agenda)").fetchall()]
if "dia" not in agenda_cols:
    db_exec("ALTER TABLE agenda RENAME TO agenda_bkp")
    db_exec("CREATE TABLE agenda (funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)")
    try: c.execute("INSERT INTO agenda SELECT funcionario,'Segunda',mercado,produto FROM agenda_bkp")
    except: pass
    db_exec("DROP TABLE IF EXISTS agenda_bkp")
    # committed by db_exec

usuarios_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(usuarios)").fetchall()]
if "primeiro_acesso" not in usuarios_cols:
    db_exec("ALTER TABLE usuarios ADD COLUMN primeiro_acesso INTEGER DEFAULT 0")
    # committed by db_exec
if "telefone" not in usuarios_cols:
    db_exec("ALTER TABLE usuarios ADD COLUMN telefone TEXT DEFAULT ''")
    # committed by db_exec
if "email" not in usuarios_cols:
    db_exec("ALTER TABLE usuarios ADD COLUMN email TEXT DEFAULT ''")
    # committed by db_exec

mercados_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(mercados)").fetchall()]
if "logo" not in mercados_cols:
    db_exec("ALTER TABLE mercados ADD COLUMN logo TEXT DEFAULT ''")
    # committed by db_exec

relatorio_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(relatorio)").fetchall()]
if "produto_faltante" not in relatorio_cols:
    db_exec("ALTER TABLE relatorio ADD COLUMN produto_faltante TEXT DEFAULT ''")
    # committed by db_exec

usuarios_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(usuarios)").fetchall()]

if db_read("SELECT * FROM usuarios").empty:
    db_exec("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone,email) VALUES(?,?,?,?,?,?)",
              ('admin','123','admin',0,'',''))

# Garante que o superadmin existe sempre (recria se apagado acidentalmente)
if db_read("SELECT * FROM usuarios WHERE usuario='superadmin'").empty:
    db_exec("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone,email) VALUES(?,?,?,?,?,?)",
              ('superadmin','elkam@super2025','superadmin',0,'',''))

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
    r = conn.cursor().execute("SELECT valor FROM config WHERE chave=?", (chave,)).fetchone()
    return r[0] if r else padrao

def salvar_config(chave: str, valor: str):
    db_exec("INSERT OR REPLACE INTO config (chave,valor) VALUES(?,?)", (chave, valor))
    # committed by db_exec

# ═══════════════════════════════════════════════
#  SESSION
# ═══════════════════════════════════════════════

if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "modo_view" not in st.session_state:
    st.session_state["modo_view"] = "admin"   # superadmin: "admin" ou "funcionario"

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
                user = conn.cursor().execute(
                    "SELECT * FROM usuarios WHERE LOWER(usuario)=LOWER(?) AND senha=?",
                    (u, senha_input)).fetchone()
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
                row = conn.cursor().execute(
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
                    db_exec("UPDATE usuarios SET senha=? WHERE LOWER(usuario)=LOWER(?)",
                              (nova_senha_r, cod_user))
                    salvar_config("codigo_rec", "")
                    # committed by db_exec
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

# Superadmin pode alternar entre visão admin e funcionário
is_superadmin = (tipo == "superadmin")
if is_superadmin:
    tipo_efetivo = st.session_state["modo_view"]
else:  # funcionario / superadmin modo funcionario

    # Superadmin simulando funcionário: usa o usuário selecionado
    if is_superadmin and st.session_state.get("superadmin_simular"):
        usuario = st.session_state["superadmin_simular"]

    # Banner de modo superadmin (só visível para você)
    if is_superadmin:
        nome_sim = st.session_state.get("superadmin_simular", "—")
        st.markdown(f"""
        <div style='background:linear-gradient(90deg,#1a1000,#1a0a00);
                    border:1.5px solid #f59e0b55;border-radius:12px;
                    padding:12px 18px;margin-bottom:20px;
                    display:flex;align-items:center;gap:14px'>
            <div style='font-size:24px'>🔧</div>
            <div>
                <div style='color:#f59e0b;font-size:11px;font-weight:700;
                            letter-spacing:2px;text-transform:uppercase'>Modo Superadmin</div>
                <div style='color:#666;font-size:12px;margin-top:2px'>
                    Simulando funcionário: <b style='color:#ddd'>{nome_sim}</b>
                    &nbsp;·&nbsp;
                    <span style='color:#f59e0b'>Invisível para o cliente</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    tipo_efetivo = tipo

# ═══════════════════════════════════════════════
#  PRIMEIRO ACESSO
# ═══════════════════════════════════════════════

conn.cursor().execute("SELECT primeiro_acesso FROM usuarios WHERE usuario=?", (usuario,))
row_pa = c.fetchone()
if row_pa and row_pa[0] == 1 and tipo != "superadmin":
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
                db_exec("UPDATE usuarios SET senha=?, primeiro_acesso=0 WHERE usuario=?", (nova_s, usuario))
                # committed by db_exec
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
        for _k in list(st.session_state.keys()):
            del st.session_state[_k]
        st.rerun()

    # ── SUPERADMIN: toggle de modo ──
    if is_superadmin:
        st.markdown("""
        <div style='margin-top:20px;padding-top:16px;border-top:1px solid #1c1c1c'>
            <div style='color:#f59e0b;font-size:10px;font-weight:700;letter-spacing:2px;
                        text-transform:uppercase;margin-bottom:10px'>🔧 Modo Superadmin</div>
        </div>
        """, unsafe_allow_html=True)
        modo_atual = st.session_state["modo_view"]
        label_btn  = "👷 Ver como Funcionário" if modo_atual == "admin" else "🛡️ Ver como Admin"
        cor_btn    = "#f59e0b" if modo_atual == "admin" else "#3b82f6"
        st.markdown(f"""
        <div style='background:#1a1400;border:1px solid #f59e0b33;border-radius:10px;
                    padding:10px 14px;margin-bottom:10px;font-size:12px;color:#888;line-height:1.6'>
            Modo atual:<br>
            <b style='color:#f59e0b;font-size:14px'>
                {"🛡️ Admin" if modo_atual == "admin" else "👷 Funcionário"}
            </b>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label_btn, use_container_width=True):
            st.session_state["modo_view"] = "funcionario" if modo_atual == "admin" else "admin"
            st.rerun()
        # Seletor de qual funcionário simular (para ver agenda real)
        if modo_atual == "funcionario":
            funcs_sa = db_read("SELECT usuario FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")
            if not funcs_sa.empty:
                func_opts = funcs_sa["usuario"].tolist()
                func_sim = st.selectbox("👤 Simular funcionário",
                                        func_opts,
                                        key="superadmin_func_sim")
                st.session_state["superadmin_simular"] = func_sim
            else:
                st.info("Nenhum funcionário cadastrado.")

# ═══════════════════════════════════════════════════════
#  ADMIN
# ═══════════════════════════════════════════════════════

if tipo_efetivo == "admin":

    # ── ADMIN NAV ──
    _MENU_OPTS = ["Dashboard", "Funcionários", "Mercados", "Agenda", "Relatórios",
                  "Fotos", "Fotos de Produtos", "Chat", "Empresa",
                  "Destinatários", "⚙️ Configurações"]
    if "adm_menu" not in st.session_state:
        st.session_state["adm_menu"] = "Dashboard"
    menu = st.session_state["adm_menu"]

    # ── SIDEBAR: botões de navegação (desktop e celular) ──
    with st.sidebar:
        st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
        _icons = {"Dashboard":"📊","Funcionários":"👥","Mercados":"🏪","Agenda":"📋",
                  "Relatórios":"📈","Fotos":"📷","Fotos de Produtos":"🖼️","Chat":"💬",
                  "Empresa":"🏢","Destinatários":"📬","⚙️ Configurações":"⚙️"}
        for _opt in _MENU_OPTS:
            _ico = _icons.get(_opt, "•")
            _ativo = menu == _opt
            _style = "background:#ff2b2b22;border-color:#ff2b2b55;" if _ativo else ""
            _lbl = f"{_ico}  {_opt}"
            if st.button(_lbl, key=f"adm_nav_{_opt}", use_container_width=True):
                st.session_state["adm_menu"] = _opt
                st.rerun()

    # ── TOP NAV RÁPIDA — só aparece no celular (CSS esconde em desktop) ──
    st.markdown('<div class="mobile-topnav">', unsafe_allow_html=True)
    _nca,_ncb,_ncc,_ncd,_nce,_ncf,_ncg = st.columns(7)
    with _nca:
        if st.button("📊\nDash",    key="mn_d",   use_container_width=True): st.session_state["adm_menu"]="Dashboard";         st.rerun()
    with _ncb:
        if st.button("👥\nFuncs",   key="mn_f",   use_container_width=True): st.session_state["adm_menu"]="Funcionários";       st.rerun()
    with _ncc:
        if st.button("🏪\nMerc.", key="mn_m",   use_container_width=True): st.session_state["adm_menu"]="Mercados";           st.rerun()
    with _ncd:
        if st.button("📋\nAgenda",  key="mn_ag",  use_container_width=True): st.session_state["adm_menu"]="Agenda";             st.rerun()
    with _nce:
        if st.button("📈\nRelat.",  key="mn_r",   use_container_width=True): st.session_state["adm_menu"]="Relatórios";         st.rerun()
    with _ncf:
        if st.button("💬\nChat",    key="mn_c",   use_container_width=True): st.session_state["adm_menu"]="Chat";               st.rerun()
    with _ncg:
        if st.button("⚙️\nConf.",   key="mn_cfg", use_container_width=True): st.session_state["adm_menu"]="⚙️ Configurações";   st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── NOTIFICAÇÃO DE MENSAGENS NÃO LIDAS ──
    msgs_novas = db_read(
        "SELECT remetente, mensagem, hora FROM chat WHERE tipo='funcionario' AND lido=0 ORDER BY id DESC"
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
        _hd = date.today(); _od = _hd - timedelta(days=1)
        _is = _hd - timedelta(days=_hd.weekday()); _ia = _is - timedelta(days=7); _fa2 = _is - timedelta(days=1)
        _ra = db_read("SELECT * FROM relatorio"); _ca = db_read("SELECT * FROM checkin")
        if not _ra.empty: _ra["_d"] = pd.to_datetime(_ra["data"]).dt.date
        if not _ca.empty: _ca["_d"] = pd.to_datetime(_ca["data"]).dt.date
        def _fd(df,d): return df[df["_d"]==d] if not df.empty and "_d" in df.columns else pd.DataFrame()
        def _fr(df,d1,d2): return df[(df["_d"]>=d1)&(df["_d"]<=d2)] if not df.empty and "_d" in df.columns else pd.DataFrame()
        _rh=_fd(_ra,_hd); _ro=_fd(_ra,_od); _rs=_fr(_ra,_is,_hd); _rant=_fr(_ra,_ia,_fa2)
        section_title("📊 Hoje")
        _c1,_c2,_c3,_c4,_c5 = st.columns(5)
        _c1.metric("Relatórios hoje", len(_rh), delta=f"{len(_rh)-len(_ro):+d} vs ontem")
        _fah=_rh["funcionario"].nunique() if not _rh.empty else 0; _fao=_ro["funcionario"].nunique() if not _ro.empty else 0
        _c2.metric("Funcionários ativos", _fah, delta=f"{_fah-_fao:+d} vs ontem")
        _mah=_rh["mercado"].nunique() if not _rh.empty else 0; _mao=_ro["mercado"].nunique() if not _ro.empty else 0
        _c3.metric("Mercados visitados", _mah, delta=f"{_mah-_mao:+d} vs ontem")
        _pfh=len(_rh[_rh["status"]=="falta"]) if not _rh.empty else 0; _pfo=len(_ro[_ro["status"]=="falta"]) if not _ro.empty else 0
        _c4.metric("Produtos em falta", _pfh, delta=f"{_pfh-_pfo:+d} vs ontem", delta_color="inverse")
        _fth=len(_rh[_rh["foto"]!=""]) if not _rh.empty else 0; _fto=len(_ro[_ro["foto"]!=""]) if not _ro.empty else 0
        _c5.metric("Fotos enviadas", _fth, delta=f"{_fth-_fto:+d} vs ontem")
        _cih = _fd(_ca, _hd)
        if not _cih.empty:
            _uc = _cih.sort_values("id",ascending=False).iloc[0]
            st.markdown(f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:12px;padding:14px 18px;margin:16px 0;display:flex;gap:16px;align-items:center'><div style='font-size:28px'>⏱️</div><div><div style='color:#444;font-size:10px;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px'>Último relatório</div><div style='color:#fff;font-size:15px;font-weight:700'>{_uc.get('mercado','—')}</div><div style='color:#555;font-size:12px'>👤 {_uc.get('funcionario','—')} · {_uc.get('hora_entrada','—')}</div></div></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
        section_title("👥 Visitas por funcionário hoje")
        if not _rh.empty:
            _vf = _rh.groupby("funcionario").size().reset_index(name="n").sort_values("n",ascending=False)
            _mx = _vf["n"].max()
            for _ri,(_, _rrow) in enumerate(_vf.iterrows()):
                _pct=int(_rrow["n"]/_mx*100) if _mx>0 else 0
                _md2=["🥇","🥈","🥉"][_ri] if _ri<3 else "👤"
                st.markdown(f"<div style='margin-bottom:10px'><div style='display:flex;justify-content:space-between;margin-bottom:4px'><span style='color:#ddd;font-size:13px;font-weight:600'>{_md2} {_rrow['funcionario'].split('.')[0].capitalize()}</span><span style='color:#ff2b2b;font-size:13px;font-weight:700'>{int(_rrow['n'])} visitas</span></div><div style='background:#1a1a1a;border-radius:6px;height:6px'><div style='background:#ff2b2b;width:{_pct}%;height:6px;border-radius:6px'></div></div></div>", unsafe_allow_html=True)
        else: st.info("Nenhuma visita hoje.")
        _cia = db_read("SELECT * FROM checkin WHERE data=? AND status='em_visita'", (_hd,))
        if not _cia.empty:
            st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
            section_title("📍 Em visita agora")
            for _,_cr in _cia.iterrows():
                st.markdown(f"<div style='background:#0a1f0a;border:1px solid #22c55e33;border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px'><div style='width:8px;height:8px;background:#22c55e;border-radius:50%'></div><div><div style='color:#ddd;font-size:13px;font-weight:600'>👤 {_cr['funcionario'].split('.')[0].capitalize()}</div><div style='color:#555;font-size:12px'>🏪 {_cr['mercado']} · desde {_cr['hora_entrada']}</div></div></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
        section_title("📈 Comparativo semanal")
        _dl=["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
        def _pd(df):
            if df.empty or "_d" not in df.columns: return [0]*7
            return [len(df[df["_d"]==(_is+timedelta(days=_di))]) for _di in range(7)]
        st.bar_chart(pd.DataFrame({"Semana atual":_pd(_rs),"Anterior":_pd(_rant)},index=_dl))
        _ta=sum(_pd(_rs)); _tb=sum(_pd(_rant))
        _sc1,_sc2,_sc3=st.columns(3)
        _sc1.metric("Semana atual",_ta); _sc2.metric("Semana anterior",_tb); _sc3.metric("Variação",f"{_ta-_tb:+d}")
        _nl=db_read("SELECT COUNT(*) as t FROM chat WHERE tipo='funcionario' AND lido=0").iloc[0]["t"]
        if _nl>0: st.warning(f"💬 **{int(_nl)}** mensagem(ns) não lida(s) no Chat.")

    # ── FUNCIONÁRIOS ──────────────────────────────────────

    elif menu == "Funcionários":
        page_header("Gestão", "Funcionários")

        if "exp_cad_func" not in st.session_state: st.session_state["exp_cad_func"] = False
        if st.button(("🔼 Cadastrar novo funcionário" if st.session_state["exp_cad_func"] else "➕ Cadastrar novo funcionário"), key="btn_exp_cad_func"):
            st.session_state["exp_cad_func"] = not st.session_state["exp_cad_func"]
            st.rerun()
        if st.session_state["exp_cad_func"]:
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
                    db_exec("SELECT usuario FROM usuarios WHERE usuario=?", (login,))
                    if c.fetchone():
                        st.error(f"Login '{login}' já existe.")
                    else:
                        db_exec("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone) VALUES(?,?,?,?,?)",
                                  (login,"elkam","funcionario",1,tel_novo.strip()))
                        # committed by db_exec
                        st.success(f"✅ Criado! Login: **{login}** · Senha: **elkam**")
                        st.rerun()

        section_title("Funcionários cadastrados")
        funcs = db_read("SELECT usuario, telefone FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")

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
                        _txt_enc = urllib.parse.quote(msg_wa)
                        # wa.me funciona no celular; web.whatsapp.com funciona no PC
                        wa_url    = f"https://wa.me/55{tel_func}?text={_txt_enc}"
                        wa_url_pc = f"https://web.whatsapp.com/send?phone=55{tel_func}&text={_txt_enc}"
                        st.markdown(
                            f"""<div style='display:flex;gap:6px'>
                            <a href='{wa_url}' target='_blank' rel='noopener noreferrer' style='flex:1'>
                                <button style='background:#25D366;color:#fff;border:none;
                                border-radius:8px;padding:8px 10px;font-size:11px;
                                font-weight:600;cursor:pointer;width:100%'>
                                📲 Celular</button></a>
                            <a href='{wa_url_pc}' target='_blank' rel='noopener noreferrer' style='flex:1'>
                                <button style='background:#128C7E;color:#fff;border:none;
                                border-radius:8px;padding:8px 10px;font-size:11px;
                                font-weight:600;cursor:pointer;width:100%'>
                                💻 PC</button></a>
                            </div>""",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            "<div style='color:#333;font-size:11px;padding:10px 0'>Sem telefone</div>",
                            unsafe_allow_html=True)
                with col_r:
                    if st.button("🔑 Resetar senha", key=f"reset_{login_func}"):
                        db_exec("UPDATE usuarios SET senha='elkam', primeiro_acesso=1 WHERE usuario=?",
                                  (login_func,))
                        # committed by db_exec
                        st.success(f"Senha de **{login_func}** resetada.")
                        st.rerun()
                with col_e:
                    if st.button("🗑️", key=f"del_{login_func}"):
                        st.session_state[f"confirm_del_func_{login_func}"] = True
                        st.rerun()

                # Confirmação antes de excluir
                if st.session_state.get(f"confirm_del_func_{login_func}", False):
                    st.warning(f"⚠️ Excluir **{login_func}**? Agenda e chat serão removidos. Relatórios serão mantidos como *(ex func)*.")
                    _cd1, _cd2 = st.columns(2)
                    with _cd1:
                        if st.button("✅ Confirmar exclusão", key=f"ok_del_{login_func}", use_container_width=True):
                            fazer_backup()
                            # Remove usuário e dados vinculados (menos relatórios)
                            db_exec("DELETE FROM usuarios WHERE usuario=? AND tipo='funcionario' AND usuario!='superadmin'", (login_func,))
                            db_exec("DELETE FROM agenda WHERE funcionario=?", (login_func,))
                            db_exec("DELETE FROM checkin WHERE funcionario=?", (login_func,))
                            db_exec("DELETE FROM chat WHERE remetente=?", (login_func,))
                            # Marca relatórios como ex-funcionário (não apaga)
                            db_exec("UPDATE relatorio SET funcionario=? WHERE funcionario=?",
                                      (f"{login_func} (ex)", login_func))
                            st.session_state.pop(f"confirm_del_func_{login_func}", None)
                            st.success(f"✅ {login_func} excluído. Relatórios preservados.")
                            st.rerun()
                    with _cd2:
                        if st.button("✖ Cancelar", key=f"cancel_del_{login_func}", use_container_width=True):
                            st.session_state.pop(f"confirm_del_func_{login_func}", None)
                            st.rerun()

    # ── MERCADOS ──────────────────────────────────────────

    elif menu == "Mercados":
        page_header("Cadastro", "Mercados")

        if "exp_novo_merc" not in st.session_state: st.session_state["exp_novo_merc"] = False
        if st.button(("🔼 Novo mercado" if st.session_state["exp_novo_merc"] else "➕ Novo mercado"), key="btn_exp_novo_merc"):
            st.session_state["exp_novo_merc"] = not st.session_state["exp_novo_merc"]
            st.rerun()
        if st.session_state["exp_novo_merc"]:
            cm, ce = st.columns(2)
            with cm: mercado  = st.text_input("Nome do mercado")
            with ce: endereco = st.text_input("Endereço")
            logo_up = st.file_uploader("🖼️ Logo do mercado (opcional)", type=["jpg","jpeg","png"], key="logo_new")
            if st.button("Cadastrar mercado"):
                if not mercado.strip() or not endereco.strip():
                    st.warning("Preencha nome e endereço.")
                else:
                    db_exec("SELECT mercado FROM mercados WHERE endereco=?", (endereco.strip(),))
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
                            db_exec("INSERT INTO mercados (mercado,endereco,logo) VALUES(?,?,?)",
                                      (mercado.strip(), endereco.strip(), logo_path))
                            # committed by db_exec
                            st.success("✅ Mercado cadastrado!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

        section_title("Lista de mercados")
        mdf = db_read("SELECT id, mercado, endereco, logo FROM mercados")

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
                        db_exec("DELETE FROM mercados WHERE id=?", (int(row["id"]),))
                        db_exec("DELETE FROM agenda WHERE mercado=?", (row["mercado"],))
                        # committed by db_exec
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
                                db_exec("UPDATE mercados SET mercado=?,endereco=?,logo=? WHERE id=?",
                                          (novo_nome.strip(), novo_end.strip(), logo_path, int(row["id"])))
                                if novo_nome.strip() != nome_antigo:
                                    db_exec("UPDATE agenda SET mercado=? WHERE mercado=?",
                                              (novo_nome.strip(), nome_antigo))
                                # committed by db_exec
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

        funcs_ag = db_read("SELECT usuario FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")
        mercs_ag = db_read("SELECT mercado FROM mercados")
        prods_cad = db_read("SELECT DISTINCT produto FROM produtos")

        if "exp_add_agenda" not in st.session_state: st.session_state["exp_add_agenda"] = False
        if st.button(("🔼 Adicionar item à agenda" if st.session_state["exp_add_agenda"] else "➕ Adicionar item à agenda"), key="btn_exp_add_agenda"):
            st.session_state["exp_add_agenda"] = not st.session_state["exp_add_agenda"]
            st.rerun()
        if st.session_state["exp_add_agenda"]:
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
                            dup = conn.cursor().execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                (fs, ds, ms, ps.strip())).fetchone()[0]
                            if dup > 0:
                                st.warning("⚠️ Produto já existe nesse dia/mercado.")
                            else:
                                db_exec("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                          (fs, ds, ms, ps.strip()))
                                # Salva produto no catálogo se for novo
                                if ps.strip() not in lista_prod:
                                    dup_p = conn.cursor().execute("SELECT COUNT(*) FROM produtos WHERE produto=?", (ps.strip(),)).fetchone()[0]
                                    if dup_p == 0:
                                        db_exec("INSERT INTO produtos (mercado,produto) VALUES(?,?)", (ms, ps.strip()))
                                # committed by db_exec
                                st.success(f"✅ {ps.strip()} adicionado — {ms} / {ds}")
                                st.rerun()
                with cb2:
                    # Replicar dia inteiro de outro dia
                    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                    dia_orig = st.selectbox("Replicar do dia", [d for d in DIAS_SEMANA if d != ds], key="ag_rep_dia")
                    if st.button("📋 Replicar dia", key="ag_rep"):
                        items = db_read(
                            "SELECT mercado,produto FROM agenda WHERE funcionario=? AND dia=?",
                            (fs, dia_orig))
                        if items.empty:
                            st.warning(f"Nenhum item em {dia_orig} para {fs}.")
                        else:
                            ins = 0
                            for _, r in items.iterrows():
                                dup = conn.cursor().execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                    (fs, ds, r["mercado"], r["produto"])).fetchone()[0]
                                if dup == 0:
                                    db_exec("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (fs, ds, r["mercado"], r["produto"]))
                                    ins += 1
                            # committed by db_exec
                            st.success(f"✅ {ins} item(ns) replicado(s) de {dia_orig} para {ds}!")
                            st.rerun()

        if "exp_copy_ag" not in st.session_state: st.session_state["exp_copy_ag"] = False
        if st.button(("🔼 Copiar agenda" if st.session_state["exp_copy_ag"] else "🔁 Copiar agenda"), key="btn_exp_copy_ag"):
            st.session_state["exp_copy_ag"] = not st.session_state["exp_copy_ag"]
            st.rerun()
        if st.session_state["exp_copy_ag"]:
            if funcs_ag.empty:
                st.warning("Nenhum funcionário.")
            else:
                lista = funcs_ag["usuario"].tolist()
                co1, co2 = st.columns(2)
                with co1: fo = st.selectbox("Copiar DE", lista, key="cp_de")
                with co2: fd = st.selectbox("Copiar PARA", lista, key="cp_para")
                ag_orig = db_read("SELECT dia,mercado,produto FROM agenda WHERE funcionario=?", (fo,))
                if ag_orig.empty:
                    st.warning(f"'{fo}' não tem agenda.")
                else:
                    st.dataframe(ag_orig, use_container_width=True, hide_index=True)
                    apagar = st.checkbox("Substituir agenda atual do destino", value=True, key="cp_apagar")
                    st.markdown(
                        f"<div style='background:#1a0800;border:1px solid #f59e0b33;border-radius:8px;"
                        f"padding:10px 14px;margin:8px 0;color:#888;font-size:12px'>"
                        f"Vai copiar <b style='color:#f59e0b'>{len(ag_orig)} item(ns)</b> de "
                        f"<b style='color:#ddd'>{fo}</b> → <b style='color:#ddd'>{fd}</b>"
                        f"{'  ·  <span style=\'color:#ff4444\'>agenda atual será apagada</span>' if apagar else ''}"
                        f"</div>",
                        unsafe_allow_html=True)
                    if st.button("✅ Confirmar cópia de agenda", key="cp_confirm", use_container_width=True):
                        if fo == fd:
                            st.error("Origem e destino iguais.")
                        else:
                            if apagar:
                                db_exec("DELETE FROM agenda WHERE funcionario=?", (fd,))
                            ins = 0
                            for _, r in ag_orig.iterrows():
                                dup = conn.cursor().execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                    (fd, r["dia"], r["mercado"], r["produto"])).fetchone()[0]
                                if dup == 0:
                                    db_exec("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (fd, r["dia"], r["mercado"], r["produto"]))
                                    ins += 1
                            st.success(f"✅ {ins} tarefas copiadas para '{fd}'!")
                            st.session_state["exp_copy_ag"] = False
                            st.rerun()

        if "exp_imp_ag" not in st.session_state: st.session_state["exp_imp_ag"] = False
        if st.button(("🔼 Importar Agenda CSV" if st.session_state["exp_imp_ag"] else "📂 Importar Agenda CSV"), key="btn_exp_imp_ag"):
            st.session_state["exp_imp_ag"] = not st.session_state["exp_imp_ag"]
            st.rerun()
        if st.session_state["exp_imp_ag"]:
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
                            dup = conn.cursor().execute("SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                (func_imp, dia_v, merc_v, prod_v)).fetchone()[0]
                            if dup == 0:
                                db_exec("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                          (func_imp, dia_v, merc_v, prod_v))
                                # Salva template
                                db_exec("INSERT INTO agenda_template (nome_empresa,funcionario,dia,mercado,produto) VALUES(?,?,?,?,?)",
                                          (nome_empresa_imp.strip() or "Sem nome", func_imp, dia_v, merc_v, prod_v))
                                ins += 1
                            else:
                                dup_count += 1
                        # committed by db_exec
                        st.success(f"✅ {ins} item(ns) importado(s) para **{func_imp}**!"
                                   + (f" ({dup_count} duplicado(s) ignorado(s))" if dup_count else ""))
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro ao ler CSV: {e}")

        # ══════════════════════════════════════════
        # AGENDAS POR FUNCIONÁRIO
        # ══════════════════════════════════════════
        st.markdown("<hr style='border-color:#1c1c1c;margin:28px 0 20px'>", unsafe_allow_html=True)
        section_title("📋 Agendas por funcionário")

        _all_funcs = db_read("SELECT usuario FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")
        _mercs_list = db_read("SELECT mercado FROM mercados")["mercado"].tolist() if not db_read("SELECT mercado FROM mercados").empty else []
        _prods_list = db_read("SELECT DISTINCT produto FROM produtos")["produto"].tolist() if not db_read("SELECT DISTINCT produto FROM produtos").empty else []

        if _all_funcs.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            for _func_u in _all_funcs["usuario"].tolist():
                _ag_f = db_read("SELECT rowid, dia, mercado, produto FROM agenda WHERE funcionario=?", (_func_u,))
                _n_items = len(_ag_f)

                # ── CABEÇALHO DO CARD DO FUNCIONÁRIO ──
                _fk = f"ag_open_{_func_u}"
                if _fk not in st.session_state: st.session_state[_fk] = False

                _hcol1, _hcol2, _hcol3 = st.columns([6, 2, 2])
                with _hcol1:
                    st.markdown(
                        f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:12px;"
                        f"padding:14px 18px;margin:6px 0'>"
                        f"<span style='color:#ff2b2b;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px'>Funcionário</span><br>"
                        f"<span style='color:#fff;font-size:16px;font-weight:800'>"
                        f"👤 {_func_u.split('.')[0].capitalize() + ' ' + (_func_u.split('.')[1].capitalize() if '.' in _func_u else '')}"
                        f"</span>"
                        f"<span style='color:#444;font-size:12px;margin-left:10px'>{_n_items} item(ns)</span>"
                        f"</div>",
                        unsafe_allow_html=True)
                with _hcol2:
                    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
                    _btn_lbl = "🔼 Fechar" if st.session_state[_fk] else "📋 Ver agenda"
                    if st.button(_btn_lbl, key=f"toggle_{_func_u}", use_container_width=True):
                        st.session_state[_fk] = not st.session_state[_fk]
                        st.rerun()
                with _hcol3:
                    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
                    if st.button("⚠️ Limpar tudo", key=f"clr_{_func_u}", use_container_width=True):
                        st.session_state[f"confirm_clr_{_func_u}"] = True
                        st.rerun()

                # Confirmação de limpeza
                if st.session_state.get(f"confirm_clr_{_func_u}", False):
                    st.warning(f"⚠️ Apagar TODA a agenda de **{_func_u}**? Irreversível.")
                    _cc1, _cc2 = st.columns(2)
                    with _cc1:
                        if st.button("✅ Confirmar limpeza", key=f"ok_clr_{_func_u}", use_container_width=True):
                            fazer_backup()
                            db_exec("DELETE FROM agenda WHERE funcionario=?", (_func_u,))
                            st.session_state[f"confirm_clr_{_func_u}"] = False
                            st.success(f"Agenda de {_func_u} limpa!")
                            st.rerun()
                    with _cc2:
                        if st.button("✖ Cancelar", key=f"cancel_clr_{_func_u}", use_container_width=True):
                            st.session_state[f"confirm_clr_{_func_u}"] = False
                            st.rerun()

                if st.session_state[_fk]:
                    # ── CONTEÚDO DA AGENDA ──
                    st.markdown("<div style='background:#0d0d0d;border:1px solid #1a1a1a;border-radius:12px;padding:16px 18px;margin-bottom:8px'>", unsafe_allow_html=True)

                    if _ag_f.empty:
                        st.markdown("<div style='color:#333;font-size:13px;text-align:center;padding:12px'>Nenhum item na agenda.</div>", unsafe_allow_html=True)
                    else:
                        for _dia_e in DIAS_SEMANA:
                            _df_d = _ag_f[_ag_f["dia"] == _dia_e]
                            if _df_d.empty: continue
                            st.markdown(
                                f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;"
                                f"letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 6px'>"
                                f"📅 {_dia_e}</div>",
                                unsafe_allow_html=True)
                            for _mg in _df_d["mercado"].unique():
                                _pgs = _df_d[_df_d["mercado"]==_mg]
                                st.markdown(
                                    f"<div style='color:#888;font-size:12px;padding:4px 0 2px 10px;"
                                    f"border-left:2px solid #ff2b2b33'>🏪 <b style='color:#ccc'>{_mg}</b></div>",
                                    unsafe_allow_html=True)
                                for _, _row in _pgs.iterrows():
                                    _pc1, _pc2 = st.columns([8, 1])
                                    with _pc1:
                                        st.markdown(
                                            f"<div style='color:#666;font-size:12px;padding:3px 0 3px 20px'>"
                                            f"· {_row['produto']}</div>",
                                            unsafe_allow_html=True)
                                    with _pc2:
                                        if st.button("🗑️", key=f"del_ag_{_row['rowid']}_{_func_u}",
                                                     help=f"Remover {_row['produto']}"):
                                            db_exec("DELETE FROM agenda WHERE rowid=?", (int(_row["rowid"]),))
                                            st.rerun()

                    # ── ADICIONAR ITEM INDIVIDUAL ──
                    st.markdown("<hr style='border-color:#1c1c1c;margin:14px 0'>", unsafe_allow_html=True)
                    _ak = f"ag_add_open_{_func_u}"
                    if _ak not in st.session_state: st.session_state[_ak] = False
                    if st.button(("🔼 Fechar" if st.session_state[_ak] else "➕ Adicionar item"), key=f"add_toggle_{_func_u}", use_container_width=True):
                        st.session_state[_ak] = not st.session_state[_ak]
                        st.rerun()

                    if st.session_state[_ak]:
                        _ia1, _ia2 = st.columns(2)
                        with _ia1:
                            _ds2 = st.selectbox("Dia", DIAS_SEMANA, key=f"ia_dia_{_func_u}")
                        with _ia2:
                            _ms2 = st.selectbox("Mercado", _mercs_list if _mercs_list else ["(sem mercados)"], key=f"ia_merc_{_func_u}")
                        _pl2 = _prods_list + ["➕ Novo produto..."]
                        _psel2 = st.selectbox("Produto", _pl2, key=f"ia_prod_{_func_u}")
                        if _psel2 == "➕ Novo produto...":
                            _ps2 = st.text_input("Nome do novo produto", key=f"ia_prod_new_{_func_u}")
                        else:
                            _ps2 = _psel2
                        if st.button("✅ Confirmar adição", key=f"ia_add_{_func_u}", use_container_width=True):
                            if not _ps2.strip():
                                st.warning("Informe o produto.")
                            elif not _mercs_list:
                                st.warning("Cadastre um mercado primeiro.")
                            else:
                                _dup = conn.cursor().execute(
                                    "SELECT COUNT(*) FROM agenda WHERE funcionario=? AND dia=? AND mercado=? AND produto=?",
                                    (_func_u, _ds2, _ms2, _ps2.strip())).fetchone()[0]
                                if _dup > 0:
                                    st.warning("⚠️ Item já existe nesse dia/mercado.")
                                else:
                                    db_exec("INSERT INTO agenda (funcionario,dia,mercado,produto) VALUES(?,?,?,?)",
                                              (_func_u, _ds2, _ms2, _ps2.strip()))
                                    if _ps2.strip() not in _prods_list:
                                        db_exec("INSERT OR IGNORE INTO produtos (mercado,produto) VALUES(?,?)",
                                                  (_ms2, _ps2.strip()))
                                    st.success(f"✅ Adicionado: {_ps2.strip()} — {_ms2} / {_ds2}")
                                    st.session_state[_ak] = False
                                    st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)

    # ── RELATÓRIOS ────────────────────────────────────────

    elif menu == "Relatórios":
        page_header("Acompanhamento", "Relatório Completo")

        rel_all = db_read("SELECT rowid, * FROM relatorio")

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
                        db_exec("DELETE FROM relatorio WHERE rowid=?", (rid,))
                    # auto-committed; st.success("Excluído(s)."); st.rerun()
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

        rel = db_read("SELECT * FROM relatorio WHERE foto != ''")
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

        if "exp_foto_prod" not in st.session_state: st.session_state["exp_foto_prod"] = False
        if st.button(("🔼 Adicionar foto de produto" if st.session_state["exp_foto_prod"] else "➕ Adicionar foto de produto"), key="btn_exp_foto_prod"):
            st.session_state["exp_foto_prod"] = not st.session_state["exp_foto_prod"]
            st.rerun()
        if st.session_state["exp_foto_prod"]:
            pf1, pf2 = st.columns(2)
            with pf1:
                prods_todos = db_read("SELECT DISTINCT produto FROM produtos")
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
                    ex = conn.cursor().execute("SELECT id FROM produto_fotos WHERE produto=?", (p_nome_foto.strip(),)).fetchone()
                    if ex:
                        db_exec("UPDATE produto_fotos SET foto=? WHERE produto=?", (fp_path, p_nome_foto.strip()))
                    else:
                        db_exec("INSERT INTO produto_fotos (produto,foto) VALUES(?,?)", (p_nome_foto.strip(), fp_path))
                        if p_nome_foto.strip() not in lista_p:
                            db_exec("INSERT INTO produtos (mercado,produto) VALUES('',?)", (p_nome_foto.strip(),))
                    # committed by db_exec
                    st.success(f"✅ Foto de '{p_nome_foto}' salva!")
                    st.rerun()

        section_title("Produtos com foto de referência")
        pf_df = db_read("SELECT * FROM produto_fotos")
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

        # Apaga mensagens com mais de 24h
        db_exec("DELETE FROM chat WHERE datetime(data||' '||hora) < datetime('now','-24 hours')")

        db_exec("UPDATE chat SET lido=1 WHERE tipo='funcionario'")
        # committed by db_exec

        funcs_ch = db_read("SELECT usuario FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")

        if funcs_ch.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            func_sel = st.selectbox("Conversa com:", funcs_ch["usuario"].tolist())

            hist = db_read(
                "SELECT * FROM chat WHERE (remetente=? AND tipo='funcionario') "
                "OR (remetente=? AND tipo='admin') ORDER BY id", (func_sel, func_sel))

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
                        db_exec("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                                  (str(now.date()), now.strftime("%H:%M"), func_sel, "admin", msg_a.strip(), 1))
                        # auto-committed; st.rerun()

    # ── CONFIGURAÇÕES ─────────────────────────────────────

    elif menu == "⚙️ Configurações":
        apenas_admin()
        page_header("Sistema", "Configurações")

        # ── ALTERAR SENHA ──
        section_title("🔐 Alterar senha")
        _csp1, _csp2 = st.columns(2)
        with _csp1:
            _cfg_nova = st.text_input("Nova senha", type="password", key="cfg_pw_nova",
                                      placeholder="Nova senha...")
        with _csp2:
            _cfg_conf = st.text_input("Confirmar senha", type="password", key="cfg_pw_conf",
                                      placeholder="Confirme...")
        if st.button("💾 Salvar senha", key="cfg_pw_save", use_container_width=False):
            if not _cfg_nova or not _cfg_conf:
                st.error("Preencha os dois campos.")
            elif _cfg_nova != _cfg_conf:
                st.error("As senhas não coincidem.")
            elif len(_cfg_nova) < 4:
                st.error("Mínimo 4 caracteres.")
            else:
                db_exec("UPDATE usuarios SET senha=? WHERE usuario=?", (_cfg_nova, usuario))
                st.success("✅ Senha alterada com sucesso!")

        st.markdown("<hr style='border-color:#1c1c1c;margin:24px 0'>", unsafe_allow_html=True)

        # ── EMAIL DE RECUPERAÇÃO ──
        section_title("📧 Email de recuperação do admin")
        admin_row = db_read(
            "SELECT email FROM usuarios WHERE usuario='admin'")
        email_atual = admin_row.iloc[0]["email"] if not admin_row.empty else ""

        col_em, col_sb = st.columns([3,1])
        with col_em:
            novo_email = st.text_input("Email de recuperação", value=email_atual,
                                       placeholder="admin@empresa.com", key="cfg_email")
        with col_sb:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Salvar email"):
                if "@" in novo_email and "." in novo_email:
                    db_exec("UPDATE usuarios SET email=? WHERE tipo='admin'", (novo_email.strip(),))
                    # committed by db_exec
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

        if "exp_smtp" not in st.session_state: st.session_state["exp_smtp"] = False
        if st.button(("🔼 ️ Configurar SMTP" if st.session_state["exp_smtp"] else "⚙ ️ Configurar SMTP"), key="btn_exp_smtp"):
            st.session_state["exp_smtp"] = not st.session_state["exp_smtp"]
            st.rerun()
        if st.session_state["exp_smtp"]:
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

        emp = db_read("SELECT * FROM empresa WHERE id=1")
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
                        db_exec("INSERT INTO empresa (id,nome,descricao,foto,concluida) VALUES(1,?,?,?,0)",
                                  (nome_emp, desc_emp, foto_path))
                    else:
                        db_exec("UPDATE empresa SET nome=?,descricao=?,foto=? WHERE id=1",
                                  (nome_emp, desc_emp, foto_path))
                    # committed by db_exec
                    st.success("Rascunho salvo!")
            with cb2:
                if st.button("✅ Concluir e publicar"):
                    if not nome_emp.strip() or not desc_emp.strip():
                        st.error("Preencha nome e descrição antes de publicar.")
                    else:
                        if dados is None:
                            db_exec("INSERT INTO empresa (id,nome,descricao,foto,concluida) VALUES(1,?,?,?,1)",
                                      (nome_emp, desc_emp, foto_path))
                        else:
                            db_exec("UPDATE empresa SET nome=?,descricao=?,foto=?,concluida=1 WHERE id=1",
                                      (nome_emp, desc_emp, foto_path))
                        # committed by db_exec
                        st.session_state["editando_empresa"] = False
                        st.success("✅ Apresentação publicada!")
                        st.rerun()

    # ── DESTINATÁRIOS PDF ─────────────────────────────────

    elif menu == "Destinatários":
        page_header("Configuração", "Destinatários do Relatório PDF")
        st.caption("Números que receberão o link do PDF quando o funcionário enviar o relatório.")

        if "exp_add_dest" not in st.session_state: st.session_state["exp_add_dest"] = False
        if st.button(("🔼 Adicionar destinatário" if st.session_state["exp_add_dest"] else "➕ Adicionar destinatário"), key="btn_exp_add_dest"):
            st.session_state["exp_add_dest"] = not st.session_state["exp_add_dest"]
            st.rerun()
        if st.session_state["exp_add_dest"]:
            cd1, cd2 = st.columns(2)
            with cd1: dest_nome = st.text_input("Nome")
            with cd2: dest_tel  = st.text_input("WhatsApp (com DDD, só números)", placeholder="11999998888")
            if st.button("Adicionar"):
                if dest_nome.strip() and dest_tel.strip():
                    db_exec("INSERT INTO destinatarios (nome,telefone) VALUES(?,?)",
                              (dest_nome.strip(), dest_tel.strip()))
                    # committed by db_exec
                    st.success(f"✅ {dest_nome} adicionado!")
                    st.rerun()
                else:
                    st.warning("Preencha nome e telefone.")

        section_title("Lista de destinatários")
        dests = db_read("SELECT * FROM destinatarios")
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
                        db_exec("DELETE FROM destinatarios WHERE id=?", (int(d["id"]),))
                        # auto-committed; st.rerun()

# ═══════════════════════════════════════════════════════
#  FUNCIONÁRIO
# ═══════════════════════════════════════════════════════

else:

    nao_lidas_f = db_read(
        "SELECT COUNT(*) as t FROM chat WHERE remetente=? AND tipo='admin' AND lido=0", (usuario,)).iloc[0]["t"]

    emp_pub = db_read("SELECT * FROM empresa WHERE id=1 AND concluida=1")
    tem_empresa = not emp_pub.empty

    # ── FUNC NAV ──
    if "func_aba" not in st.session_state:
        st.session_state["func_aba"] = "🏠  Início"

    abas_nav = ["🏠  Início", "📋  Agenda"]
    if tem_empresa: abas_nav.append("🏢  Empresa")
    _chat_lbl = f"💬  Chat{'  ●' if nao_lidas_f > 0 else ''}"
    abas_nav.append(_chat_lbl)
    abas_nav.append("⚙️  Config")

    # Garante que func_aba seja válido
    if st.session_state["func_aba"] not in abas_nav:
        # chat label pode ter mudado (● sumiu), normaliza
        if "💬" in st.session_state["func_aba"]:
            st.session_state["func_aba"] = _chat_lbl
        else:
            st.session_state["func_aba"] = "🏠  Início"

    # Botões mobile — só aparecem no celular (CSS esconde em desktop)
    st.markdown('<div class="mobile-topnav">', unsafe_allow_html=True)
    _fn1, _fn2, _fn3, _fn4 = st.columns(4)
    with _fn1:
        if st.button("🏠\nInício",  key="fn_ini",  use_container_width=True):
            st.session_state["func_aba"] = "🏠  Início"; st.rerun()
    with _fn2:
        if st.button("📋\nAgenda",  key="fn_ag",   use_container_width=True):
            st.session_state["func_aba"] = "📋  Agenda"; st.rerun()
    with _fn3:
        _chat_ico = "💬●\nChat" if nao_lidas_f > 0 else "💬\nChat"
        if st.button(_chat_ico,      key="fn_chat", use_container_width=True):
            st.session_state["func_aba"] = _chat_lbl; st.rerun()
    with _fn4:
        if st.button("⚙️\nConfig",  key="fn_cfg",  use_container_width=True):
            st.session_state["func_aba"] = "⚙️  Config"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar: sair + botões de navegação (desktop)
    with st.sidebar:
        if st.button("🚪 Sair", use_container_width=True, key="func_sair"):
            for _k in list(st.session_state.keys()):
                del st.session_state[_k]
            st.rerun()
        st.markdown("<hr style='border-color:#1c1c1c;margin:10px 0'>", unsafe_allow_html=True)
        _ficons = {"🏠  Início":"🏠", "📋  Agenda":"📋", "🏢  Empresa":"🏢",
                   "⚙️  Config":"⚙️"}
        for _fopt in abas_nav:
            _fi = _ficons.get(_fopt, "💬")
            _fat = st.session_state["func_aba"] == _fopt
            if st.button(f"{_fi}  {_fopt.strip()}", key=f"fn_sb_{_fopt}", use_container_width=True):
                st.session_state["func_aba"] = _fopt
                st.rerun()

    aba = st.session_state["func_aba"]

    # ── INÍCIO / DASHBOARD FUNCIONÁRIO ──

    if aba == "🏠  Início":
        nome_exib_d = usuario.split(".")[0].capitalize()
        page_header(f"Olá, {nome_exib_d}! 👋", "Painel do dia")
        _hj = str(date.today())
        _ds = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"][date.today().weekday()]
        _trf = db_read("SELECT * FROM agenda WHERE funcionario=?", (usuario,))
        _md = _trf[_trf["dia"]==_ds]["mercado"].unique().tolist() if not _trf.empty else []
        _rh2 = db_read("SELECT * FROM relatorio WHERE funcionario=? AND data=?", (usuario,_hj))
        _vis = _rh2["mercado"].nunique() if not _rh2.empty else 0
        _fotos_n = len(_rh2[_rh2["foto"]!=""]) if not _rh2.empty else 0
        _falta_n = len(_rh2[_rh2["status"]=="falta"]) if not _rh2.empty else 0
        _ci2 = db_read("SELECT * FROM checkin WHERE funcionario=? AND data=?", (usuario,_hj))

        _m1,_m2,_m3,_m4 = st.columns(4)
        _m1.metric("Visitas hoje", f"{_vis}/{len(_md)}")
        _m2.metric("Fotos enviadas", _fotos_n)
        _m3.metric("Produtos em falta", _falta_n)
        _m4.metric("Check-ins", len(_ci2))

        if len(_md) > 0:
            _p = int(_vis/len(_md)*100)
            _prog_html = (f"<div style='margin:16px 0 8px'><div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
                         f"<span style='color:#888;font-size:12px'>Progresso da rota</span>"
                         f"<span style='color:#ff2b2b;font-size:12px;font-weight:700'>{_p}%</span></div>"
                         f"<div style='background:#1a1a1a;border-radius:8px;height:8px'>"
                         f"<div style='background:linear-gradient(90deg,#ff2b2b,#ff6b6b);width:{_p}%;height:8px;border-radius:8px'></div></div></div>")
            st.markdown(_prog_html, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1c1c1c;margin:18px 0'>", unsafe_allow_html=True)

        _pend = [m for m in _md if m not in (_rh2["mercado"].tolist() if not _rh2.empty else [])]
        if _pend:
            _prx = _pend[0]
            _inf = db_read("SELECT endereco FROM mercados WHERE mercado=?", (_prx,))
            _end = _inf.iloc[0]["endereco"] if not _inf.empty else ""
            _mp = ("https://www.google.com/maps/search/" + _end.replace(' ','+')) if _end else "#"
            _prx_html = (f"<div style='background:linear-gradient(135deg,#140000,#1e0000);"
                        f"border:1.5px solid #ff2b2b44;border-radius:16px;padding:18px 20px;margin-bottom:14px'>"
                        f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;letter-spacing:2px;"
                        f"text-transform:uppercase;margin-bottom:6px'>📍 Próxima visita</div>"
                        f"<div style='color:#fff;font-size:18px;font-weight:900'>{_prx}</div>"
                        f"<div style='color:#444;font-size:12px;margin-top:4px'>{_end}</div></div>")
            st.markdown(_prx_html, unsafe_allow_html=True)
            _pb1, _pb2 = st.columns(2)
            with _pb1:
                if _end:
                    st.markdown(f"<a href='{_mp}' target='_blank'><button style='width:100%;background:#1a1a1a;color:#3b82f6;border:1px solid #1e3a5f;border-radius:10px;padding:12px;font-size:13px;font-weight:600;cursor:pointer'>🗺️ Ver rota</button></a>", unsafe_allow_html=True)
            with _pb2:
                if st.button("📷 Registrar visita", key="dash_reg", use_container_width=True):
                    st.session_state["func_aba"] = "📋  Agenda"
                    st.rerun()
        elif _md:
            st.markdown("<div style='background:#0a2b14;border:1px solid #22c55e33;border-radius:14px;padding:20px;text-align:center'><div style='font-size:36px'>🏆</div><div style='color:#22c55e;font-size:16px;font-weight:800;margin-top:8px'>Rota concluída!</div></div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1c1c1c;margin:18px 0'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#444;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px'>📅 Agenda de hoje</div>", unsafe_allow_html=True)
        for _m in _md:
            _ok = _m in (_rh2["mercado"].tolist() if not _rh2.empty else [])
            _ico = "✅" if _ok else "⏳"
            _stl = "text-decoration:line-through;color:#555" if _ok else "color:#ddd"
            st.markdown(f"<div style='background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:11px 16px;margin-bottom:7px;display:flex;align-items:center;gap:12px'><span>{_ico}</span><span style='{_stl};font-size:14px;font-weight:600'>{_m}</span></div>", unsafe_allow_html=True)

        if not _rh2.empty and not _ci2.empty:
            _ul = _ci2.sort_values("id",ascending=False).iloc[0]
            _hs = " · Saída "+str(_ul.get("hora_saida","")) if _ul.get("hora_saida") else ""
            st.markdown(f"<div style='margin-top:14px;background:#111;border:1px solid #1c1c1c;border-radius:10px;padding:13px 16px'><div style='color:#444;font-size:10px;text-transform:uppercase;letter-spacing:1px'>Última atividade</div><div style='color:#ddd;font-size:13px;font-weight:600;margin-top:4px'>🏪 {_ul.get('mercado','—')}</div><div style='color:#555;font-size:11px;margin-top:2px'>Entrada {_ul.get('hora_entrada','—')}{_hs}</div></div>", unsafe_allow_html=True)

    # ── CONFIG FUNCIONÁRIO ──

    elif "⚙️  Config" in aba:
        page_header("Configurações", "Minha conta")
        section_title("🔐 Alterar senha")
        _fcs1, _fcs2 = st.columns(2)
        with _fcs1: _fc_nova = st.text_input("Nova senha", type="password", key="fc_ns", placeholder="Nova senha...")
        with _fcs2: _fc_conf = st.text_input("Confirmar", type="password", key="fc_cs", placeholder="Confirme...")
        if st.button("💾 Salvar senha", use_container_width=True, key="fc_save"):
            if not _fc_nova or not _fc_conf: st.error("Preencha os dois campos.")
            elif _fc_nova != _fc_conf: st.error("Senhas não coincidem.")
            elif len(_fc_nova) < 4: st.error("Mínimo 4 caracteres.")
            else:
                db_exec("UPDATE usuarios SET senha=? WHERE usuario=?", (_fc_nova, usuario))
                st.success("✅ Senha alterada!")

    # ── EMPRESA (FUNCIONÁRIO) ──

    elif aba == "🏢  Empresa" and tem_empresa:
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

        tarefas = db_read("SELECT * FROM agenda WHERE funcionario=?", (usuario,))

        if tarefas.empty:
            st.info("Nenhuma agenda cadastrada ainda. Aguarde seu supervisor.")
            st.stop()

        DIAS_SEMANA_F = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
        dias_present = [d for d in DIAS_SEMANA_F if d in tarefas["dia"].values]

        # ── TABELA VISUAL DA SEMANA ──
        estrutura = {}
        for _, r in tarefas.iterrows():
            estrutura.setdefault(r["mercado"], {}).setdefault(r["dia"], []).append(r["produto"])

        # ── TABELA VISUAL (desktop) / CARDS (mobile) ──
        tabela_html = "<div class='tab-ag-wrap'><table class='tab-ag'><thead><tr><th>Mercado</th>"
        for d in dias_present:
            tabela_html += f"<th>{d}</th>"
        tabela_html += "</tr></thead><tbody>"
        for merc_t in estrutura:
            tabela_html += f"<tr><td><span class='mn'>🏪 {merc_t}</span></td>"
            for d in dias_present:
                pp = estrutura[merc_t].get(d,[])
                if pp:
                    tabela_html += "<td>" + "".join(f"<span class='pi'>· {p}</span>" for p in pp) + "</td>"
                else:
                    tabela_html += '<td class="vz"></td>'
            tabela_html += "</tr>"
        tabela_html += "</tbody></table></div>"

        # Cards mobile por dia
        mobile_html = "<div class='agenda-semana-mobile'>"
        for d in dias_present:
            mercs_d = tarefas[tarefas["dia"]==d]["mercado"].unique()
            mobile_html += (f"<div style='background:#111;border:1px solid #1c1c1c;"
                            f"border-radius:12px;padding:14px 16px;margin-bottom:10px'>")
            mobile_html += (f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;"
                            f"letter-spacing:2px;text-transform:uppercase;margin-bottom:8px'>📅 {d}</div>")
            for m in mercs_d:
                pp = estrutura.get(m,{}).get(d,[])
                mobile_html += f"<div style='color:#ddd;font-size:13px;font-weight:600;margin-bottom:2px'>🏪 {m}</div>"
                for p in pp:
                    mobile_html += f"<div style='color:#555;font-size:12px;padding-left:14px'>· {p}</div>"
            mobile_html += "</div>"
        mobile_html += "</div>"

        st.markdown(tabela_html + mobile_html, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        section_title("Detalhes do dia")

        dia_sel   = st.selectbox("Selecione o dia", dias_present)
        dados_dia = tarefas[tarefas["dia"] == dia_sel]

        for merc in dados_dia["mercado"].unique():
            merc_info = db_read("SELECT endereco, logo FROM mercados WHERE mercado=?", (merc,))
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
            checkin_hoje = db_read(
                "SELECT * FROM checkin WHERE funcionario=? AND mercado=? AND data=?", (usuario, merc, str(date.today())))

            if checkin_hoje.empty:
                if st.button(f"📍 Fazer check-in em {merc}", key=f"cin_{merc}_{dia_sel}"):
                    now = datetime.now()
                    db_exec("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                              (str(date.today()), now.strftime("%H:%M"), "", usuario, merc, "em_visita"))
                    # committed by db_exec
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
                foto_ref = db_read(
                    "SELECT foto FROM produto_fotos WHERE produto=? LIMIT 1", (prod_nome,))
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

                # Câmera / upload — só abre quando o usuário clica
                chave_mostrar_cam = f"mostrar_cam_{merc}_{dia_sel}_{i}"
                if not st.session_state.get(chave_mostrar_cam, False):
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("📸 Tirar foto", key=f"abrir_cam_{merc}_{dia_sel}_{i}",
                                     use_container_width=True):
                            st.session_state[chave_mostrar_cam] = "cam"
                            st.rerun()
                    with bc2:
                        if st.button("📁 Galeria", key=f"abrir_arq_{merc}_{dia_sel}_{i}",
                                     use_container_width=True):
                            st.session_state[chave_mostrar_cam] = "arq"
                            st.rerun()
                else:
                    modo_ativo = st.session_state[chave_mostrar_cam]
                    if st.button("✖ Fechar câmera", key=f"fechar_cam_{merc}_{dia_sel}_{i}"):
                        st.session_state[chave_mostrar_cam] = False
                        st.rerun()

                    if modo_ativo == "cam":
                        fc = st.camera_input("", key=f"cam_p_{merc}_{dia_sel}_{i}",
                                             label_visibility="collapsed")
                        if fc:
                            # Salva com timestamp na imagem (anti-fraude)
                            from PIL import Image, ImageDraw, ImageFont
                            import io
                            img = Image.open(fc)
                            draw = ImageDraw.Draw(img)
                            ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            txt = f"El Kam · {usuario} · {ts}"
                            # Fundo semi-transparente na marca d'água
                            w, h = img.size
                            font_size = max(16, w // 28)
                            try:
                                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                            except:
                                font = ImageFont.load_default()
                            bbox = draw.textbbox((0,0), txt, font=font)
                            tw = bbox[2]-bbox[0]; th2 = bbox[3]-bbox[1]
                            pad = 8
                            x, y = pad, h - th2 - pad*3
                            # sombra
                            draw.rectangle([x-pad, y-pad, x+tw+pad, y+th2+pad],
                                           fill=(0,0,0,160))
                            draw.text((x, y), txt, fill=(255,255,255,255), font=font)
                            buf = io.BytesIO()
                            img.save(buf, format="JPEG", quality=88)
                            with open(nome_foto_prod,"wb") as fp2: fp2.write(buf.getvalue())
                            st.session_state[chave_mostrar_cam] = False
                            st.rerun()
                    else:
                        fa = st.file_uploader("", key=f"arq_p_{merc}_{dia_sel}_{i}",
                                              type=["jpg","jpeg","png"],
                                              label_visibility="collapsed")
                        if fa:
                            from PIL import Image, ImageDraw, ImageFont
                            import io
                            img = Image.open(fa)
                            draw = ImageDraw.Draw(img)
                            ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            txt = f"El Kam · {usuario} · {ts}"
                            w, h = img.size
                            font_size = max(16, w // 28)
                            try:
                                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                            except:
                                font = ImageFont.load_default()
                            bbox = draw.textbbox((0,0), txt, font=font)
                            tw = bbox[2]-bbox[0]; th2 = bbox[3]-bbox[1]
                            pad = 8; x, y = pad, h - th2 - pad*3
                            draw.rectangle([x-pad, y-pad, x+tw+pad, y+th2+pad], fill=(0,0,0,160))
                            draw.text((x, y), txt, fill=(255,255,255,255), font=font)
                            buf = io.BytesIO()
                            img.save(buf, format="JPEG", quality=88)
                            with open(nome_foto_prod,"wb") as fp2: fp2.write(buf.getvalue())
                            st.session_state[chave_mostrar_cam] = False
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

            # Status principal: apenas ocorrência do mercado (sem Abastecido — este vem dos checkboxes)
            _st_key = f"st_{merc}_{dia_sel}"
            _st_opts = ["⚠️  Produto em falta", "❌  Loja fechada", "✅  Tudo abastecido"]
            _st_idx  = st.session_state.get(_st_key+"_idx", 2)

            _sc1, _sc2, _sc3 = st.columns(3)
            with _sc1:
                _active1 = _st_idx == 1
                if st.button(
                    ("🔴 " if _active1 else "") + "❌ Loja fechada",
                    key=f"stbtn_fecha_{merc}_{dia_sel}",
                    use_container_width=True):
                    st.session_state[_st_key+"_idx"] = 1
                    st.rerun()
            with _sc2:
                _active0 = _st_idx == 0
                if st.button(
                    ("🔴 " if _active0 else "") + "⚠️ Produto em falta",
                    key=f"stbtn_falta_{merc}_{dia_sel}",
                    use_container_width=True):
                    st.session_state[_st_key+"_idx"] = 0
                    st.rerun()
            with _sc3:
                _active2 = _st_idx == 2
                if st.button(
                    ("🟢 " if _active2 else "") + "✅ Tudo abastecido",
                    key=f"stbtn_abast_{merc}_{dia_sel}",
                    use_container_width=True):
                    st.session_state[_st_key+"_idx"] = 2
                    st.rerun()

            # Mostra seleção atual
            _status_labels = {0:"⚠️ Produto em falta", 1:"❌ Loja fechada", 2:"✅ Tudo abastecido"}
            _status_cores   = {0:"#2b1f0a", 1:"#2b0a0a", 2:"#0a2b14"}
            _status_borda   = {0:"#f59e0b44", 1:"#ff2b2b44", 2:"#22c55e44"}
            _status_texto   = {0:"#f59e0b", 1:"#ff4444", 2:"#22c55e"}
            st.markdown(
                f"<div style='background:{_status_cores[_st_idx]};border:1px solid {_status_borda[_st_idx]};"
                f"border-radius:8px;padding:8px 14px;margin:8px 0;text-align:center;"
                f"color:{_status_texto[_st_idx]};font-size:13px;font-weight:700'>"
                f"{_status_labels[_st_idx]}</div>",
                unsafe_allow_html=True)

            # Campo de produtos em falta — múltiplos
            prod_faltante = ""
            if _st_idx == 0:
                st.markdown(
                    "<div style='color:#f59e0b;font-size:12px;font-weight:600;margin:10px 0 6px'>"
                    "📦 Quais produtos estão em falta?</div>",
                    unsafe_allow_html=True)
                # Produtos da agenda deste mercado como sugestão
                _prods_merc = prods["produto"].tolist() if not prods.empty else []
                _falta_chk_key = f"falta_chk_{merc}_{dia_sel}"
                if _falta_chk_key not in st.session_state:
                    st.session_state[_falta_chk_key] = []
                # Checkboxes para cada produto do mercado
                _selecionados = []
                for _pp in _prods_merc:
                    _ck = st.checkbox(_pp, key=f"fck_{merc}_{dia_sel}_{_pp}",
                                      value=_pp in st.session_state[_falta_chk_key])
                    if _ck:
                        _selecionados.append(_pp)
                # Campo livre para produto não cadastrado
                _extra = st.text_input("➕ Outro produto (não listado)",
                                       key=f"falta_extra_{merc}_{dia_sel}",
                                       placeholder="Digite o nome do produto...")
                if _extra.strip():
                    _selecionados.append(_extra.strip())
                st.session_state[_falta_chk_key] = _selecionados
                prod_faltante = ", ".join(_selecionados)
                if prod_faltante:
                    st.markdown(
                        f"<div style='background:#1a1000;border:1px solid #f59e0b33;border-radius:8px;"
                        f"padding:8px 12px;margin-top:6px;color:#f59e0b;font-size:12px'>"
                        f"Em falta: <b>{prod_faltante}</b></div>",
                        unsafe_allow_html=True)

            status_opcoes = {
                "⚠️  Produto em falta": "falta",
                "❌  Loja fechada":     "fechado",
                "✅  Tudo abastecido":  "abastecido",
            }
            status_sel = list(status_opcoes.keys())[_st_idx]

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
                db_exec("""INSERT INTO relatorio
                    (data,funcionario,mercado,produto,status,foto,produto_faltante)
                    VALUES(?,?,?,?,?,?,?)""",
                    (str(date.today()), usuario, merc, "varios",
                     status_val, caminho, prod_faltante))

                now = datetime.now()
                if not checkin_hoje.empty and checkin_hoje.iloc[0]["status"] == "em_visita":
                    db_exec("UPDATE checkin SET hora_saida=?,status=? WHERE id=?",
                              (now.strftime("%H:%M"), "concluido", int(checkin_hoje.iloc[0]["id"])))
                elif checkin_hoje.empty:
                    db_exec("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                              (str(date.today()), now.strftime("%H:%M"), now.strftime("%H:%M"), usuario, merc, "concluido"))

                # ── Apaga fotos do disco após envio (economiza espaço) ──
                fotos_apagadas = 0
                for _, rp in prods.iterrows():
                    fp_del = f"fotos/{usuario}/{merc}_{dia_sel}_{rp['produto']}_{date.today()}.jpg".replace(" ","_")
                    if os.path.exists(fp_del):
                        try:
                            os.remove(fp_del)
                            fotos_apagadas += 1
                        except Exception:
                            pass
                # Limpa chaves de câmera/check do session_state deste mercado
                keys_del = [k for k in st.session_state
                            if merc.replace(" ","_") in k and dia_sel in k]
                for k in keys_del:
                    del st.session_state[k]

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

                # Coleta caminhos das fotos ANTES de apagar
                fotos_paths = [
                    fp for _, r in prods.iterrows()
                    for fp in [f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{date.today()}.jpg".replace(' ','_')]
                    if os.path.exists(fp)
                ]

                # Embute fotos em base64 no HTML (para não depender dos arquivos depois)
                import base64 as _b64
                def foto_para_b64(fp):
                    with open(fp,"rb") as f2:
                        return "data:image/jpeg;base64," + _b64.b64encode(f2.read()).decode()

                fotos_html = "".join(
                    f'<div style="margin:12px 0"><b style="color:#222">{r["produto"]}</b><br>'
                    f'<img src="{foto_para_b64(fp)}" style="width:100%;max-width:300px;border-radius:8px;margin-top:6px"></div>'
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

                # Apaga fotos originais do disco (já estão embutidas no HTML)
                for fp_del in fotos_paths:
                    try: os.remove(fp_del)
                    except Exception: pass

                html_bytes = rel_html.encode("utf-8")
                st.download_button("⬇️ Baixar relatório",
                    data=html_bytes,
                    file_name=f"relatorio_{merc}_{date.today()}.html".replace(" ","_"),
                    mime="text/html", key=f"dl_{merc}_{dia_sel}",
                    use_container_width=True)
                import urllib.parse
                dests_f = db_read("SELECT * FROM destinatarios")
                msg_rel = (f"📋 *Relatório El Kam*\n👤 {usuario}\n🏪 {merc}\n"
                           f"📅 {date.today().strftime('%d/%m/%Y')}\nStatus: {badge}")
                if not dests_f.empty:
                    st.markdown("<div style='margin-top:12px;color:#555;font-size:11px;"
                                "text-transform:uppercase;letter-spacing:1px'>Enviar por WhatsApp:</div>",
                                unsafe_allow_html=True)
                    for _, d in dests_f.iterrows():
                        _te = urllib.parse.quote(msg_rel)
                        _wa_m = f"https://wa.me/55{d['telefone']}?text={_te}"
                        _wa_p = f"https://web.whatsapp.com/send?phone=55{d['telefone']}&text={_te}"
                        st.markdown(
                            f"""<div style='display:flex;gap:8px;margin:6px 0'>
                            <a href='{_wa_m}' target='_blank' rel='noopener noreferrer' style='flex:2'>
                                <button style='background:#25D366;color:#fff;border:none;
                                border-radius:12px;padding:14px;font-size:14px;
                                font-weight:700;cursor:pointer;width:100%'>
                                📲 {d['nome']} (celular)</button></a>
                            <a href='{_wa_p}' target='_blank' rel='noopener noreferrer' style='flex:1'>
                                <button style='background:#128C7E;color:#fff;border:none;
                                border-radius:12px;padding:14px;font-size:13px;
                                font-weight:700;cursor:pointer;width:100%'>
                                💻 PC</button></a>
                            </div>""",
                            unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

    # ── CHAT FUNCIONÁRIO ──

    else:  # qualquer aba de chat

        page_header("Fale com o Admin", "Chat")

        db_exec("UPDATE chat SET lido=1 WHERE remetente=? AND tipo='admin'", (usuario,))
        # committed by db_exec

        hist = db_read(
            "SELECT * FROM chat WHERE (remetente=? AND tipo='funcionario') "
            "OR (remetente=? AND tipo='admin') ORDER BY id", (usuario, usuario))

        # Última mensagem do admin para o push
        ultima_adm = db_read(
            "SELECT id, mensagem FROM chat WHERE remetente=? AND tipo='admin' ORDER BY id DESC LIMIT 1",
            (usuario,))
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
                    db_exec("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                              (str(now.date()), now.strftime("%H:%M"), usuario, "funcionario", msg_f.strip(), 0))
                    # auto-committed; st.rerun()
