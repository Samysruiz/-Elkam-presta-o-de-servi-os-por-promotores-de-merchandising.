 import streamlit as st
import pandas as pd
from datetime import date
import os

# 1. CONFIGURAÇÃO (Sempre a primeira linha)
st.set_page_config(page_title="EL KAM", layout="centered")

# 2. CSS INTERFACE (Fundo Preto e Detalhes Vermelhos)
st.markdown("""
<style>
.stApp {
    background-color: black;
}
h1, h2, h3, .stSubheader {
    color: #ff2b2b !important;
}
label, p, span {
    color: white !important;
}
.stButton button {
    background-color: #ff2b2b;
    color: white;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 3. LOGO CENTRALIZADO E GRANDE
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    # Ajustado para o caminho real que aparece no seu GitHub
    logo_path = "logotipo/el_kam_logo.png" 
    
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("Aguardando carregamento do sistema...")

st.divider()
import os

st.write(os.listdir())
st.write(os.listdir("logotipo"))

# ---------------- DADOS E LOGIN CONTINUAM ABAIXO ----------------
