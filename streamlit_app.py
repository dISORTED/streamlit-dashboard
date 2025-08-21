import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("📊 Mi Dashboard de Datos")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("Sube un CSV", type="csv")
    st.write("---")
    st.markdown("ℹ️ **Dataset de ejemplo**: `data/sample.csv`")

# Carga de datos
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Datos cargados desde tu archivo")
else:
    st.info("ℹ️ Cargando datos de ejemplo")
    df = pd.read_csv("data/sample.csv")

# Métricas clave
n_rows, n_cols = df.shape
n_nulls = df.isna().sum().sum()
col1, col2, col3 = st.columns(3)
col1.metric("Filas", n_rows)
col2.metric("Columnas", n_cols)
col3.metric("Valores nulos", n_nulls)

st.markdown("---")

# Vista de datos
with st.container():
    st.subheader("🔍 Vista de datos")
    st.dataframe(df)

st.markdown("---")

# Estadísticas descriptivas
with st.container():
    st.subheader("📊 Estadísticas descriptivas")
    stats = df.select_dtypes("number").describe().T
    st.table(stats)

# Media por columna
means = df.select_dtypes("number").mean().reset_index()
means.columns = ["columna", "media"]
st.subheader("📈 Media por columna numérica")
fig_bar = px.bar(means, x="columna", y="media", title="Media de cada columna")
st.plotly_chart(fig_bar, use_container_width=True)
