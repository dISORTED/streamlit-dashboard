import streamlit as st
import pandas as pd
import plotly.express as px

# Título y descripción
st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("📊 Mi Dashboard de Datos")
st.write("Carga un archivo CSV y explora tus datos de forma interactiva.")

# Carga de CSV
uploaded_file = st.file_uploader("➤ Sube un archivo CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Vista de los datos")
    st.dataframe(df)

    # Selección de columnas para gráfico
    cols = st.multiselect(
        "Selecciona dos columnas para graficar",
        options=df.columns.tolist(),
        default=df.columns.tolist()[:2]
    )

    if len(cols) == 2:
        x_col, y_col = cols
        st.subheader(f"Gráfico de dispersión: **{x_col}** vs **{y_col}**")
        fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔢 Selecciona **exactamente** dos columnas para generar el gráfico.")
