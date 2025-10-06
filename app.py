import streamlit as st
import pandas as pd

# =====================
# CONFIGURACIÓN INICIAL
# =====================
EXCEL_FILE = "averias.xlsx"
SHEET_NAME = "i-SAT"
PASSWORD = "FuckingM@sta"  # 🔒 Contraseña de acceso

st.set_page_config(page_title="Buscador de Averías Waldner SAT", layout="wide")
st.title("🔎 Buscador de Averías Waldner SAT")
st.markdown("---")

# =====================
# FUNCIÓN DE CARGA DE DATOS
# =====================
@st.cache_data
def cargar_datos():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = df.columns.str.strip().str.lower()
    return df

# =====================
# BLOQUEO POR CONTRASEÑA
# =====================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.subheader("🔐 Acceso restringido")
    password_input = st.text_input("Introduce la contraseña:", type="password")
    if st.button("Entrar"):
        if password_input == PASSWORD:
            st.session_state["autenticado"] = True
            st.success("✅ Acceso concedido. Bienvenido.")
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta.")
    st.stop()  # 🔒 Detiene la ejecución si no está autenticado

# =====================
# CARGA DE DATOS
# =====================
try:
    df = cargar_datos()
    st.success("Archivo cargado correctamente ✅")
except Exception as e:
    st.error(f"❌ Error al cargar el archivo '{EXCEL_FILE}': {e}")
    st.stop()

# =====================
# SELECTOR DE MODO
# =====================
modo = st.radio(
    "Elige el método de búsqueda:",
    ["Por palabra clave (síntoma)", "Por cascada"],
    index=0,
    horizontal=True
)

st.markdown("---")

# =====================
# MODO 1: PALABRA CLAVE
# =====================
if modo == "Por palabra clave (síntoma)":
    palabra = st.text_input(
        "Escribe una palabra clave para buscar en la columna 'sintoma':",
        placeholder="Ej: error, sensor, ventilador..."
    )

    if palabra:
        resultados = df[df["sintoma"].str.contains(palabra, case=False, na=False)]
        if not resultados.empty:
            st.success(f"🔹 Se encontraron {len(resultados)} coincidencias para '{palabra}':")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.warning("No se encontraron coincidencias.")

# =====================
# MODO 2: CASCADA
# =====================
elif modo == "Por cascada":
    def get_options(df_filtered, column_name):
        options = [c for c in df_filtered[column_name].unique().tolist() if c]
        return sorted(options)

    controladores = get_options(df, "controlador")
    controlador = st.selectbox("1️⃣ Selecciona Controlador:", [""] + controladores)

    filtro_df = df.copy()

    if controlador:
        filtro_df = filtro_df[filtro_df["controlador"] == controlador]
        modelos = get_options(filtro_df, "modelo")
        modelo = st.selectbox("2️⃣ Selecciona Modelo:", [""] + modelos)

        if modelo:
            filtro_df = filtro_df[filtro_df["modelo"] == modelo]
            sintomas = get_options(filtro_df, "sintoma")
            sintoma = st.selectbox("3️⃣ Selecciona Síntoma:", [""] + sintomas)

            if sintoma:
                filtro_df = filtro_df[filtro_df["sintoma"] == sintoma]
                experiencias = get_options(filtro_df, "experiencia")
                experiencia = st.selectbox("4️⃣ Selecciona Experiencia/Solución:", [""] + experiencias)

                if experiencia:
                    resultado_final = filtro_df[filtro_df["experiencia"] == experiencia]
                    st.success("🎯 Resultado final:")
                    st.dataframe(resultado_final, use_container_width=True)


