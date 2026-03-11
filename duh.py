import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date, datetime, timedelta

def now_br():
    """Datetime atual no fuso de Brasília (UTC-3)."""
    # Streamlit Cloud roda em UTC — Brasil (Toledo-PR) = UTC-3
    return datetime.utcnow() - timedelta(hours=3)

def today_br():
    return now_br().date()

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
        // ── GPS: captura posição e salva em hidden inputs ──
(function() {
  function _updateGPS() {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(function(pos) {
      var lat = pos.coords.latitude.toFixed(6);
      var lon = pos.coords.longitude.toFixed(6);
      var acc = Math.round(pos.coords.accuracy);
      // Grava em sessionStorage para o Streamlit pegar via query_params trick
      sessionStorage.setItem('gps_lat', lat);
      sessionStorage.setItem('gps_lon', lon);
      sessionStorage.setItem('gps_acc', acc);
      // Também preenche campos hidden se existirem
      var fl = document.getElementById('gps_lat_field');
      var fn = document.getElementById('gps_lon_field');
      if (fl) fl.value = lat;
      if (fn) fn.value = lon;
    }, function(err) {
      sessionStorage.setItem('gps_lat', '');
      sessionStorage.setItem('gps_lon', '');
    }, {enableHighAccuracy: true, timeout: 10000, maximumAge: 0});
  }
  _updateGPS();
  setInterval(_updateGPS, 30000); // atualiza a cada 30s
})();

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

