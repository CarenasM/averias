import streamlit as st
import pandas as pd
from io import BytesIO

# =====================
# Configuración inicial
# =====================
REQUIRED_COLS = ["controlador", "modelo", "sintoma", "experiencia"]

st.set_page_config(
    page_title="Buscador de Averías",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔎 Buscador de Averías")
st.markdown("---")

# =====================
# Cargar datos
# =====================
uploaded_file = st.file_uploader(
    "📂 Sube tu archivo Excel con la tabla de averías",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Sube un archivo Excel (.xlsx) para comenzar la búsqueda.")
    st.stop()

try:
    df = pd.read_excel(BytesIO(uploaded_file.getvalue()))
    
    # Normalizar columnas
    df.columns = df.columns.astype(str).str.strip().str.lower()
    
    # Verificar columnas requeridas
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        st.error(f"⚠️ El archivo no contiene todas las columnas requeridas. Faltan: {', '.join(missing_cols)}")
        st.stop()
    
    st.success("✅ Datos cargados correctamente")
    
    if st.checkbox("Mostrar previsualización de datos"):
        st.dataframe(df.head(), use_container_width=True)

except Exception as e:
    st.error(f"❌ Error al procesar el archivo: {e}")
    st.stop()

# =====================
# Selector de modo de búsqueda
# =====================
st.subheader("Modo de Búsqueda")
modo = st.radio(
    "Elige cómo quieres buscar:",
    ["Por palabra clave (sintoma)", "Por cascada"],
    horizontal=True
)
st.markdown("---")

# =====================
# Búsqueda por palabra clave
# =====================
if modo == "Por palabra clave (sintoma)":
    palabra = st.text_input("✍️ Escribe una palabra clave (buscará en la columna 'sintoma'):")

    if palabra:
        resultados = df[df["sintoma"].str.contains(palabra, case=False, na=False)]
        if not resultados.empty:
            st.success(f"Se encontraron {len(resultados)} coincidencias para '{palabra}':")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.warning("No se encontraron coincidencias.")

# =====================
# Búsqueda en cascada
# =====================
elif modo == "Por cascada":
    st.header("🌳 Búsqueda en cascada")

    def get_options(df_filtered, column):
        return sorted([c for c in df_filtered[column].dropna().unique().tolist() if c])

    filtro_df = df.copy()

    controlador = st.selectbox("1️⃣ Selecciona Controlador:", [""] + get_options(filtro_df, "controlador"))
    if controlador:
        filtro_df = filtro_df[filtro_df["controlador"] == controlador]

        modelo = st.selectbox("2️⃣ Selecciona Modelo:", [""] + get_options(filtro_df, "modelo"))
        if modelo:
            filtro_df = filtro_df[filtro_df["modelo"] == modelo]

            sintoma = st.selectbox("3️⃣ Selecciona Síntoma:", [""] + get_options(filtro_df, "sintoma"))
            if sintoma:
                filtro_df = filtro_df[filtro_df["sintoma"] == sintoma]

                experiencia = st.selectbox("4️⃣ Selecciona Experiencia:", [""] + get_options(filtro_df, "experiencia"))
                if experiencia:
                    filtro_df = filtro_df[filtro_df["experiencia"] == experiencia]

    if not filtro_df.empty and (controlador or modelo or sintoma or experiencia):
        st.success("📌 Resultados filtrados:")
        st.dataframe(filtro_df, use_container_width=True)
