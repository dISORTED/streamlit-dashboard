import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("📊 Mi Dashboard de Datos")

# --- Sidebar de configuración ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.selectbox("Fuente de datos", ["Ejemplo (CSV)", "Base de datos"])
    if modo == "Ejemplo (CSV)":
        uploaded_file = st.file_uploader("Sube un CSV", type="csv")
    else:
        uploaded_file = None
    st.write("---")
    st.markdown("ℹ️ Si eliges **Base de datos**, se usará el SQLite en `data/sample.db`.")

# --- Carga de datos según la opción ---
if modo == "Base de datos":
    st.info("🔌 Conectando a la base de datos…")
    engine = create_engine(st.secrets["DB_URL"])
    df = pd.read_sql_table("sample", con=engine)
    st.success(f"✅ Cargadas {len(df)} filas desde la tabla `sample`")
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Datos cargados desde tu archivo")
else:
    st.info("ℹ️ Cargando datos de ejemplo")
    df = pd.read_csv("data/sample.csv")

# --- Métricas clave ---
n_rows, n_cols = df.shape
n_nulls = df.isna().sum().sum()
col1, col2, col3 = st.columns(3)
col1.metric("Filas", n_rows)
col2.metric("Columnas", n_cols)
col3.metric("Valores nulos", n_nulls)

st.markdown("---")

# --- Vista de datos ---
st.subheader("🔍 Vista de datos")
st.dataframe(df)

st.markdown("---")

# --- Estadísticas descriptivas ---
st.subheader("📊 Estadísticas descriptivas")
stats = df.select_dtypes("number").describe().T
st.table(stats)

st.markdown("---")

# --- Gráfico de medias por columna numérica ---
st.subheader("📈 Media por columna numérica")
means = df.select_dtypes("number").mean().reset_index()
means.columns = ["columna", "media"]
fig_bar = px.bar(means, x="columna", y="media", title="Media de cada columna")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- Scatter plot opcional ---
cols = st.multiselect(
    "🔢 (Opcional) Scatter: selecciona dos columnas",
    options=df.select_dtypes("number").columns.tolist(),
    default=df.select_dtypes("number").columns.tolist()[:2]
)
if len(cols) == 2:
    x_col, y_col = cols
    st.subheader(f"Scatter: {y_col} vs {x_col}")
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(fig, use_container_width=True)