# Limpa fotos órfãs com mais de 7 dias (guardado por 1 semana conforme configuração)
def _limpar_fotos_antigas():
    limite = _time.time() - 7 * 86400  # 7 dias (guardado por 1 semana)
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
    usuario TEXT, senha TEXT, tipo TEXT, primeiro_acesso INTEGER DEFAULT 1,
    aniversario TEXT DEFAULT '')""")
c.execute("""CREATE TABLE IF NOT EXISTS mercados (
    id INTEGER PRIMARY KEY AUTOINCREMENT, mercado TEXT, endereco TEXT UNIQUE, logo TEXT DEFAULT '',
    telefone_rel TEXT DEFAULT '', email_rel TEXT DEFAULT '')""")
c.execute("""CREATE TABLE IF NOT EXISTS produtos (mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS produto_fotos (
    produto TEXT, foto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS agenda (
    funcionario TEXT, dia TEXT, mercado TEXT, produto TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS relatorio (
    data TEXT, funcionario TEXT, mercado TEXT, produto TEXT, status TEXT, foto TEXT,
    produto_faltante TEXT DEFAULT '', foto_b64 TEXT DEFAULT '',
    hora TEXT DEFAULT '', enviado_mercado INTEGER DEFAULT 0, notif_admin INTEGER DEFAULT 0,
    lat REAL DEFAULT NULL, lon REAL DEFAULT NULL, foto_hash TEXT DEFAULT '')""")
c.execute("""CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT, hora TEXT, funcionario TEXT, mercado TEXT, tipo TEXT, detalhe TEXT)""")
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
if "email" not in usuarios_cols:
    db_exec("ALTER TABLE usuarios ADD COLUMN email TEXT DEFAULT ''")
try:
    _uc2 = [r[1] for r in conn.cursor().execute("PRAGMA table_info(usuarios)").fetchall()]
    if "aniversario" not in _uc2:
        db_exec("ALTER TABLE usuarios ADD COLUMN aniversario TEXT DEFAULT ''")
except: pass

mercados_cols = [r[1] for r in conn.cursor().execute("PRAGMA table_info(mercados)").fetchall()]
if "logo" not in mercados_cols:
    db_exec("ALTER TABLE mercados ADD COLUMN logo TEXT DEFAULT ''")
if "telefone_rel" not in mercados_cols:
    db_exec("ALTER TABLE mercados ADD COLUMN telefone_rel TEXT DEFAULT ''")
if "email_rel" not in mercados_cols:
    db_exec("ALTER TABLE mercados ADD COLUMN email_rel TEXT DEFAULT ''")

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
    ts = now_br().strftime("%Y%m%d_%H%M%S")
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
                                  (now_br() + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"))
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
                expirado  = now_br() > datetime.strptime(cod_exp, "%Y-%m-%d %H:%M:%S") \
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
    # Quando simula funcionário, usa o usuário selecionado para ver agenda real
    if tipo_efetivo == "funcionario" and st.session_state.get("superadmin_simular"):
        usuario = st.session_state["superadmin_simular"]
else:
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
    # Logo da empresa (se cadastrada)
    _emp_logo_row = db_read("SELECT foto FROM empresa WHERE id=1 LIMIT 1")
    _emp_logo_path = str(_emp_logo_row.iloc[0]["foto"]) if not _emp_logo_row.empty else ""
    if _emp_logo_path and _emp_logo_path not in ("","nan") and os.path.exists(_emp_logo_path):
        import base64 as _b64_sb
        with open(_emp_logo_path,"rb") as _lf_sb:
            _logo_sb_b64 = _b64_sb.b64encode(_lf_sb.read()).decode()
        _ext_sb = _emp_logo_path.split(".")[-1].lower()
        _mime_sb = "image/png" if _ext_sb=="png" else "image/jpeg"
        st.markdown(
            f"<div style='padding:16px 16px 8px;text-align:center'>"
            f"<img src='data:{_mime_sb};base64,{_logo_sb_b64}' "
            f"style='max-height:64px;max-width:180px;object-fit:contain;border-radius:8px'>"
            f"</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='padding:12px 16px 16px;border-bottom:1px solid #1c1c1c;margin-bottom:16px'>
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
                  "Destinatários", "Auditoria", "Configurações"]
    if "adm_menu" not in st.session_state:
        st.session_state["adm_menu"] = "Dashboard"
    menu = st.session_state["adm_menu"]

    # ── SIDEBAR: botões de navegação (desktop e celular) ──
    with st.sidebar:
        st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
        _icons = {"Dashboard":"📊","Funcionários":"👥","Mercados":"🏪","Agenda":"📋",
                  "Relatórios":"📈","Fotos":"📷","Fotos de Produtos":"🖼️","Chat":"💬",
                  "Empresa":"🏢","Destinatários":"📬","Auditoria":"🔍","Configurações":"⚙️"}
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
        if st.button("⚙️\nConf.",   key="mn_cfg", use_container_width=True): st.session_state["adm_menu"]="Configurações";   st.rerun()
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

    # ── NOTIFICAÇÃO DE NOVOS RELATÓRIOS ──
    _rel_novos = db_read(
        """SELECT funcionario, mercado, hora, status FROM relatorio
            WHERE data=? AND (notif_admin IS NULL OR notif_admin=0)
            ORDER BY rowid DESC LIMIT 5""",
        (str(today_br()),))
    if not _rel_novos.empty:
        _badge_n = {"abastecido":"✅","falta":"⚠️","fechado":"❌"}
        _rn = _rel_novos.iloc[0]
        _outros = len(_rel_novos) - 1
        _extra = f" <span style='color:#555'>+{_outros} outro(s)</span>" if _outros > 0 else ""
        st.markdown(f"""
        <div style='position:fixed;bottom:{24 if msgs_novas.empty else 110}px;right:24px;z-index:9998;
            background:#0a1a0a;border:1px solid #22c55e44;border-left:3px solid #22c55e;
            border-radius:12px;padding:14px 18px;box-shadow:0 8px 32px rgba(0,0,0,0.5);
            max-width:300px;animation:fadeIn 0.3s ease'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>
                <div style='width:8px;height:8px;background:#22c55e;border-radius:50%;flex-shrink:0'></div>
                <span style='color:#22c55e;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase'>
                    🔔 Novo relatório recebido{_extra}
                </span>
            </div>
            <div style='color:#fff;font-size:13px;font-weight:600;margin-bottom:2px'>
                🏪 {_rn['mercado']}
            </div>
            <div style='color:#888;font-size:12px'>
                👤 {_rn['funcionario'].split('.')[0].capitalize()}
                {_badge_n.get(str(_rn.get('status','')),'')}
                · {_rn.get('hora','') or 'agora'}
            </div>
            <div style='color:#333;font-size:10px;margin-top:6px'>Abra Relatórios para revisar</div>
        </div>
        """, unsafe_allow_html=True)
        # Marca como notificado ao abrir dashboard ou relatórios
        if menu in ("Dashboard","Relatórios"):
            try:
                conn2 = get_conn()
                conn2.cursor().execute(
                    "UPDATE relatorio SET notif_admin=1 WHERE data=? AND (notif_admin IS NULL OR notif_admin=0)",
                    (str(today_br()),))
                conn2.commit()
            except: pass

    # ── DASHBOARD ─────────────────────────────────────────

    if menu == "Dashboard":
        page_header("Visão Geral", "Dashboard")
        _hd = today_br(); _od = _hd - timedelta(days=1)
        # ── Aniversários de hoje ──
        _anivs = db_read(
            "SELECT usuario, telefone, aniversario FROM usuarios WHERE tipo='funcionario' AND aniversario != '' AND aniversario IS NOT NULL")
        _hoje_ddmm = _hd.strftime("%d/%m")
        if not _anivs.empty:
            _anivs_hoje = _anivs[_anivs["aniversario"].str.strip().str[:5] == _hoje_ddmm]
            for _, _ar in _anivs_hoje.iterrows():
                _n_aniv = _ar["usuario"].split(".")[0].capitalize()
                st.markdown(
                    f"<div style='background:linear-gradient(90deg,#1a1200,#1a0800);"
                    f"border:1.5px solid #f59e0b66;border-radius:12px;padding:14px 20px;"
                    f"margin-bottom:16px;display:flex;align-items:center;gap:14px'>"
                    f"<div style='font-size:32px'>🎂</div>"
                    f"<div style='flex:1'>"
                    f"<div style='color:#f59e0b;font-size:13px;font-weight:700'>"
                    f"Hoje é aniversário de {_n_aniv}! 🎉</div>"
                    f"<div style='color:#666;font-size:12px;margin-top:2px'>"
                    f"Acesse Funcionários para enviar parabéns pelo WhatsApp</div>"
                    f"</div></div>",
                    unsafe_allow_html=True)
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
        _cic = db_read("SELECT * FROM checkin WHERE data=? AND status='concluido'", (_hd,))

        # helper: calcula minutos entre duas strings HH:MM
        def _mins(h_ini, h_fim):
            try:
                from datetime import datetime as _dt2
                _a = _dt2.strptime(str(h_ini).strip(), "%H:%M")
                _b = _dt2.strptime(str(h_fim).strip(), "%H:%M")
                _d = int((_b - _a).total_seconds() / 60)
                return _d if _d >= 0 else None
            except: return None

        if not _cia.empty:
            st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
            section_title("📍 Em visita agora")
            for _,_cr in _cia.iterrows():
                _m_ativ = _mins(_cr['hora_entrada'], now_br().strftime("%H:%M"))
                _tempo_tag = f" · ⏱️ <span style='color:#f59e0b'>{_m_ativ} min</span>" if _m_ativ is not None else ""
                # Detectar hora UTC errada (< 06:00 pode ser UTC em vez de BR)
                _hora_suspeita = False
                try:
                    _h_num = int(str(_cr["hora_entrada"]).split(":")[0])
                    _hora_suspeita = _h_num < 6
                except: pass
                _hora_aviso = " ⚠️" if _hora_suspeita else ""
                st.markdown(
                    f"<div style='background:#0a1f0a;border:1px solid #22c55e33;border-radius:10px;"
                    f"padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px'>"
                    f"<div style='width:8px;height:8px;background:#22c55e;border-radius:50%'></div>"
                    f"<div><div style='color:#ddd;font-size:13px;font-weight:600'>"
                    f"👤 {_cr['funcionario'].split('.')[0].capitalize()}</div>"
                    f"<div style='color:#555;font-size:12px'>🏪 {_cr['mercado']} · desde {_cr['hora_entrada']}{_hora_aviso}{_tempo_tag}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True)

        # ── Botão para corrigir check-ins com hora UTC errada ──
        _ci_utc = db_read(
            "SELECT id, hora_entrada, hora_saida FROM checkin WHERE data=? "
            "AND CAST(SUBSTR(hora_entrada,1,2) AS INTEGER) < 6",
            (str(_hd),))
        if not _ci_utc.empty:
            st.markdown(
                f"<div style='background:#1a0a00;border:1px solid #f59e0b55;"
                f"border-radius:10px;padding:10px 14px;margin:8px 0;"
                f"font-size:12px;color:#f59e0b'>"
                f"⚠️ {len(_ci_utc)} check-in(s) com hora incorreta (UTC em vez de Brasília). "
                f"Clique para corrigir automaticamente (+3h).</div>",
                unsafe_allow_html=True)
            if st.button("🔧 Corrigir horas (UTC → Brasília)", key="btn_fix_utc"):
                from datetime import datetime as _dtt2, timedelta as _tdd2
                for _, _ce in _ci_utc.iterrows():
                    try:
                        _he = _dtt2.strptime(str(_ce["hora_entrada"]).strip(), "%H:%M")
                        _he_br = (_he + _tdd2(hours=3)).strftime("%H:%M")
                        _hs_br = ""
                        if str(_ce.get("hora_saida","")).strip() not in ("","nan"):
                            _hs = _dtt2.strptime(str(_ce["hora_saida"]).strip(), "%H:%M")
                            _hs_br = (_hs + _tdd2(hours=3)).strftime("%H:%M")
                        if _hs_br:
                            db_exec("UPDATE checkin SET hora_entrada=?, hora_saida=? WHERE id=?",
                                    (_he_br, _hs_br, int(_ce["id"])))
                        else:
                            db_exec("UPDATE checkin SET hora_entrada=? WHERE id=?",
                                    (_he_br, int(_ce["id"])))
                    except: pass
                st.success("✅ Horas corrigidas para Brasília!")
                st.rerun()

        if not _cic.empty:
            st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
            section_title("✅ Visitas concluídas hoje — tempo de permanência")
            for _,_cr2 in _cic.sort_values("id",ascending=False).iterrows():
                _min_p = _mins(_cr2['hora_entrada'], _cr2.get('hora_saida',''))
                if _min_p is not None:
                    if _min_p >= 60:
                        _tempo_str = f"{_min_p//60}h {_min_p%60}min"
                    else:
                        _tempo_str = f"{_min_p} min"
                    _cor_tempo = "#22c55e" if _min_p >= 15 else "#f59e0b" if _min_p >= 5 else "#ff4444"
                else:
                    _tempo_str = "—"
                    _cor_tempo = "#333"
                st.markdown(
                    f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:10px;"
                    f"padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center'>"
                    f"<div>"
                    f"<span style='color:#ddd;font-size:13px;font-weight:600'>"
                    f"👤 {_cr2['funcionario'].split('.')[0].capitalize()}</span>"
                    f" <span style='color:#444;font-size:11px'>·</span>"
                    f" <span style='color:#888;font-size:12px'>🏪 {_cr2['mercado']}</span>"
                    f"</div>"
                    f"<div style='text-align:right'>"
                    f"<div style='color:{_cor_tempo};font-size:13px;font-weight:700'>⏱️ {_tempo_str}</div>"
                    f"<div style='color:#444;font-size:11px'>{_cr2['hora_entrada']} → {_cr2.get('hora_saida','?')}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True)
        # ── MAPA DE VISITAS DO DIA ──
        _mercs_visitados_h = _rh["mercado"].unique().tolist() if not _rh.empty else []
        if _mercs_visitados_h:
            st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
            section_title("🗺️ Mapa de visitas hoje")
            _mercs_end = db_read("SELECT mercado, endereco FROM mercados")
            _q_parts = []
            for _mv in _mercs_visitados_h:
                _row_mv = _mercs_end[_mercs_end["mercado"]==_mv]
                if not _row_mv.empty:
                    _end_mv = str(_row_mv.iloc[0]["endereco"])
                    _q_parts.append(_end_mv)
            if _q_parts:
                # Monta URL do OpenStreetMap com os endereços como marcadores de busca
                _primeiro_end = _q_parts[0].replace(" ", "+").replace(",", "%2C")
                _mapa_url = f"https://www.openstreetmap.org/search?query={_primeiro_end}"
                # Lista visual dos mercados visitados com links de mapa individuais
                import urllib.parse as _upm
                _cols_map = st.columns(min(len(_q_parts), 3))
                for _mi_idx, (_mv2, _end2) in enumerate(zip(_mercs_visitados_h[:6], _q_parts[:6])):
                    with _cols_map[_mi_idx % min(len(_q_parts), 3)]:
                        _enc_end = _upm.quote(_end2 + ", Brasil")
                        _gmap_url = f"https://www.google.com/maps/search/?api=1&query={_enc_end}"
                        _osm_url  = f"https://www.openstreetmap.org/search?query={_enc_end}"
                        # Verifica se tem checkin concluído nesse mercado hoje
                        _ci_m = _cic[_cic["mercado"]==_mv2] if not _cic.empty else pd.DataFrame()
                        _status_m = "✅" if not _ci_m.empty else ("🟢" if _mv2 in (_cia["mercado"].tolist() if not _cia.empty else []) else "⏳")
                        st.markdown(
                            f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:10px;"
                            f"padding:12px 14px;margin-bottom:8px'>"
                            f"<div style='color:#fff;font-size:13px;font-weight:600;margin-bottom:6px'>"
                            f"{_status_m} {_mv2}</div>"
                            f"<div style='color:#555;font-size:11px;margin-bottom:8px'>{_end2}</div>"
                            f"<div style='display:flex;gap:6px'>"
                            f"<a href='{_gmap_url}' target='_blank' style='flex:1'>"
                            f"<button style='background:#1a73e8;color:#fff;border:none;border-radius:6px;"
                            f"padding:6px 8px;font-size:11px;font-weight:600;cursor:pointer;width:100%'>"
                            f"📍 Google Maps</button></a>"
                            f"<a href='{_osm_url}' target='_blank' style='flex:1'>"
                            f"<button style='background:#1c1c1c;color:#aaa;border:1px solid #333;border-radius:6px;"
                            f"padding:6px 8px;font-size:11px;font-weight:600;cursor:pointer;width:100%'>"
                            f"🗺️ OSM</button></a>"
                            f"</div></div>",
                            unsafe_allow_html=True)
            else:
                st.info("Cadastre endereços nos mercados para ver o mapa.")

        st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
        section_title("📈 Comparativo semanal")
        _dl=["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
        def _pd(df):
            if df.empty or "_d" not in df.columns: return [0]*7
            return [len(df[df["_d"]==(_is+timedelta(days=_di))]) for _di in range(7)]
        # Gráfico com ordem garantida Seg→Dom usando Altair
        import altair as alt
        _chart_vals = _pd(_rs) + _pd(_rant)
        _chart_days = _dl * 2
        _chart_semanas = ["Semana atual"]*7 + ["Anterior"]*7
        _chart_df = pd.DataFrame({"Dia": _chart_days, "Visitas": _chart_vals, "Semana": _chart_semanas})
        _chart = alt.Chart(_chart_df).mark_bar().encode(
            x=alt.X("Dia:N", sort=_dl, title=None,
                    axis=alt.Axis(labelColor="#888", tickColor="#333", domainColor="#333")),
            y=alt.Y("Visitas:Q", title=None,
                    axis=alt.Axis(labelColor="#888", gridColor="#1c1c1c", domainColor="#1c1c1c")),
            color=alt.Color("Semana:N",
                scale=alt.Scale(domain=["Semana atual","Anterior"], range=["#ff2b2b","#444"]),
                legend=alt.Legend(orient="bottom", labelColor="#888", titleColor="#888")),
            xOffset="Semana:N",
            tooltip=["Dia","Semana","Visitas"]
        ).properties(height=200).configure_view(
            strokeWidth=0, fill="#0a0a0a"
        ).configure(background="#0a0a0a")
        st.altair_chart(_chart, use_container_width=True)
        _sc1,_sc2,_sc3=st.columns(3)
        _sc1.metric("Semana atual",_ta); _sc2.metric("Semana anterior",_tb); _sc3.metric("Variação",f"{_ta-_tb:+d}")
        _nl=db_read("SELECT COUNT(*) as t FROM chat WHERE tipo='funcionario' AND lido=0").iloc[0]["t"]
        if _nl>0: st.warning(f"💬 **{int(_nl)}** mensagem(ns) não lida(s) no Chat.")

        # ── RANKING SEMANAL ──
        st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
        section_title("🏆 Ranking da semana")
        _rk_cols = st.columns(2)
        with _rk_cols[0]:
            if not _rs.empty:
                _rk = _rs.groupby("funcionario").agg(
                    visitas=("mercado","count"),
                    fotos=("foto_b64", lambda x: sum(1 for v in x if str(v).strip())),
                    faltas=("status", lambda x: sum(1 for v in x if v=="falta"))
                ).reset_index().sort_values("visitas", ascending=False).head(10)
                medals = ["🥇","🥈","🥉","4º","5º","6º","7º","8º","9º","10º"]
                for _ri2, (_, _rrow2) in enumerate(_rk.iterrows()):
                    _pct2 = int(_rrow2["visitas"]/_rk["visitas"].max()*100) if _rk["visitas"].max()>0 else 0
                    st.markdown(
                        f"<div style='margin-bottom:10px'>"
                        f"<div style='display:flex;justify-content:space-between;margin-bottom:3px'>"
                        f"<span style='color:#ddd;font-size:13px;font-weight:600'>"
                        f"{medals[_ri2] if _ri2<len(medals) else '•'} "
                        f"{_rrow2['funcionario'].split('.')[0].capitalize()}</span>"
                        f"<span style='color:#ff2b2b;font-size:12px;font-weight:700'>"
                        f"{int(_rrow2['visitas'])} vis · {int(_rrow2['fotos'])}📷 · {int(_rrow2['faltas'])}⚠️</span></div>"
                        f"<div style='background:#1a1a1a;border-radius:4px;height:5px'>"
                        f"<div style='background:#ff2b2b;width:{_pct2}%;height:5px;border-radius:4px'></div></div></div>",
                        unsafe_allow_html=True)
            else:
                st.info("Sem dados esta semana.")
        with _rk_cols[1]:
            # ── ESTOQUE CRÍTICO: produto em falta 3+ dias seguidos ──
            section_title("🚨 Estoque crítico")
            _rall2 = db_read("SELECT * FROM relatorio WHERE status='falta' AND produto_faltante!='' AND produto_faltante IS NOT NULL")
            if not _rall2.empty:
                _rall2["_d2"] = pd.to_datetime(_rall2["data"], errors="coerce").dt.date
                _alertas_est = []
                for _pf_combo, _df_pf in _rall2.groupby(["mercado","produto_faltante"]):
                    _dias_falta = sorted(_df_pf["_d2"].unique(), reverse=True)
                    if len(_dias_falta) >= 3:
                        _alertas_est.append((_pf_combo[0], _pf_combo[1], len(_dias_falta), _dias_falta[0]))
                if _alertas_est:
                    for _ae in sorted(_alertas_est, key=lambda x: -x[2]):
                        st.markdown(
                            f"<div style='background:#1a0000;border:1px solid #ff2b2b33;"
                            f"border-left:3px solid #ff2b2b;border-radius:8px;padding:10px 14px;margin-bottom:6px'>"
                            f"<div style='color:#ff4444;font-size:12px;font-weight:700'>🚨 {_ae[1]}</div>"
                            f"<div style='color:#555;font-size:11px'>🏪 {_ae[0]} · em falta {_ae[2]} dia(s)</div>"
                            f"<div style='color:#333;font-size:10px'>Último: {_ae[3].strftime('%d/%m/%Y') if hasattr(_ae[3],'strftime') else _ae[3]}</div>"
                            f"</div>", unsafe_allow_html=True)
                else:
                    st.success("✅ Nenhum produto crítico.")
            else:
                st.info("Sem registros de falta.")

        # ── RESUMO DIÁRIO (envio manual — relatório automático requer servidor externo) ──
        st.markdown("<hr style='border-color:#1c1c1c;margin:20px 0'>", unsafe_allow_html=True)
        section_title("📨 Resumo do dia")
        _adm_row2 = db_read("SELECT telefone, email FROM usuarios WHERE tipo='admin'")
        _adm_tel2 = _adm_row2.iloc[0]["telefone"] if not _adm_row2.empty else ""
        _n_vis_h = len(_rh); _n_merc_h = _rh["mercado"].nunique() if not _rh.empty else 0
        _n_func_h = _rh["funcionario"].nunique() if not _rh.empty else 0
        _n_falta_h = len(_rh[_rh["status"]=="falta"]) if not _rh.empty else 0
        _n_fech_h  = len(_rh[_rh["status"]=="fechado"]) if not _rh.empty else 0
        _n_ok_h    = len(_rh[_rh["status"]=="abastecido"]) if not _rh.empty else 0
        _resumo_txt = (
            f"📊 *Resumo El Kam — {_hd.strftime('%d/%m/%Y')}*\n"
            f"👥 Funcionários ativos: {_n_func_h}\n"
            f"🏪 Mercados visitados: {_n_merc_h}\n"
            f"📋 Total de visitas: {_n_vis_h}\n"
            f"✅ Abastecidos: {_n_ok_h}\n"
            f"⚠️ Produtos em falta: {_n_falta_h}\n"
            f"❌ Lojas fechadas: {_n_fech_h}"
        )
        st.markdown(
            f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:12px;padding:14px 18px;margin-bottom:12px'>"
            f"<div style='color:#888;font-size:12px;white-space:pre-line'>{_resumo_txt.replace('*','')}</div>"
            f"</div>", unsafe_allow_html=True)
        import urllib.parse as _upr2
        _enc_res = _upr2.quote(_resumo_txt)
        _sr1, _sr2, _sr3 = st.columns(3)
        with _sr1:
            if _adm_tel2:
                st.markdown(
                    f"<a href='https://wa.me/55{_adm_tel2}?text={_enc_res}' target='_blank'>"
                    f"<button style='background:#25D366;color:#fff;border:none;border-radius:8px;"
                    f"padding:10px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                    f"📲 Enviar ao admin (celular)</button></a>",
                    unsafe_allow_html=True)
        with _sr2:
            if _adm_tel2:
                st.markdown(
                    f"<a href='https://web.whatsapp.com/send?phone=55{_adm_tel2}&text={_enc_res}' target='_blank'>"
                    f"<button style='background:#128C7E;color:#fff;border:none;border-radius:8px;"
                    f"padding:10px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                    f"💻 Enviar ao admin (PC)</button></a>",
                    unsafe_allow_html=True)
        with _sr3:
            st.caption("⚠️ Relatório automático às 18h requer servidor dedicado (não disponível no Streamlit Cloud). Use este botão manualmente.")

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
            _cc1, _cc2 = st.columns(2)
            with _cc1: tel_novo = st.text_input("📱 WhatsApp (com DDD, só números)", placeholder="11999998888")
            with _cc2: aniv_novo = st.text_input("🎂 Aniversário (DD/MM)", placeholder="25/12")
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
                        db_exec("INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,telefone,aniversario) VALUES(?,?,?,?,?,?)",
                                  (login,"elkam","funcionario",1,tel_novo.strip(),aniv_novo.strip()))
                        st.success(f"✅ Criado! Login: **{login}** · Senha: **elkam**")
                        st.rerun()

        section_title("Funcionários cadastrados")
        funcs = db_read("SELECT usuario, telefone, aniversario FROM usuarios WHERE tipo='funcionario' AND usuario!='superadmin'")

        if funcs.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            for _, row in funcs.iterrows():
                login_func = row['usuario']
                tel_func   = row.get('telefone','') or ''

                col_i, col_w, col_r, col_ed, col_e = st.columns([4, 2, 2, 1, 1])
                _aniv_func = row.get("aniversario","") or ""
                # Verifica se hoje é aniversário
                _hoje_ddmm = today_br().strftime("%d/%m")
                _is_aniv = (_aniv_func.strip()[:5] == _hoje_ddmm) if _aniv_func else False
                _aniv_tag = f" · 🎂 <span style='color:#f59e0b'>Aniversário hoje!</span>" if _is_aniv else (f" · 🎂 {_aniv_func}" if _aniv_func else "")
                with col_i:
                    st.markdown(
                        f"<div style='color:#ddd;font-size:13px;font-weight:600;padding:10px 0'>"
                        f"👤 {login_func}"
                        f"<span style='color:#444;font-weight:400;font-size:11px'>"
                        f"{'  · 📱 '+tel_func if tel_func else '  · sem telefone'}"
                        f"{_aniv_tag}</span></div>",
                        unsafe_allow_html=True)
                # Envia parabéns automático via WhatsApp se for aniversário
                if _is_aniv and tel_func:
                    import urllib.parse as _up_aniv
                    _nome_aniv = login_func.split('.')[0].capitalize()
                    _msg_aniv = (f"🎂 *Parabéns, {_nome_aniv}!* 🎉\n\n"
                                 f"Toda a equipe El Kam Merchandising deseja a você um feliz aniversário! 🥳\n"
                                 f"Que este novo ano seja repleto de saúde, alegria e muito sucesso!\n\n"
                                 f"Com carinho,\nEquipe El Kam 🏪")
                    _enc_aniv = _up_aniv.quote(_msg_aniv)
                    st.markdown(
                        f"<div style='background:#1a1200;border:1px solid #f59e0b55;border-radius:10px;"
                        f"padding:10px 14px;margin-bottom:8px'>"
                        f"<div style='color:#f59e0b;font-size:12px;font-weight:700;margin-bottom:6px'>🎂 Hoje é aniversário de {_nome_aniv}! Enviar parabéns:</div>"
                        f"<div style='display:flex;gap:6px'>"
                        f"<a href='https://wa.me/55{tel_func}?text={_enc_aniv}' target='_blank' style='flex:1'>"
                        f"<button style='background:#25D366;color:#fff;border:none;border-radius:8px;padding:8px;font-size:11px;font-weight:700;cursor:pointer;width:100%'>📲 Celular</button></a>"
                        f"<a href='https://web.whatsapp.com/send?phone=55{tel_func}&text={_enc_aniv}' target='_blank' style='flex:1'>"
                        f"<button style='background:#128C7E;color:#fff;border:none;border-radius:8px;padding:8px;font-size:11px;font-weight:700;cursor:pointer;width:100%'>💻 PC</button></a>"
                        f"</div></div>",
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
                with col_ed:
                    if st.button("✏️", key=f"edit_{login_func}", help="Editar funcionário"):
                        # Toggle: abre/fecha formulário de edição
                        _ek = f"editando_func_{login_func}"
                        st.session_state[_ek] = not st.session_state.get(_ek, False)
                        # Fechar qualquer outro que esteja aberto
                        for _k2 in list(st.session_state.keys()):
                            if _k2.startswith("editando_func_") and _k2 != _ek:
                                st.session_state[_k2] = False
                        st.rerun()
                with col_e:
                    if st.button("🗑️", key=f"del_{login_func}", help="Excluir funcionário"):
                        st.session_state[f"confirm_del_func_{login_func}"] = True
                        st.rerun()

                # ── FORMULÁRIO DE EDIÇÃO ──
                if st.session_state.get(f"editando_func_{login_func}", False):
                    # Buscar dados atuais do funcionário
                    _fu_row = db_read(
                        "SELECT usuario, telefone, aniversario, email FROM usuarios WHERE usuario=?",
                        (login_func,))
                    _fu = _fu_row.iloc[0] if not _fu_row.empty else {}
                    _tel_atual   = str(_fu.get("telefone","") or "")
                    _aniv_atual  = str(_fu.get("aniversario","") or "")
                    _email_atual = str(_fu.get("email","") or "")

                    st.markdown(
                        f"<div style='background:#0d1a0d;border:1.5px solid #ff2b2b44;"
                        f"border-radius:14px;padding:18px 20px;margin:8px 0 16px'>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='color:#ff2b2b;font-size:10px;font-weight:700;"
                        f"letter-spacing:2px;text-transform:uppercase;margin-bottom:12px'>"
                        f"✏️ Editando: {login_func}</div>",
                        unsafe_allow_html=True)

                    # Separar nome.sobrenome para edição
                    _partes = login_func.split(".")
                    _nome_ed    = _partes[0].capitalize() if len(_partes) > 0 else ""
                    _sobr_ed    = _partes[1].capitalize() if len(_partes) > 1 else ""

                    _ec1, _ec2 = st.columns(2)
                    with _ec1:
                        _ed_nome = st.text_input("Nome", value=_nome_ed,
                                                  key=f"ed_nome_{login_func}")
                    with _ec2:
                        _ed_sobr = st.text_input("Sobrenome", value=_sobr_ed,
                                                  key=f"ed_sobr_{login_func}")
                    _ec3, _ec4 = st.columns(2)
                    with _ec3:
                        _ed_tel  = st.text_input("📱 WhatsApp", value=_tel_atual,
                                                  placeholder="11999998888",
                                                  key=f"ed_tel_{login_func}")
                    with _ec4:
                        _ed_aniv = st.text_input("🎂 Aniversário (DD/MM)", value=_aniv_atual,
                                                  placeholder="25/12",
                                                  key=f"ed_aniv_{login_func}")
                    _ed_email = st.text_input("📧 E-mail (opcional)", value=_email_atual,
                                               key=f"ed_email_{login_func}")

                    st.caption("⚠️ Mudar nome/sobrenome cria um novo login. A senha e agenda serão migradas.")

                    _eb1, _eb2 = st.columns(2)
                    with _eb1:
                        if st.button("💾 Salvar alterações", key=f"salvar_ed_{login_func}",
                                     use_container_width=True):
                            _novo_login = f"{_ed_nome.strip().lower()}.{_ed_sobr.strip().lower()}"
                            _login_mudou = (_novo_login != login_func)

                            if not _ed_nome.strip() or not _ed_sobr.strip():
                                st.error("Nome e sobrenome são obrigatórios.")
                            elif _login_mudou and not db_read(
                                    "SELECT usuario FROM usuarios WHERE usuario=?",
                                    (_novo_login,)).empty:
                                st.error(f"Login '{_novo_login}' já existe.")
                            else:
                                if _login_mudou:
                                    # Criar novo login preservando senha/tipo/acesso
                                    _u_old = db_read(
                                        "SELECT senha, tipo, primeiro_acesso FROM usuarios WHERE usuario=?",
                                        (login_func,))
                                    if not _u_old.empty:
                                        _r = _u_old.iloc[0]
                                        db_exec(
                                            "INSERT INTO usuarios (usuario,senha,tipo,primeiro_acesso,"
                                            "telefone,email,aniversario) VALUES(?,?,?,?,?,?,?)",
                                            (_novo_login, _r["senha"], _r["tipo"],
                                             int(_r["primeiro_acesso"]),
                                             _ed_tel.strip(), _ed_email.strip(), _ed_aniv.strip()))
                                        # Migrar agenda, checkin, chat, relatorio
                                        db_exec("UPDATE agenda SET funcionario=? WHERE funcionario=?",
                                                  (_novo_login, login_func))
                                        db_exec("UPDATE checkin SET funcionario=? WHERE funcionario=?",
                                                  (_novo_login, login_func))
                                        db_exec("UPDATE chat SET remetente=? WHERE remetente=?",
                                                  (_novo_login, login_func))
                                        db_exec("UPDATE relatorio SET funcionario=? WHERE funcionario=?",
                                                  (_novo_login, login_func))
                                        db_exec("DELETE FROM usuarios WHERE usuario=?", (login_func,))
                                else:
                                    db_exec(
                                        "UPDATE usuarios SET telefone=?, email=?, aniversario=? "
                                        "WHERE usuario=?",
                                        (_ed_tel.strip(), _ed_email.strip(),
                                         _ed_aniv.strip(), login_func))

                                st.session_state[f"editando_func_{login_func}"] = False
                                st.success(f"✅ Funcionário {'**' + _novo_login + '**' if _login_mudou else '**' + login_func + '**'} editado com sucesso!")
                                st.rerun()
                    with _eb2:
                        if st.button("✖ Cancelar", key=f"cancel_ed_{login_func}",
                                     use_container_width=True):
                            st.session_state[f"editando_func_{login_func}"] = False
                            st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)

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
            _ct, _ce2 = st.columns(2)
            with _ct: _tel_rel = st.text_input("📱 Telefone para relatório (com DDD)", placeholder="11999998888", key="nm_tel_rel")
            with _ce2: _email_rel = st.text_input("📧 Email para relatório", placeholder="gerente@mercado.com", key="nm_email_rel")
            logo_up = st.file_uploader("🖼️ Logo do mercado (opcional)", type=["jpg","jpeg","png"], key="logo_new")
            st.caption("📌 Telefone e email são usados pelo admin para enviar relatórios ao contratante.")
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
                            db_exec("INSERT INTO mercados (mercado,endereco,logo,telefone_rel,email_rel) VALUES(?,?,?,?,?)",
                                      (mercado.strip(), endereco.strip(), logo_path,
                                       _tel_rel.strip(), _email_rel.strip()))
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
                        _et, _ee = st.columns(2)
                        with _et:
                            novo_tel_rel = st.text_input("📱 Telefone para relatório", value=row.get("telefone_rel","") or "", key=f"edit_tel_{row['id']}", placeholder="11999998888")
                        with _ee:
                            novo_email_rel = st.text_input("📧 Email para relatório", value=row.get("email_rel","") or "", key=f"edit_email_{row['id']}", placeholder="gerente@mercado.com")
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
                                db_exec("UPDATE mercados SET mercado=?,endereco=?,logo=?,telefone_rel=?,email_rel=? WHERE id=?",
                                          (novo_nome.strip(), novo_end.strip(), logo_path,
                                           novo_tel_rel.strip(), novo_email_rel.strip(), int(row["id"])))
                                if novo_nome.strip() != nome_antigo:
                                    db_exec("UPDATE agenda SET mercado=? WHERE mercado=?",
                                              (novo_nome.strip(), nome_antigo))
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
        page_header("Acompanhamento", "Relatórios")
        import base64 as _b64r, urllib.parse as _upr

        badge_map = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}

        def _fmt_data(d):
            """Converte 2026-03-10 para 10/03/2026."""
            try:
                from datetime import datetime as _dtp
                return _dtp.strptime(str(d)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
            except: return str(d)[:10]

        # Logo El Kam real (base64 embutido — sem depender de arquivo externo)
        _LOGO_SVG = "<img src='data:image/png;base64,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AAAAABJAAgAFAAABJAAwABgAFABMAAgAAAAALAAAAKACZAAAAyABkAEAAABQAUAAAAAAAAAAAEkAEABYAAkAEABkAAAAACAAgAMgASQAAAAAQAAAFABQAAATAAGAAUAAAAAAAAAAADIAJIAAAAAIACgAoAAAAAAAAAAAAAAAAAIABgADAAKACYABQAAAQAAAAAEABQAMgAAAoAAAAAJgAAAEAAAAABkAAAAAAAAAAAAACSACAAyAAAAAAAAABAAQAGUAAAAkgAgAAAAAAAMgAAAAAAAAAAAAAAAAASQAQAAAAAAAFABQAAAQAAAFAAAAAAABAAQAGQAAAAAAAAAAAAAAAAAIAAACAAAAoAKAAAAAAAAAAACAAoAAAAAAAAAAAAAAAAAAAAAAAIACAAAAAAoAAAEAAoAAAAAAAAAJgADAAKAAAAAAAAAAAAAAACAAgAMgAAAAAAAAAQAEABQAUAEABAAAAAAAAUAEAAABkAAAAAAAAACAAAAgAAAAAAAAALkAEAAABQAUAAAAAAAEkACAAUAAAAAAAAAAAEAAABQASQAQAAAAAFgAFAAAAAAAAAAAAwAAAAAAAAACZABQAAAAAAAAAAAAAYgAAAAAAAoAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSACAAyAAAAABJAAABQAAASQAQAFABQAQAFkAGIAAAAAKACgAAAAAAAAAkgAgAAAAAAAAAAAAAKAAACgAAAAAAAAAgAKACZABQAAAAASQAQAAAFAAABAAUADAAKACZABQAMgAAAAAAAAAAAAAAAkgAgAMgAAAAAAAQADIAAAIAAAAAAAAACgAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAABIAAAKACSAAACgAkgAgAAAMgAAAYgAsgAgAAAAAAALAAKAAAAAAACSACAAAAAAoAIAAAAADIAAAGIAMgAAAAAAAAAAAQADIAKACAAAAgAAAMgAAAAASAAUAAAEkAEAAABQAUAAAAAAAAAAAEkACAAUAAAAAEABAAAAXAAIAAAAAAAAACgAoAAAAAAAAAAAAAJIAAAEgAgAKACgAAAAAAAgAIACwABgAAAAAFAAAAABJABAAUAFABAAAAQAAAFABAAAAWAAUAAAAAEkAEAAAAAAAAAAAAAAABYABQAAAAAAAAAAAAAAAAAYgAuQAAAMAASACgA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AAKADEAAAAAFwABAAKAAACZABQAQAEABYABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAADIAKACSACAAygAAAEABQAAAAAQAEAAABQAQAGQAAAAAMQAAAXAAKAAAAACAAZAAABAAAAAAAAAAWAAUAAAAAAAAAAAAAAAAAEkAEAAAAABQAUAAAAAAAAAEyAAABAAKMhESlBiAoAMQAAAAAAAAAUAFAAABMgAZABAAAAAAAAAAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkgAZABQAQAEAAABkACSABgAFAAAAAAAAAAAAAAwACAAgAAAAALkACQAQAFgAFAAABAAQAAAAAFABAAAAAAUAEABQAUAAAAAAAEgAFAAAAAAABiAAAAAAAAACgAZABAAUAAAEAAABQAUAAAEkAEABQAQAAAAAAAFgAFABiAAAAAAAAAAACwACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxAAABkACSAAACgAAAAAAAAAAAAAgAKAAAAAAACYABAAAAAAAAAAAAUAFAAABiAAAAAAAAAAAAAAACgAoAAAAAAAAAIACgAgAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIAAAEkAEAAAAABQAQAAAAAFABAAAAUAEAAABQAUAAAAAAAAAAAAAAAAAAAAAAAAAEyACgAAAAAAAAAAAgAIADIAAAAAAAAAAAAAAAAAEkAEABcgAAAAAgAMgASQAQAAAAAFABAgAABkAAADEAAAAAFwACAAAABACgAgALkADIAGQAUAAACQAYgAAAoAGAAAAQAAAFAAAAwABgAEAAAAAAAAAAABYABQAAAQAEABQAUAEABAAAAAAAAZAAAAxABQAUAAAAAAAAAAAAAAAAAAAAAAAAAEkAAAFAAAAAAAAAAAAAAAAAAAAkAEABcgAAAAAAAAAAAgAIAAAAAAADIAAAEwAAACAAoAIAAADIAAAAAGIAAAMgASQAQAAAAAAAAAAAFgAFAAAAABMAAYABQAAASQAQAAAFkACAAUAAAAAGIAAAAAAAAALAAKAAAAACYABAAWAAUAAAEABAAAAXIAKAAAAACZAAAAABQAAAAATIAKAAAAAAAAAAACYABQAAAAAAAAAAAAAAAAAAAAAQAEABYABQAAAAAAAAAAATAAGAAAAQAGUAAAAAAgAIACgAYAAwACgAAAAAgAAAKAAAAACYAAwAAACAAsAAoAAAAAAAAAAAAAAAAAIACAAAAoAKABkAEABAAAAAAAAAAZABAAAAAAAACSAAACgAAAgAIAC4AAwABkADIAGQAQAAAFgAFAAABAAQAGQAAAAAIACgAAAAAAAmAAUAAAEABQAAAAAAASQAQAGUAAgAKAAAAAAAAAAAAAAAAAAACYABQAAAAAAAAAAAAAAAAAAAAASQAUAAAAAAAAAAAAAEwACgAAAkgAoAAAAAAAAAAAAAIACAAoAKACAAgAAAAAKABgAAAFAAAAAAAAAAABJABAAUADIAKAAAAAAACAAgAAAAAAAAAKACgAkgAAAoAAAAAAAAAAAAAAAAAAAJIAIACwACgAAAAAgAIACgAQACgAAAAAAAAAkgAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJkAFAAABAAUAAAAAAAAAEkAEABQAUAAAEwACAAAAAAsAAoAAAAAAAAAAAAAAAJIAIAAAAACgAoAIACAAAAAAAAAAAAoAAAKAAACYABQAAAAAAAAAAAAAAAAAAASQAMAAoAAAAAAAJIAIAAACwACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmQAQAFyACgAkgAsAAAAAAAAmQAAAAAQAFAAyABkAEAAAAABYABAAXIAAAKACSACgAmQAMgAgAAAAAAAAAAAAAASiEigAgAAAAALAAKAAAAAAAAAAAAAAAAAAAAAAABkAEyAAACgAAAAAAAAAAAAAxABQAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEyACgAkgAZAAgAFAAABMgAoAMQAAAAAAAAAAAUAEABkAAAAABIAMQAWAAQAAAAAAAAAAAAAAAFABAAUAFAAAAABJABAAAAAAAAAAAAAAUAEAAAAAAAAAAABYABQAQAAAAAFAAAAAAAAAAAAAAABAAQAAAGQAAAAAAAAAAAAAMQAUAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJABAAZAAkgAgALAAKAAADEAAAAAAAAAAAAAGQAAAAAAAAAAAJIAAAAAGAAAAAAMAAgAAAAAKACAAAAAAoAKACSABIAIAAAAAAAAADIAGIALAAKAAACYAAkAEAAAAAAAAAAABkAAAAAAAAAAAAAAAAAAAAACYABQAAAAAAAAAAAAASQAQAGUAAAAAAAAAAAAAAAAmQAMgAoAAAAAAAAAAAIABAAKAAAAACSACAAyAAAAAAABAAQAFAAAAwACgAAAAAAAAAAAgAAAKAAAAAAAAAAACYAAABQASQAQAAAAAFwACgAAAAAAAxAAAAAAABkAAAAAAAAACAAAAAAAAgAAAAAAALAAKACZAAyABkAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAABAAWAAAAAAAAAAAAAAAASQAQAGUAAAAAAAAAAAAkgAAAZABQAAAAAAAAAAAAAAATAAKAAACZABQAAAAAAABPcgAAAAEABQAAAAAAAAAAAAAAAAAAAAAYgAAAsAAoAAJ2SJkYgKAAACSACAAAAAAuQAUAAAAACQAYgAuAAUAAAEkAEAAAAABYABZABAAQAFAAwACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmQAAAXAAAAAAAAAAAAAAJIAAAAAKAAAAAAAAAAAAAAAAAAAAACAAAAoAAAAAAAAAAAAAAAAAAAAAIABAAIACgAoAAAAAMQAWAAMgAAAQMggQYgMgAAAAAYgAAAAAAAyAAAAAAABAAUAAAAAEkAEABkAAAAAAADEAAAGUAAAAAAAAAAAAAAAAAAmQAMgAZABQAAAAAAAAAAAAAAAAAAAAASQAQAFgAFAAAAAAAAAAAAABAAIABQAAAAAAAAAAAAAAAAAYgAAAyAAAAAAAAAAAAAAAAAAAAAAAAAAkAGIAAAAAAAAALkAAAEAAAAAAABYEwlikkQAoAAAAAAAMQAUAFAAABAAUAAAAAAAAAAAAAEABQAAASQAUAAAEwACgAAAAAAAAAAAAAAAAAgAGAAMAAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIACgAAAAAAAAAmAAUAAAAAAAAAAAEABYAAAAAAABAAAAUAEkACAAJABAAAAAAAAAAAAAAUAFATskyMQEkAFAAAAABiACgAAAoAAAAAAAAAAAAAAAIABAAEgAoAAAAAAAJIAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSACgAAAAAAAAAAAAAAAAmEAJmEJQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkgAgAMgAAAAASQAQAGQAAAAAAAAAMQAAAAAUAFAAABAAUEwhMdhIkBiMQGQAAAAAIAAAC4ABAAAAMgAoAAAAAAAAAAAIACgAAAAAAAAAAAkgAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmOwlIgxAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEkAAAFAAAAAAAAAAAAAAAAABJAAABAAAAZAAAAAAmQAUGUMUx2JIkBBiAyAAAAAAAAAAABJABAAUAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATsgAAAAAAABJAAgAFAEggAAAAAAAGQjclMCAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAIABQAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAxABkDJiySQAQBCVEShMoWAAAAATCEwCQGIiYQmUMgAQAAAFAAEwbEJQRshkAxAUAAAAAAAAE7IZIMQFAAAAAAAAExBsgBOxskQEbJAYiZQoAACUAAAAAAAAAJiEJA2QncQQAoAAAmANjZIgxGTFQTsQlBiAoAAJiEJSRKJSAxEoUAAAAAAAAAATCQQRsbJAYiZQoCUAAAAAAAAAAAAAAAAAAAAADJEpkQmIQlQ2NkiDEZI5GRAnkhQAAAAAAAAAASQlBGyGSAQJ2QoAAAAAkEAAAAAAAAAAAAAkECUAAAAAAAAAlKEoABgf/2Q==' style='height:70px;max-width:260px;object-fit:contain;background:#000;border-radius:8px;padding:4px 8px'>"

        def _gerar_html_rel(df_rows, titulo="El Kam Merchandising", subtitulo="", apagar_fotos=False):
            """Gera HTML profissional agrupado por mercado, fotos em pasta clicável."""
            if df_rows.empty:
                return "<html><body><p>Nenhum dado.</p></body></html>"

            _mercs_h = df_rows["mercado"].unique().tolist()
            _blocos = ""
            _foto_idx = 0  # contador global para IDs únicos dos accordions

            for _mh in sorted(_mercs_h):
                _df_mh = df_rows[df_rows["mercado"]==_mh]
                _funcs_mh = list(set(_df_mh["funcionario"].tolist()))
                _data_raw = str(_df_mh.iloc[0]["data"])[:10] if not _df_mh.empty else ""
                _data_mh  = _fmt_data(_data_raw)
                _hora_mh  = _df_mh.iloc[0].get("hora","") if not _df_mh.empty else ""

                _prods_rows = ""
                _fotos_pasta = ""  # accordions de fotos no final
                _n_fotos_merc = 0

                for _, _rh2 in _df_mh.iterrows():
                    _foto_idx += 1
                    _st_r    = str(_rh2.get("status","")).strip()
                    _badge_r = {"abastecido":"✅ Abastecido","falta":"⚠️ Em falta","fechado":"❌ Loja fechada"}.get(_st_r.lower().strip(), _st_r or "—")
                    _cor_r   = {"abastecido":"#f0fff4","falta":"#fffbeb","fechado":"#fff1f2"}.get(_st_r.lower().strip(), "#fff")
                    _ico_r   = {"abastecido":"🟢","falta":"🟡","fechado":"🔴"}.get(_st_r.lower().strip(), "⚪")
                    _pf_r    = _rh2.get("produto_faltante","") or ""
                    _prod_nm = _rh2.get("produto","—")
                    _b64_r   = _rh2.get("foto_b64","") or ""
                    _aid     = f"foto_{_foto_idx}"

                    # Link clicável para a foto (abre accordion na pasta)
                    if _b64_r.strip():
                        _n_fotos_merc += 1
                        _foto_link = f"<a href='#pasta_{_mh.replace(' ','_')}' onclick='document.getElementById(\"{_aid}\").style.display=\"block\";return false;' style='color:#1a56db;font-size:12px;text-decoration:none'>📷 Ver foto</a>"
                        _fotos_pasta += (
                            f"<div id='{_aid}' style='display:none;margin:12px 0;padding:14px;background:#f8f8f8;border-radius:10px;border:1px solid #eee'>"
                            f"<div style='font-weight:700;font-size:13px;margin-bottom:10px;color:#222'>📦 {_prod_nm}</div>"
                            f"<img src='data:image/jpeg;base64,{_b64_r}' style='max-width:100%;max-height:320px;border-radius:8px;border:2px solid #ddd'>"
                            f"</div>"
                        )
                    else:
                        _foto_link = "<span style='color:#aaa;font-size:12px'>Sem foto</span>"

                    _prods_rows += (
                        f"<tr style='background:{_cor_r}'>"
                        f"<td style='padding:10px 12px;font-weight:700'>{_ico_r} {_prod_nm}</td>"
                        f"<td style='padding:10px 12px'>{_badge_r}</td>"
                        f"<td style='padding:10px 12px;color:#b45309'>{_pf_r or '—'}</td>"
                        f"<td style='padding:10px 12px'>{_foto_link}</td>"
                        f"</tr>"
                    )
                    if apagar_fotos:
                        db_exec("UPDATE relatorio SET foto_b64='',foto='' WHERE rowid=?", (int(_rh2.get("rowid",0)),))

                # Pasta de fotos clicável
                _pasta_html = ""
                if _fotos_pasta:
                    _pasta_html = (
                        f"<div id='pasta_{_mh.replace(' ','_')}' style='background:#f5f5f5;border-radius:10px;padding:16px 18px;margin-top:12px'>"
                        f"<div style='font-size:13px;font-weight:700;color:#444;margin-bottom:10px'>📁 Pasta de fotos — {_mh} ({_n_fotos_merc} foto(s))</div>"
                        f"<div style='color:#888;font-size:12px;margin-bottom:10px'>Clique em 'Ver foto' ao lado de cada produto para abrir a imagem aqui.</div>"
                        f"{_fotos_pasta}"
                        f"</div>"
                    )

                _blocos += (
                    f"<div style='border:1.5px solid #e5e7eb;border-radius:14px;margin-bottom:32px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.06)'>"
                    f"<div style='background:#ff2b2b;color:#fff;padding:14px 20px;display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='font-size:17px;font-weight:900'>🏪 {_mh}</span>"
                    f"<span style='font-size:12px;opacity:.9'>📅 {_data_mh}{'  🕐 '+_hora_mh if _hora_mh else ''}  ·  "
                    f"👤 {', '.join(f.split(chr(46))[0].capitalize() for f in _funcs_mh)}</span>"
                    f"</div>"
                    f"<div style='padding:0 0 16px'>"
                    f"<table style='width:100%;border-collapse:collapse;font-size:13px'>"
                    f"<thead><tr style='background:#fafafa'>"
                    f"<th style='padding:10px 14px;text-align:left;border-bottom:2px solid #eee;color:#444'>Produto</th>"
                    f"<th style='padding:10px 14px;text-align:left;border-bottom:2px solid #eee;color:#444'>Status</th>"
                    f"<th style='padding:10px 14px;text-align:left;border-bottom:2px solid #eee;color:#444'>Em falta</th>"
                    f"<th style='padding:10px 14px;text-align:left;border-bottom:2px solid #eee;color:#444'>Foto</th>"
                    f"</tr></thead><tbody>{_prods_rows}</tbody></table>"
                    f"<div style='padding:0 16px'>{_pasta_html}</div>"
                    f"</div></div>"
                )

            _now_str = now_br().strftime('%d/%m/%Y %H:%M')
            return (
                "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
                "body{font-family:Arial,sans-serif;background:#fff;padding:28px;color:#222;max-width:980px;margin:auto}"
                ".hdr{display:flex;align-items:flex-start;justify-content:space-between;"
                "border-bottom:5px solid #ff2b2b;padding-bottom:24px;margin-bottom:32px}"
                ".sub{color:#888;font-size:13px;margin-top:6px}"
                ".ftr{color:#bbb;font-size:11px;margin-top:36px;text-align:center;"
                "border-top:1px solid #eee;padding-top:16px}"
                "a{color:#1a56db}"
                "</style></head><body>"
                f"<div class='hdr'>"
                f"<div style='display:flex;flex-direction:column;gap:6px'>"
                f"{_LOGO_SVG}"
                f"<div class='sub' style='color:#888;font-size:12px;margin-top:4px'>{subtitulo}</div></div>"
                f"<div style='text-align:right'>"
                f"<div style='color:#ff2b2b;font-size:14px;font-weight:700'>{titulo}</div>"
                f"<div style='color:#888;font-size:12px;margin-top:4px'>Gerado em {_now_str}</div>"
                f"</div></div>"
                f"{_blocos}"
                f"<div class='ftr'>© El Kam Merchandising — {_now_str} — Todos os direitos reservados.</div>"
                "</body></html>"
            )

        # ── FILTROS (preferência: hoje) ──
        rel_all = db_read("SELECT rowid, * FROM relatorio")
        _mercs_info = db_read("SELECT mercado, telefone_rel, email_rel FROM mercados")

        st.markdown("### 🔍 Filtros")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            periodo = st.selectbox("Período", ["Hoje","Últimos 7 dias","Últimos 30 dias","Intervalo personalizado"], index=0)
        with fc2:
            fm_rel = st.selectbox("Mercado", ["Todos"] + (sorted(rel_all["mercado"].unique().tolist()) if not rel_all.empty else []))
        with fc3:
            ff_rel = st.selectbox("Funcionário", ["Todos"] + (sorted(rel_all["funcionario"].unique().tolist()) if not rel_all.empty else []))

        if periodo == "Intervalo personalizado":
            dc1, dc2 = st.columns(2)
            with dc1: d_ini = st.date_input("De", value=today_br()-timedelta(days=7))
            with dc2: d_fim = st.date_input("Até", value=today_br())
        elif periodo == "Hoje": d_ini = d_fim = today_br()
        elif periodo == "Últimos 7 dias": d_ini = today_br()-timedelta(days=7); d_fim = today_br()
        else: d_ini = today_br()-timedelta(days=30); d_fim = today_br()

        df_r = rel_all.copy()
        if not df_r.empty:
            df_r["data_dt"] = pd.to_datetime(df_r["data"], errors="coerce")
            df_r = df_r[(df_r["data_dt"].dt.date >= d_ini) & (df_r["data_dt"].dt.date <= d_fim)]
        if fm_rel != "Todos" and not df_r.empty: df_r = df_r[df_r["mercado"]==fm_rel]
        if ff_rel != "Todos" and not df_r.empty: df_r = df_r[df_r["funcionario"]==ff_rel]

        # ── MÉTRICAS ──
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Visitas", len(df_r))
        m2.metric("Funcionários", df_r["funcionario"].nunique() if not df_r.empty else 0)
        m3.metric("Mercados", df_r["mercado"].nunique() if not df_r.empty else 0)
        m4.metric("✅ Abastecidos", len(df_r[df_r["status"]=="abastecido"]) if not df_r.empty else 0)

        st.markdown("<hr style='border-color:#1c1c1c;margin:16px 0'>", unsafe_allow_html=True)

        if df_r.empty:
            st.info("Nenhum relatório no período selecionado.")
        else:
            # ── GRADE DE RELATÓRIOS ──
            section_title("📋 Relatórios do período — marque para enviar ao mercado")
            selecionados_rel = []

            # Agrupa por mercado para exibir 1 card por mercado com produtos listados
            _mercs_rel = df_r["mercado"].unique().tolist() if not df_r.empty else []
            for _merc_r in sorted(_mercs_rel):
                _df_merc_r = df_r[df_r["mercado"]==_merc_r].sort_values(
                    ["data_dt","hora"] if "hora" in df_r.columns else ["data_dt"], ascending=False)
                _funcs_r = _df_merc_r["funcionario"].unique().tolist()
                _enviado_r = int(_df_merc_r["enviado_mercado"].max() or 0) if "enviado_mercado" in _df_merc_r.columns else 0
                _env_tag = "<span style='color:#22c55e;font-size:11px;font-weight:700'>✅ Enviado</span>" if _enviado_r else "<span style='color:#555;font-size:11px'>⏳ Pendente envio</span>"
                _hora_r  = _df_merc_r.iloc[0].get("hora","") if not _df_merc_r.empty else ""
                _data_r  = _fmt_data(_df_merc_r.iloc[0]["data"]) if not _df_merc_r.empty else ""

                # Monta lista de produtos com status e foto
                _prods_html = ""
                for _, _pr in _df_merc_r.iterrows():
                    _badge_p = {"abastecido":"✅","falta":"⚠️","fechado":"❌"}.get(str(_pr.get("status","")), "·")
                    _pf_p    = _pr.get("produto_faltante","") or ""
                    _has_f   = bool((str(_pr.get("foto_b64","")) or "").strip())
                    _foto_ico = "📷" if _has_f else ""
                    _pf_tag   = f" <span style='color:#f59e0b;font-size:11px'>(em falta)</span>" if _pf_p else ""
                    _prods_html += (
                        f"<div style='display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #1a1a1a'>"
                        f"<span style='font-size:14px'>{_badge_p}</span>"
                        f"<span style='color:#ccc;font-size:13px;font-weight:600'>{_pr.get('produto','—')}</span>"
                        f"{_pf_tag}"
                        f"<span style='margin-left:auto;color:#555;font-size:11px'>{_foto_ico}  👤 {_pr.get('funcionario','').split('.')[0].capitalize()}</span>"
                        f"</div>"
                    )

                _ck_r, _ci_r = st.columns([1, 11])
                with _ck_r:
                    # Seleciona todos os rowids deste mercado de uma vez
                    if st.checkbox("", key=f"sel_merc_{_merc_r}", label_visibility="collapsed"):
                        for _rid_r in _df_merc_r["rowid"].tolist():
                            selecionados_rel.append(int(_rid_r))
                with _ci_r:
                    st.markdown(
                        f"<div style='background:#111;border:1px solid {'#22c55e33' if _enviado_r else '#1c1c1c'};"
                        f"border-radius:12px;padding:14px 16px;margin-bottom:8px'>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
                        f"<span style='color:#ff2b2b;font-size:15px;font-weight:900'>🏪 {_merc_r}</span>"
                        f"<span>{_env_tag}</span></div>"
                        f"<div style='color:#555;font-size:12px;margin-bottom:8px'>"
                        f"📅 {_data_r}{'  🕐 '+_hora_r if _hora_r else ''}  ·  "
                        f"👥 {', '.join(f.split('.')[0].capitalize() for f in _funcs_r)}</div>"
                        f"<div style='background:#0d0d0d;border-radius:8px;padding:10px 12px'>"
                        f"{_prods_html}</div></div>",
                        unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # ── AÇÕES ──
            _a1, _a2, _a3 = st.columns(3)
            with _a1:
                if st.button("🗑️ Excluir selecionados", key="del_rel", disabled=not selecionados_rel, use_container_width=True):
                    fazer_backup()
                    for rid in selecionados_rel:
                        db_exec("DELETE FROM relatorio WHERE rowid=?", (rid,))
                    st.success("Excluído(s).")
                    st.rerun()
            with _a2:
                if st.button("📥 Baixar relatório (com fotos)", key="dl_rel", use_container_width=True):
                    _df_dl = df_r[df_r["rowid"].isin(selecionados_rel)] if selecionados_rel else df_r
                    _titulo_dl = f"Relatório de {d_ini.strftime('%d/%m/%Y')} a {d_fim.strftime('%d/%m/%Y')}"
                    _sub_dl = f"Gerado em {now_br().strftime('%d/%m/%Y %H:%M')}"
                    _html_dl = _gerar_html_rel(_df_dl, _titulo_dl, _sub_dl, apagar_fotos=False)
                    st.download_button("⬇️ Clique para baixar", data=_html_dl.encode("utf-8"),
                        file_name=f"relatorio_elkam_{d_ini}_{d_fim}.html", mime="text/html",
                        key="dl_btn_rel")
            with _a3:
                if st.button("📤 Enviar ao mercado", key="enviar_merc_btn",
                             disabled=not selecionados_rel, use_container_width=True):
                    st.session_state["confirm_envio_merc"] = True
                    st.rerun()

            # ── MODAL DE CONFIRMAÇÃO DE ENVIO ──
            if st.session_state.get("confirm_envio_merc", False):
                _df_env = df_r[df_r["rowid"].isin(selecionados_rel)]
                _merc_env = _df_env["mercado"].unique().tolist() if not _df_env.empty else []

                st.markdown(
                    "<div style='background:#1a0a00;border:2px solid #f59e0b44;border-radius:14px;padding:20px;margin:12px 0'>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<div style='color:#f59e0b;font-size:14px;font-weight:700;margin-bottom:12px'>"
                    f"⚠️ Atenção! {len(selecionados_rel)} relatório(s) serão enviados para: "
                    f"<b>{', '.join(_merc_env)}</b></div>",
                    unsafe_allow_html=True)
                st.markdown(
                    "<div style='color:#ff4444;font-size:13px;font-weight:600;margin-bottom:16px'>"
                    "📷 Após o envio, as fotos serão apagadas do banco. Deseja baixar antes?</div>",
                    unsafe_allow_html=True)

                _ec1, _ec2, _ec3 = st.columns(3)
                with _ec1:
                    if st.button("⬇️ Baixar e enviar", key="dl_e_envia", use_container_width=True):
                        _html_env = _gerar_html_rel(_df_env,
                            f"Relatório El Kam — {', '.join(_merc_env)}",
                            f"Gerado em {now_br().strftime('%d/%m/%Y %H:%M')}",
                            apagar_fotos=True)
                        for rid in selecionados_rel:
                            db_exec("UPDATE relatorio SET enviado_mercado=1 WHERE rowid=?", (rid,))
                        st.session_state["confirm_envio_merc"] = False
                        st.session_state["html_para_baixar"] = _html_env
                        st.session_state["html_fname"] = f"relatorio_{d_ini}_{d_fim}.html"
                        st.rerun()
                with _ec2:
                    if st.button("📤 Só enviar (sem baixar)", key="so_envia", use_container_width=True):
                        _html_env = _gerar_html_rel(_df_env,
                            f"Relatório El Kam — {', '.join(_merc_env)}",
                            f"Gerado em {now_br().strftime('%d/%m/%Y %H:%M')}",
                            apagar_fotos=True)
                        for rid in selecionados_rel:
                            db_exec("UPDATE relatorio SET enviado_mercado=1 WHERE rowid=?", (rid,))
                        st.session_state["confirm_envio_merc"] = False
                        st.rerun()
                        st.success("✅ Relatório marcado como enviado. Fotos apagadas.")
                with _ec3:
                    if st.button("✖ Cancelar", key="cancel_envio", use_container_width=True):
                        st.session_state["confirm_envio_merc"] = False
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

                # ── LINKS DE ENVIO POR WHATSAPP / EMAIL para cada mercado ──
                for _merc_n in _merc_env:
                    _mi = _mercs_info[_mercs_info["mercado"]==_merc_n]
                    _tel_m = _mi.iloc[0]["telefone_rel"] if not _mi.empty and _mi.iloc[0].get("telefone_rel") else ""
                    _email_m = _mi.iloc[0]["email_rel"] if not _mi.empty and _mi.iloc[0].get("email_rel") else ""
                    _df_merc = _df_env[_df_env["mercado"]==_merc_n]
                    _n_vis = len(_df_merc)
                    _n_falta = len(_df_merc[_df_merc["status"]=="falta"])
                    _msg_merc = (_upr.quote(
                        f"📋 *Relatório El Kam Merchandising*\n"
                        f"🏪 {_merc_n}\n"
                        f"📅 {d_ini.strftime('%d/%m/%Y')} a {d_fim.strftime('%d/%m/%Y')}\n"
                        f"👤 Visitas: {_n_vis}  |  ⚠️ Faltas: {_n_falta}\n"
                        f"Segue o relatório completo em anexo."
                    ))
                    st.markdown(f"<div style='margin:8px 0;color:#888;font-size:12px;font-weight:700'>🏪 {_merc_n}</div>", unsafe_allow_html=True)
                    _lw1, _lw2, _lw3 = st.columns(3)
                    with _lw1:
                        if _tel_m:
                            st.markdown(
                                f"<a href='https://wa.me/55{_tel_m}?text={_msg_merc}' target='_blank'>"
                                f"<button style='background:#25D366;color:#fff;border:none;border-radius:8px;"
                                f"padding:9px 12px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                                f"📲 WhatsApp Celular</button></a>",
                                unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='color:#333;font-size:11px;padding:8px'>Sem telefone cadastrado</div>", unsafe_allow_html=True)
                    with _lw2:
                        if _tel_m:
                            st.markdown(
                                f"<a href='https://web.whatsapp.com/send?phone=55{_tel_m}&text={_msg_merc}' target='_blank'>"
                                f"<button style='background:#128C7E;color:#fff;border:none;border-radius:8px;"
                                f"padding:9px 12px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                                f"💻 WhatsApp PC</button></a>",
                                unsafe_allow_html=True)
                    with _lw3:
                        if _email_m:
                            _subj = _upr.quote(f"Relatório El Kam — {_merc_n} — {d_ini.strftime('%d/%m/%Y')}")
                            _body_txt = f"Segue o relatorio de merchandising de {_merc_n}. Periodo: {d_ini} a {d_fim}."
                            _body = _upr.quote(_body_txt)
                            st.markdown(
                                f"<a href='mailto:{_email_m}?subject={_subj}&body={_body}' target='_blank'>"
                                f"<button style='background:#1a56db;color:#fff;border:none;border-radius:8px;"
                                f"padding:9px 12px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                                f"📧 Email</button></a>",
                                unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='color:#333;font-size:11px;padding:8px'>Sem email cadastrado</div>", unsafe_allow_html=True)

            # ── DOWNLOAD PENDENTE (após baixar+enviar) ──
            if st.session_state.get("html_para_baixar"):
                st.download_button(
                    "⬇️ Baixar relatório agora",
                    data=st.session_state["html_para_baixar"].encode("utf-8"),
                    file_name=st.session_state.get("html_fname","relatorio.html"),
                    mime="text/html", key="dl_final_btn")
                if st.button("✅ Feito, dispensar", key="dispensar_dl"):
                    st.session_state.pop("html_para_baixar", None)
                    st.session_state.pop("html_fname", None)
                    st.rerun()

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
                        now = now_br()
                        db_exec("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                                  (str(now.date()), now.strftime("%H:%M"), func_sel, "admin", msg_a.strip(), 1))
                        # auto-committed; st.rerun()

    # ── AUDITORIA ──────────────────────────────────────────

    elif menu == "Auditoria":
        page_header("Segurança", "Painel de Auditoria")
        st.caption("Detecta anomalias: visitas muito rápidas, fotos duplicadas e alertas de integridade.")

        _aud_all = db_read("SELECT * FROM auditoria ORDER BY id DESC")
        _rel_all_a = db_read("SELECT * FROM relatorio")
        _ci_all_a  = db_read("SELECT * FROM checkin")

        # ── MÉTRICAS ──
        _a1,_a2,_a3 = st.columns(3)
        _n_rapidas  = len(_aud_all[_aud_all["tipo"]=="visita_rapida"]) if not _aud_all.empty else 0
        _n_dup_foto = len(_aud_all[_aud_all["tipo"]=="foto_duplicada"]) if not _aud_all.empty else 0
        _n_sem_foto = 0
        if not _rel_all_a.empty and "foto_b64" in _rel_all_a.columns:
            _n_sem_foto = int((_rel_all_a["foto_b64"].fillna("").str.strip() == "").sum())
        _a1.metric("⚡ Visitas rápidas", _n_rapidas)
        _a2.metric("📷 Fotos duplicadas", _n_dup_foto)
        _a3.metric("❌ Sem foto", _n_sem_foto)

        st.markdown("<hr style='border-color:#1c1c1c;margin:16px 0'>", unsafe_allow_html=True)

        # ── FILTRO ──
        _aud_tipos = ["Todos", "visita_rapida", "foto_duplicada"]
        _aud_tipo_sel = st.selectbox("Tipo de alerta", _aud_tipos,
            format_func=lambda x: {"Todos":"Todos","visita_rapida":"⚡ Visita rápida","foto_duplicada":"📷 Foto duplicada"}.get(x,x))

        _df_aud = _aud_all.copy() if not _aud_all.empty else pd.DataFrame()
        if _aud_tipo_sel != "Todos" and not _df_aud.empty:
            _df_aud = _df_aud[_df_aud["tipo"]==_aud_tipo_sel]

        if _df_aud.empty:
            st.success("✅ Nenhum alerta registrado.")
        else:
            section_title(f"📋 {len(_df_aud)} alerta(s) encontrado(s)")
            _tipo_icons = {"visita_rapida":"⚡","foto_duplicada":"📷"}
            _tipo_cores = {"visita_rapida":"#1a0a00","foto_duplicada":"#0a001a"}
            _tipo_borda = {"visita_rapida":"#f59e0b44","foto_duplicada":"#a855f744"}
            _tipo_label = {"visita_rapida":"Visita rápida","foto_duplicada":"Foto duplicada"}
            for _, _ar in _df_aud.iterrows():
                _ic = _tipo_icons.get(_ar["tipo"],"⚠️")
                _bg = _tipo_cores.get(_ar["tipo"],"#111")
                _bd = _tipo_borda.get(_ar["tipo"],"#33333344")
                _lb = _tipo_label.get(_ar["tipo"], _ar["tipo"])
                # Formata data DD/MM/AAAA
                try:
                    from datetime import datetime as _dta
                    _data_aud = _dta.strptime(str(_ar["data"])[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                except: _data_aud = str(_ar["data"])[:10]
                st.markdown(
                    f"<div style='background:{_bg};border:1px solid {_bd};"
                    f"border-left:3px solid {'#f59e0b' if _ar['tipo']=='visita_rapida' else '#a855f7'};"
                    f"border-radius:10px;padding:12px 16px;margin-bottom:6px'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='color:#ddd;font-size:13px;font-weight:700'>"
                    f"{_ic} {_lb} — {_ar.get('funcionario','').split('.')[0].capitalize()}</span>"
                    f"<span style='color:#444;font-size:11px'>{_data_aud} {_ar.get('hora','')}</span></div>"
                    f"<div style='color:#555;font-size:12px;margin-top:4px'>"
                    f"🏪 {_ar.get('mercado','—')} · {_ar.get('detalhe','')}</div>"
                    f"</div>",
                    unsafe_allow_html=True)

        # ── VISITAS SEM FOTO ──
        st.markdown("<hr style='border-color:#1c1c1c;margin:16px 0'>", unsafe_allow_html=True)
        section_title("📷 Relatórios sem foto")
        if not _rel_all_a.empty:
            _rel_sf = _rel_all_a[(_rel_all_a["foto_b64"].fillna("") == "") & (_rel_all_a["foto"].fillna("") == "")]
            if _rel_sf.empty:
                st.success("✅ Todos os relatórios têm foto.")
            else:
                for _, _rs2 in _rel_sf.head(20).iterrows():
                    try: _ds2 = datetime.strptime(str(_rs2["data"])[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                    except: _ds2 = str(_rs2["data"])[:10]
                    st.markdown(
                        f"<div style='background:#111;border:1px solid #1c1c1c;border-radius:8px;"
                        f"padding:9px 14px;margin-bottom:4px;color:#555;font-size:12px'>"
                        f"📷 Sem foto · <b style='color:#aaa'>{_rs2.get('produto','—')}</b>"
                        f" · {_rs2.get('mercado','—')} · {_rs2.get('funcionario','—')} · {_ds2}</div>",
                        unsafe_allow_html=True)
        else:
            st.info("Sem relatórios.")

    # ── CONFIGURAÇÕES ─────────────────────────────────────

    elif menu == "Configurações":
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
                        file_name=f"elkam_backup_{today_br()}.db",
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
            _fat = st.session_state["func_aba"] == _fopt
            if st.button(_fopt.strip(), key=f"fn_sb_{_fopt}", use_container_width=True):
                st.session_state["func_aba"] = _fopt
                st.rerun()

    aba = st.session_state["func_aba"]

    # ── INÍCIO / DASHBOARD FUNCIONÁRIO ──

    if aba == "🏠  Início":
        nome_exib_d = usuario.split(".")[0].capitalize()
        page_header(f"Olá, {nome_exib_d}! 👋", "Painel do dia")
        _hj = str(today_br())
        _ds = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"][today_br().weekday()]
        _trf = db_read("SELECT * FROM agenda WHERE funcionario=?", (usuario,))
        _md = _trf[_trf["dia"]==_ds]["mercado"].unique().tolist() if not _trf.empty else []
        _rh2 = db_read("SELECT * FROM relatorio WHERE funcionario=? AND data=?", (usuario,_hj))
        _vis = _rh2["mercado"].nunique() if not _rh2.empty else 0
        _fotos_n = len(_rh2[_rh2["foto"]!=""]) if not _rh2.empty else 0
        _falta_n = len(_rh2[_rh2["status"]=="falta"]) if not _rh2.empty else 0
        _ci2 = db_read("SELECT * FROM checkin WHERE funcionario=? AND data=?", (usuario,_hj))

        # ── SCORE DO DIA ──
        _total_mercs = len(_md)
        _score_vis   = int((_vis / _total_mercs * 40)) if _total_mercs > 0 else 0  # até 40pts
        _score_foto  = int((_fotos_n / max(_total_mercs, 1)) * 30)                  # até 30pts
        _score_tempo = 0
        if not _ci2.empty:
            for _, _cir in _ci2.iterrows():
                try:
                    _ta3 = datetime.strptime(str(_cir["hora_entrada"]).strip(), "%H:%M")
                    _tb3 = datetime.strptime(str(_cir.get("hora_saida","")).strip(), "%H:%M")
                    if (_tb3 - _ta3).total_seconds() >= 300:  # >= 5 min = ponto
                        _score_tempo += int(30 / max(len(_ci2), 1))
                except: pass
        _score_total = min(100, _score_vis + _score_foto + _score_tempo)
        _score_cor   = "#22c55e" if _score_total >= 80 else ("#f59e0b" if _score_total >= 50 else "#ff4444")
        _score_icon  = "🏆" if _score_total >= 90 else ("⭐" if _score_total >= 70 else ("👍" if _score_total >= 50 else "💪"))

        st.markdown(
            f"<div style='background:linear-gradient(135deg,#0f0f0f,#1a1a1a);"
            f"border:1.5px solid {_score_cor}44;border-radius:14px;padding:16px 20px;"
            f"display:flex;align-items:center;justify-content:space-between;margin-bottom:16px'>"
            f"<div><div style='color:#444;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase'>Score do dia</div>"
            f"<div style='color:{_score_cor};font-size:36px;font-weight:900;line-height:1'>{_score_total}%</div>"
            f"<div style='color:#555;font-size:12px;margin-top:4px'>"
            f"Visitas {_score_vis}pts · Fotos {_score_foto}pts · Tempo {_score_tempo}pts</div></div>"
            f"<div style='font-size:48px'>{_score_icon}</div></div>",
            unsafe_allow_html=True)

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
            # Calcula tempo de permanência
            _tp_min = None
            if _ul.get("hora_entrada") and _ul.get("hora_saida"):
                try:
                    from datetime import datetime as _dtt
                    _ta2 = _dtt.strptime(str(_ul["hora_entrada"]).strip(), "%H:%M")
                    _tb2 = _dtt.strptime(str(_ul["hora_saida"]).strip(), "%H:%M")
                    _tp_min = int((_tb2 - _ta2).total_seconds() / 60)
                    if _tp_min < 0: _tp_min = None
                except: pass
            if _tp_min is not None:
                _tp_str = f"{_tp_min//60}h {_tp_min%60}min" if _tp_min >= 60 else f"{_tp_min} min"
                _tp_tag = f"<span style='color:#22c55e;font-size:11px;font-weight:700;margin-left:8px'>⏱️ {_tp_str} na loja</span>"
            else:
                _tp_tag = ""
            st.markdown(f"<div style='margin-top:14px;background:#111;border:1px solid #1c1c1c;border-radius:10px;padding:13px 16px'><div style='color:#444;font-size:10px;text-transform:uppercase;letter-spacing:1px'>Última atividade</div><div style='color:#ddd;font-size:13px;font-weight:600;margin-top:4px'>🏪 {_ul.get('mercado','—')}</div><div style='color:#555;font-size:11px;margin-top:2px'>Entrada {_ul.get('hora_entrada','—')}{_hs}{_tp_tag}</div></div>", unsafe_allow_html=True)

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
        if emp["foto"] and str(emp["foto"]) not in ("", "nan") and os.path.exists(str(emp["foto"])):
            st.image(str(emp["foto"]), use_container_width=True)
        else:
            st.info("Nenhuma imagem cadastrada para a empresa ainda.")
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

        # Força o dia atual como padrão (ignora session_state antigo)
        _hoje_ds  = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"][today_br().weekday()]
        _def_dia  = _hoje_ds if _hoje_ds in dias_present else dias_present[0]
        # Resetar se o valor salvo for de outro dia da semana passada
        if st.session_state.get("_agenda_dia_sel") != _def_dia:
            st.session_state["_agenda_dia_sel"] = _def_dia
        dia_sel = st.selectbox("Selecione o dia", dias_present,
                               index=dias_present.index(st.session_state["_agenda_dia_sel"]),
                               key="_agenda_dia_sel")
        dados_dia = tarefas[tarefas["dia"] == dia_sel]

        # ── AVISO se o dia selecionado não é hoje ──
        _hoje_ds2 = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"][today_br().weekday()]
        _dia_e_hoje = (dia_sel == _hoje_ds2)
        if not _dia_e_hoje:
            st.info(f"📅 Você está visualizando **{dia_sel}**. Check-in e fotos só estão disponíveis para o dia de hoje ({_hoje_ds2}).")

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
                "SELECT * FROM checkin WHERE funcionario=? AND mercado=? AND data=?", (usuario, merc, str(today_br())))

            if checkin_hoje.empty:
                if _dia_e_hoje:
                    if st.button(f"📍 Fazer check-in em {merc}", key=f"cin_{merc}_{dia_sel}"):
                        now = now_br()
                        db_exec("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                                  (str(today_br()), now.strftime("%H:%M"), "", usuario, merc, "em_visita"))
                        st.success(f"✅ Check-in às {now.strftime('%H:%M')}!")
                        st.rerun()
                else:
                    st.markdown("<div style='color:#444;font-size:12px;padding:8px 0'>⛔ Check-in disponível apenas hoje</div>", unsafe_allow_html=True)
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
                nome_foto_prod = f"{pasta_p}/{merc}_{dia_sel}_{prod_nome}_{today_br()}.jpg".replace(" ","_")
                tem_foto_prod  = os.path.exists(nome_foto_prod)

                # Foto de referência cadastrada pelo admin
                foto_ref = db_read(
                    "SELECT foto FROM produto_fotos WHERE produto=? LIMIT 1", (prod_nome,))
                tem_ref = (not foto_ref.empty and
                           str(foto_ref.iloc[0]["foto"]) not in ("","nan") and
                           os.path.exists(str(foto_ref.iloc[0]["foto"])))

                # Persiste estado: se foto já existe em disco, considera abastecido
                if tem_foto_prod and not st.session_state.get(chave_check, False):
                    st.session_state[chave_check] = True
                abast_prod = st.session_state.get(chave_check, False)

                # ── CARD DO PRODUTO ──
                cor_borda = "#22c55e44" if abast_prod else "#1a1a1a"
                cor_bg    = "#0a180e"   if abast_prod else "#0d0d0d"
                _badge_ab = ("<span style='background:#0a2b14;border:1px solid #22c55e44;"
                              "border-radius:8px;padding:4px 10px;color:#22c55e;"
                              "font-size:11px;font-weight:700'>✅ Abastecido</span>"
                              if abast_prod else "")
                st.markdown(
                    f"<div style='background:{cor_bg};border:1.5px solid {cor_borda};"
                    f"border-radius:14px;padding:14px 18px;margin-bottom:8px'>"
                    f"<div style='display:flex;align-items:center;gap:10px'>"
                    f"<span style='background:#ff2b2b22;border-radius:8px;"
                    f"padding:6px 10px;font-size:18px'>📦</span>"
                    f"<div style='flex:1'>"
                    f"<div style='color:#888;font-size:10px;letter-spacing:1.5px;"
                    f"text-transform:uppercase'>Produto</div>"
                    f"<div style='color:#fff;font-size:16px;font-weight:800'>{prod_nome}</div>"
                    f"</div>{_badge_ab}</div></div>",
                    unsafe_allow_html=True)

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
                    if _dia_e_hoje:
                        if st.button("📸 Tirar foto", key=f"abrir_cam_{merc}_{dia_sel}_{i}",
                                     use_container_width=True):
                            st.session_state[chave_mostrar_cam] = "cam"
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
                            ts = now_br().strftime("%d/%m/%Y %H:%M:%S")
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
                            ts = now_br().strftime("%d/%m/%Y %H:%M:%S")
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
                f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{today_br()}.jpg".replace(" ","_")
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

            # ── JÁ EXISTE RELATÓRIO deste merc hoje? ──
            _rel_existente = db_read(
                "SELECT rowid,* FROM relatorio WHERE funcionario=? AND mercado=? AND data=?",
                (usuario, merc, str(today_br())))
            _ja_enviado = not _rel_existente.empty

            if _ja_enviado:
                _r_ex = _rel_existente.iloc[0]
                _badge_ex = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(str(_r_ex.get("status","")), "")
                _pf_ex = _r_ex.get("produto_faltante","") or ""
                _hora_ex = _r_ex.get("hora","") or ""
                st.markdown(
                    f"<div style='background:#0a2b14;border:1px solid #22c55e44;border-radius:12px;"
                    f"padding:14px 18px;margin:12px 0;text-align:center'>"
                    f"<div style='color:#22c55e;font-size:14px;font-weight:700'>✅ Relatório já enviado hoje</div>"
                    f"<div style='color:#555;font-size:12px;margin-top:4px'>"
                    f"{_badge_ex}  ·  {_hora_ex}"
                    + (f"<br>⚠️ Em falta: {_pf_ex}" if _pf_ex else "")
                    + f"</div></div>",
                    unsafe_allow_html=True)
            else:
                # Botões full-width (melhor para mobile)
                if st.button("✅ Enviar relatório", key=f"btn_{merc}_{dia_sel}",
                             disabled=not confirmado, use_container_width=True):
                    import base64 as _b64
                    import urllib.parse as _up
                    status_val = status_opcoes[status_sel]
                    _hora_agora = now_br().strftime("%H:%M")
                    _data_hoje  = str(today_br())

                    import hashlib as _hl
                    # ── Coleta GPS do sessionStorage via componente HTML ──
                    _gps_lat = st.session_state.get(f"gps_lat_{merc}", None)
                    _gps_lon = st.session_state.get(f"gps_lon_{merc}", None)
                    # Injeta JS para ler GPS e salvar no session_state via URL hash
                    st.markdown(f"""
                    <script>
                    (function(){{
                        var lat = sessionStorage.getItem('gps_lat') || '';
                        var lon = sessionStorage.getItem('gps_lon') || '';
                        var acc = sessionStorage.getItem('gps_acc') || '';
                        // Preenche inputs ocultos do Streamlit via query string não funciona,
                        // mas podemos mostrar para o usuário
                        var el = document.getElementById('gps_status_disp_{merc.replace(' ','_')}');
                        if (el && lat) {{
                            el.textContent = '📍 GPS: ' + lat + ', ' + lon + ' (±' + acc + 'm)';
                            el.style.color = '#22c55e';
                        }} else if (el) {{
                            el.textContent = '📍 GPS não disponível (permita localização)';
                            el.style.color = '#555';
                        }}
                    }})();
                    </script>
                    <div id='gps_status_disp_{merc.replace(' ','_')}' style='font-size:11px;color:#555;margin:4px 0'>
                        📍 Verificando GPS...</div>
                    """, unsafe_allow_html=True)

                    # ── Salva 1 linha por PRODUTO com sua foto individual ──
                    _prods_wa_list = []
                    _alertas_fraude = []
                    for _, _rp2 in prods.iterrows():
                        _prod_nm = _rp2["produto"]
                        _fp2 = f"fotos/{usuario}/{merc}_{dia_sel}_{_prod_nm}_{today_br()}.jpg".replace(" ","_")
                        _fb64_prod = ""
                        _foto_hash = ""
                        if os.path.exists(_fp2):
                            with open(_fp2,"rb") as _fb2:
                                _raw = _fb2.read()
                                _fb64_prod = _b64.b64encode(_raw).decode()
                                _foto_hash = _hl.md5(_raw).hexdigest()
                            # ── Verificação de foto duplicada ──
                            _dup_foto = db_read(
                                "SELECT data, mercado FROM relatorio WHERE foto_hash=? AND funcionario=? AND foto_hash!=''",
                                (_foto_hash, usuario))
                            if not _dup_foto.empty:
                                _dup_row = _dup_foto.iloc[0]
                                _alertas_fraude.append(f"⚠️ Foto do produto '{_prod_nm}' já foi usada em {_dup_row['mercado']} em {_dup_row['data']}")
                                db_exec("INSERT INTO auditoria (data,hora,funcionario,mercado,tipo,detalhe) VALUES(?,?,?,?,?,?)",
                                    (_data_hoje, _hora_agora, usuario, merc, "foto_duplicada",
                                     f"Produto: {_prod_nm} | Hash: {_foto_hash[:12]}"))

                        _st_prod = "falta" if (_prod_nm in prod_faltante) else status_val
                        _pf_prod = _prod_nm if _st_prod == "falta" else ""
  foto = _fp2 if os.path.exists(_fp2) else ""

db_exec("""
INSERT INTO relatorio (
data, funcionario, mercado, produto, status, foto,
produto_faltante, foto_b64, hora,
enviado_mercado, notif_admin, lat, lon, foto_hash
)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""",
(
data, funcionario, mercado, produto, status, foto,
produto_faltante, foto_b64, hora,enviado_mercado,notif_admin
0, 0, lat, lon, foto_hash
))
                        _prods_wa_list.append(
                            f"  {'✅' if _st_prod == 'abastecido' else ('⚠️' if _st_prod == 'falta' else '❌')} {_prod_nm}")

                    # Mostra alertas de fraude se houver
                    if _alertas_fraude:
                        for _af in _alertas_fraude:
                            st.warning(_af)

                    # ── CHECK-OUT automático ──
                    _now_co = now_br()
                    _hora_co = _now_co.strftime("%H:%M")
                    _visita_rapida = False
                    if not checkin_hoje.empty and checkin_hoje.iloc[0]["status"] == "em_visita":
                        # Calcula tempo de permanência
                        try:
                            _tin = datetime.strptime(str(checkin_hoje.iloc[0]["hora_entrada"]).strip(), "%H:%M")
                            _tout = _now_co.replace(second=0, microsecond=0)
                            _mins_visita = int((_tout - _tin.replace(year=_now_co.year, month=_now_co.month, day=_now_co.day)).total_seconds() / 60)
                            if _mins_visita < 5:
                                _visita_rapida = True
                                db_exec("INSERT INTO auditoria (data,hora,funcionario,mercado,tipo,detalhe) VALUES(?,?,?,?,?,?)",
                                    (_data_hoje, _hora_co, usuario, merc, "visita_rapida",
                                     f"Tempo: {_mins_visita} min (mínimo: 5 min)"))
                        except: pass
                        db_exec("UPDATE checkin SET hora_saida=?,status=? WHERE id=?",
                                  (_hora_co, "concluido", int(checkin_hoje.iloc[0]["id"])))
                    elif checkin_hoje.empty:
                        db_exec("INSERT INTO checkin (data,hora_entrada,hora_saida,funcionario,mercado,status) VALUES(?,?,?,?,?,?)",
                                  (_data_hoje, _hora_agora, _hora_co, usuario, merc, "concluido"))
                    if _visita_rapida:
                        st.warning(f"⚠️ Visita muito rápida! Menos de 5 minutos registrados em {merc}.")

                    # ── Apaga fotos do disco (já estão no banco em b64) ──
                    for _, rp in prods.iterrows():
                        fp_del = f"fotos/{usuario}/{merc}_{dia_sel}_{rp['produto']}_{today_br()}.jpg".replace(" ","_")
                        try:
                            if os.path.exists(fp_del): os.remove(fp_del)
                        except: pass
                    keys_del = [k for k in st.session_state
                                if merc.replace(" ","_") in k and dia_sel in k]
                    for k in keys_del: del st.session_state[k]

                    # ── WhatsApp automático ao admin com lista de produtos ──
                    _admin_row = db_read("SELECT telefone FROM usuarios WHERE tipo='admin'")
                    _admin_tel = _admin_row.iloc[0]["telefone"] if not _admin_row.empty else ""
                    _badge_wa = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")
                    _pf_wa = f"\n📦 Em falta: {prod_faltante}" if prod_faltante else ""
                    _prods_wa_str = "\n".join(_prods_wa_list)
                    _msg_wa = (
                        f"📋 *Relatório El Kam*\n"
                        f"👤 {usuario.split('.')[0].capitalize()}\n"
                        f"🏪 {merc}\n"
                        f"📅 {today_br().strftime('%d/%m/%Y')}  🕐 Check-out {_hora_co}\n"
                        f"Status: {_badge_wa}{_pf_wa}\n"
                        f"\n📦 *Produtos:*\n{_prods_wa_str}"
                    )
                    if _admin_tel:
                        _wa_m = f"https://wa.me/55{_admin_tel}?text={_up.quote(_msg_wa)}"
                        _wa_p = f"https://web.whatsapp.com/send?phone=55{_admin_tel}&text={_up.quote(_msg_wa)}"
                        st.markdown(
                            f"<div style='background:#0a2b14;border:1px solid #25D36633;border-radius:10px;"
                            f"padding:12px 16px;margin:10px 0'>"
                            f"<div style='color:#22c55e;font-size:12px;font-weight:700;margin-bottom:8px'>"
                            f"📲 Relatório enviado! Toque para avisar o admin</div>"
                            f"<div style='display:flex;gap:8px'>"
                            f"<a href='{_wa_m}' target='_blank' rel='noopener noreferrer' style='flex:1'>"
                            f"<button style='background:#25D366;color:#fff;border:none;border-radius:8px;"
                            f"padding:10px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                            f"📲 Celular</button></a>"
                            f"<a href='{_wa_p}' target='_blank' rel='noopener noreferrer' style='flex:1'>"
                            f"<button style='background:#128C7E;color:#fff;border:none;border-radius:8px;"
                            f"padding:10px;font-size:12px;font-weight:700;cursor:pointer;width:100%'>"
                            f"💻 PC</button></a>"
                            f"</div></div>", unsafe_allow_html=True)

                    badge = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")
                    if status_val == "abastecido":
                        st.markdown(f"""
                        <div style='background:linear-gradient(135deg,#0a2b14,#0d3a1a);
                                    border:1px solid #22c55e44;border-radius:16px;
                                    padding:24px;text-align:center;animation:fadeIn 0.4s ease;
                                    margin-top:12px'>
                            <div style='font-size:48px;margin-bottom:12px'>🏆</div>
                            <div style='color:#22c55e;font-size:18px;font-weight:900;margin-bottom:8px'>
                                Gôndola abastecida! Check-out {_hora_co}</div>
                            <div style='color:#555;font-size:14px;line-height:1.8'>
                                Excelente trabalho, <b style='color:#aaa'>{nome_exib}</b>! 💪<br>
                                A El Kam valoriza cada visita sua.<br>
                                Continue assim — você faz a diferença! 🌟
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.success(f"✅ Relatório de {merc} enviado! Check-out: {_hora_co}  {badge}")

            if st.button("📄 Gerar PDF / WhatsApp", key=f"pdf_{merc}_{dia_sel}",
                         disabled=not confirmado, use_container_width=True):
                status_val = status_opcoes[status_sel]
                badge = {"abastecido":"✅ Abastecido","falta":"⚠️ Produto em falta","fechado":"❌ Loja fechada"}.get(status_val,"")

                # Coleta caminhos das fotos ANTES de apagar
                fotos_paths = [
                    fp for _, r in prods.iterrows()
                    for fp in [f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{today_br()}.jpg".replace(' ','_')]
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
                    for fp in [f"fotos/{usuario}/{merc}_{dia_sel}_{r['produto']}_{today_br()}.jpg".replace(' ','_')]
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
                <div class='card'><div class='label'>Data</div><div class='value'>{today_br().strftime('%d/%m/%Y')} ({dia_sel})</div></div>
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
                # Relatório salvo no banco — admin faz download pelo painel
                import urllib.parse
                dests_f = db_read("SELECT * FROM destinatarios")
                msg_rel = (f"📋 *Relatório El Kam*\n👤 {usuario}\n🏪 {merc}\n"
                           f"📅 {today_br().strftime('%d/%m/%Y')}\nStatus: {badge}")
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
                    now = now_br()
                    db_exec("INSERT INTO chat (data,hora,remetente,tipo,mensagem,lido) VALUES(?,?,?,?,?,?)",
                              (str(now.date()), now.strftime("%H:%M"), usuario, "funcionario", msg_f.strip(), 0))
                    # auto-committed; st.rerun()
