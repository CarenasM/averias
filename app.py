import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN ---
EXCEL_FILE = "averias.xlsx"
SHEET_NAME = "i-SAT"
PASSWORD = "FuckingM@sta"

st.set_page_config(page_title="Waldner SAT - Buscador Final", layout="centered")

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("Averias Sat-Waldner")
    # Firma directamente debajo del título de login
    st.markdown("<p style='color: gray; font-size: 14px; margin-top: -20px;'>By C@renasM</p>", unsafe_allow_html=True)
    
    pass_input = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if pass_input == PASSWORD:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Incorrecto")
    st.stop()

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    if not os.path.exists(EXCEL_FILE):
        return None
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = [c.strip().lower() for c in df.columns]
    return df.astype(str)

df = cargar_datos()

if df is None:
    st.error(f"Error: No se halla {EXCEL_FILE}")
    st.stop()

# --- INTERFAZ ---
st.title("🔎 Waldner SAT")
# Firma directamente debajo del título principal
st.markdown("<p style='color: gray; font-size: 14px; margin-top: -20px;'>By C@renasM</p>", unsafe_allow_html=True)
st.markdown("---") # Una línea divisoria para separar el título del contenido

# MODO CASCADA
st.subheader("MODO CASCADA")
controladores = sorted(df["controlador"].unique())
controlador = st.selectbox("1. Selecciona Controlador:", [""] + controladores)

if controlador:
    df_m = df[df["controlador"] == controlador]
    modelos = sorted(df_m["modelo"].unique())
    modelo = st.selectbox("2. Selecciona Modelo:", [""] + modelos)
    
    if modelo:
        df_s = df_m[df_m["modelo"] == modelo]
        sintomas = sorted(df_s["sintoma"].unique())
        sintoma = st.selectbox("3. Selecciona Síntoma:", [""] + sintomas)
        
        if sintoma:
            res = df_s[df_s["sintoma"] == sintoma]
            for _, row in res.iterrows():
                st.success(f"**SOLUCIÓN:**\n\n{row['experiencia']}")

st.divider()

# BUSCADOR LIBRE
st.subheader("BUSCADOR LIBRE")
texto = st.text_input("Buscador Rápido (palabra clave)")

if len(texto) > 1:
    mask = df["sintoma"].str.contains(texto, case=False, na=False)
    resultados = df[mask].head(5)
    if not resultados.empty:
        for _, row in resultados.iterrows():
            with st.expander(f"• {row['sintoma'].upper()}"):
                st.write(f"**SOL:** {row['experiencia']}")
    else:
        st.warning("No hay coincidencias")
