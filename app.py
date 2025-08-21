import streamlit as st
import pandas as pd
import plotly.express as px

# Título y descripción
st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("📊 Mi Dashboard de Datos")
st.write("Carga un archivo CSV y explora tus datos de forma interactiva.")

# Carga de datos: subido o de ejemplo
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Datos cargados desde tu archivo")
else:
    st.info("ℹ️ Cargando datos de ejemplo")
    df = pd.read_csv("data/sample.csv")

# Vista de datos y estadísticas
st.subheader("🔍 Vista de datos")
st.dataframe(df)

st.subheader("📊 Estadísticas descriptivas")
stats = df.select_dtypes("number").describe().T
st.table(stats)

# Gráfico de medias por columna numérica
means = df.select_dtypes("number").mean().reset_index()
means.columns = ["columna", "media"]
st.subheader("📈 Media por columna numérica")
fig_bar = px.bar(means, x="columna", y="media", title="Media de cada columna")
st.plotly_chart(fig_bar, use_container_width=True)
