import os
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("Dashboard de Datos")

# --- Sidebar de configuración ---
with st.sidebar:
    st.header("Configuración")
    uploaded_file = st.file_uploader(
        "Sube un archivo CSV, Excel o SQLite",
        type=["csv", "xls", "xlsx", "db"]
    )
    st.write("---")
    st.markdown(
        "Si no subes nada, se cargan los datos de ejemplo (CSV).\n\n"
        "Para `.db`, se buscará la tabla `sample` dentro del archivo."
    )

# --- Carga de datos ---
if uploaded_file is not None:
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.success(f"Datos cargados desde CSV: {uploaded_file.name}")
    elif name.endswith((".xls", ".xlsx")):
        df = pd.read_excel(uploaded_file)
        st.success(f"Datos cargados desde Excel: {uploaded_file.name}")
    elif name.endswith(".db"):
        # Guardar el .db subido en disco
        os.makedirs("data", exist_ok=True)
        db_path = os.path.join("data", "uploaded.db")
        with open(db_path, "wb") as f:
            f.write(uploaded_file.read())
        # Conectar y leer tabla 'sample'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        if "sample" not in tables:
            st.error("El archivo .db no contiene la tabla 'sample'.")
            st.stop()
        df = pd.read_sql_query("SELECT * FROM sample", conn)
        conn.close()
        st.success(f"Datos cargados desde SQLite: {uploaded_file.name}")
    else:
        st.error("Formato no soportado")
        st.stop()
else:
    # Datos de ejemplo
    df = pd.read_csv("data/sample.csv")
    st.info("Cargando datos de ejemplo (data/sample.csv)")

# --- Métricas clave ---
n_rows, n_cols = df.shape
n_nulls = df.isna().sum().sum()
col1, col2, col3 = st.columns(3)
col1.metric("Filas", n_rows)
col2.metric("Columnas", n_cols)
col3.metric("Valores nulos", n_nulls)

st.markdown("---")

# --- Vista de datos ---
st.subheader("Vista de datos")
st.dataframe(df)

st.markdown("---")

# --- Estadísticas descriptivas ---
st.subheader("Estadísticas descriptivas")
stats = df.select_dtypes("number").describe().T
st.table(stats)

st.markdown("---")

# --- Gráfico de medias por columna numérica ---
st.subheader("Media por columna numérica")
means = df.select_dtypes("number").mean().reset_index()
means.columns = ["columna", "media"]
fig_bar = px.bar(means, x="columna", y="media", title="Media de cada columna")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- Scatter plot opcional ---
numeric_cols = df.select_dtypes("number").columns.tolist()
cols = st.multiselect(
    "Scatter opcional: selecciona dos columnas numéricas",
    options=numeric_cols,
    default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
)
if len(cols) == 2:
    x_col, y_col = cols
    st.subheader(f"Scatter: {y_col} vs {x_col}")
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(fig, use_container_width=True)
