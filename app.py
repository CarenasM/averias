import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
EXCEL_FILE = "averias.xlsx"
PASSWORD = "FuckingM@sta"

st.set_page_config(page_title="Waldner SAT - Buscador Final", layout="centered")

# --- SELECTOR DE IDIOMA ---
if "idioma" not in st.session_state:
    st.session_state["idioma"] = None

if st.session_state["idioma"] is None:
    st.title("Averias Sat-Waldner")
    st.subheader("Seleccione su idioma / Select your language")
    col_es, col_en = st.columns(2)
    with col_es:
        if st.button("Español 🇪🇸", use_container_width=True):
            st.session_state["idioma"] = "es"
            st.rerun()
    with col_en:
        if st.button("English 🇬🇧", use_container_width=True):
            st.session_state["idioma"] = "en"
            st.rerun()
    st.stop()

# --- DICCIONARIO DE TRADUCCIÓN ---
if st.session_state["idioma"] == "es":
    CONF = {
        "sheet": "i-SAT",
        "login_t": "Averias Sat-Waldner",
        "pass_l": "Contraseña",
        "btn_login": "Entrar",
        "error_p": "Incorrecto",
        "main_t": "🔎 Waldner SAT",
        "cascada_t": "MODO CASCADA",
        "libre_t": "BUSCADOR LIBRE",
        "sel_c": "1. Selecciona Controlador:",
        "sel_m": "2. Selecciona Modelo:",
        "sel_s": "3. Selecciona Síntoma:",
        "sol_t": "SOLUCIÓN",
        "place_h": "Buscador Rápido (palabra clave)",
        "no_res": "No hay coincidencias",
        "back_b": "Cambiar Idioma / Change Language",
        "col_c": "controlador",
        "col_m": "modelo",
        "col_s": "sintoma",
        "col_e": "experiencia"
    }
else:
    CONF = {
        "sheet": "i-SAT-EN",
        "login_t": "Waldner SAT Faults",
        "pass_l": "Password",
        "btn_login": "Login",
        "error_p": "Incorrect",
        "main_t": "🔎 Waldner SAT",
        "cascada_t": "CASCADE MODE",
        "libre_t": "FREE SEARCH",
        "sel_c": "1. Select Controller:",
        "sel_m": "2. Select Model:",
        "sel_s": "3. Select Symptom:",
        "sol_t": "SOLUTION",
        "place_h": "Quick Search (keyword)",
        "no_res": "No matches found",
        "back_b": "Cambiar Idioma / Change Language",
        "col_c": "controller", 
        "col_m": "model",
        "col_s": "symptom",
        "col_e": "experience"
    }

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title(CONF["login_t"])
    st.markdown("<p style='color: gray; font-size: 14px; margin-top: -20px;'>By C@renasM</p>", unsafe_allow_html=True)
    
    pass_input = st.text_input(CONF["pass_l"], type="password")
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button(CONF["btn_login"]):
            if pass_input == PASSWORD:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error(CONF["error_p"])
    with c2:
        if st.button(CONF["back_b"]):
            st.session_state["idioma"] = None
            st.rerun()
    st.stop()

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos(sheet):
    if not os.path.exists(EXCEL_FILE): return None
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
        # Limpieza de nombres de columnas
        df.columns = [c.strip().lower() for c in df.columns]
        # Limpieza de espacios en todo el contenido de texto del Excel
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df.astype(str)
    except: return None

df = cargar_datos(CONF["sheet"])

if df is None:
    st.error(f"Error: Sheet '{CONF['sheet']}' not found in {EXCEL_FILE}")
    if st.button("Reset"):
        st.session_state["idioma"] = None
        st.rerun()
    st.stop()

# --- INTERFAZ ---
st.title(CONF["main_t"])
st.markdown("<p style='color: gray; font-size: 14px; margin-top: -20px;'>By C@renasM</p>", unsafe_allow_html=True)
st.markdown("---")

# MODO CASCADA
st.subheader(CONF["cascada_t"])
ctrls = sorted(df[CONF["col_c"]].unique())
sel_ctrl = st.selectbox(CONF["sel_c"], [""] + ctrls)

if sel_ctrl:
    df_m = df[df[CONF["col_c"]] == sel_ctrl]
    mods = sorted(df_m[CONF["col_m"]].unique())
    sel_mod = st.selectbox(CONF["sel_m"], [""] + mods)
    
    if sel_mod:
        df_s = df_m[df_m[CONF["col_m"]] == sel_mod]
        sints = sorted(df_s[CONF["col_s"]].unique())
        sel_sint = st.selectbox(CONF["sel_s"], [""] + sints)
        
        if sel_sint:
            # Filtramos todas las filas que coinciden
            res = df_s[df_s[CONF["col_s"]] == sel_sint]
            
            # Obtenemos soluciones únicas para evitar las 2 repetidas que mencionas
            soluciones_unicas = res[CONF["col_e"]].unique()
            
            for i, sol in enumerate(soluciones_unicas, 1):
                st.success(f"**{CONF['sol_t']} #{i}:**\n\n{sol}")

st.divider()

# BUSCADOR LIBRE
st.subheader(CONF["libre_t"])
texto = st.text_input(CONF["place_h"])

if len(texto) > 1:
    mask = df[CONF["col_s"]].str.contains(texto, case=False, na=False)
    # Aquí también aplicamos unique() por si el buscador rápido arroja duplicados
    resultados = df[mask].drop_duplicates(subset=[CONF["col_e"]]).head(5)
    
    if not resultados.empty:
        for _, row in resultados.iterrows():
            with st.expander(f"• {row[CONF['col_s']].upper()}"):
                st.write(f"**SOL:** {row[CONF['col_e']]}")
    else:
        st.warning(CONF["no_res"])

# BOTÓN EN LA BARRA LATERAL
if st.sidebar.button("Logout / Change Language"):
    st.session_state["autenticado"] = False
    st.session_state["idioma"] = None
    st.rerun()
