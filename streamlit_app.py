import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, inspect

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Datos", layout="wide")
st.title("📊 Mi Dashboard de Datos")

# --- Sidebar de configuración ---
with st.sidebar:
    st.header("⚙️ Configuración")
    modo = st.selectbox("Fuente de datos", ["Ejemplo (CSV)", "Base de datos"])
    if modo == "Ejemplo (CSV)":
        uploaded_csv = st.file_uploader("Sube un CSV", type="csv")
        uploaded_db = None
    else:
        uploaded_db = st.file_uploader("Sube un archivo .db", type="db")
        uploaded_csv = None
    st.write("---")
    st.markdown(
        "ℹ️ En **Base de datos**, si no subes `.db`, se usará `data/sample.db`. "
        "Si subes tu `.db`, se leerá esa tabla `sample`."
    )

# --- Carga de datos según la opción ---
if modo == "Base de datos":
    # 1) Preparar carpeta 'data'
    os.makedirs("data", exist_ok=True)

    # 2) Guardar .db subido (si lo hay)
    if uploaded_db is not None:
        with open("data/uploaded.db", "wb") as f:
            f.write(uploaded_db.read())
        db_path = "data/uploaded.db"
    else:
        db_path = "data/sample.db"

    # 3) Crear base y tabla si no existen
    if not os.path.exists(db_path):
        df_csv = pd.read_csv("data/sample.csv")
        eng_init = create_engine(f"sqlite:///{db_path}")
        df_csv.to_sql("sample", eng_init, index=False, if_exists="replace")

    # 4) Conectar y chequear tabla
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    if "sample" not in inspector.get_table_names():
        df_csv = pd.read_csv("data/sample.csv")
        df_csv.to_sql("sample", engine, index=False, if_exists="replace")

    # 5) Leer datos garantizados
    st.info(f"🔌 Conectando a la base de datos: `{db_path}`")
    df = pd.read_sql_query("SELECT * FROM sample", con=engine)
    st.success(f"✅ Cargadas {len(df)} filas desde la tabla `sample`")

elif modo == "Ejemplo (CSV)" and uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.success("✅ Datos cargados desde tu archivo CSV")
else:
    st.info("ℹ️ Cargando datos de ejemplo (CSV)")
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
numeric_cols = df.select_dtypes("number").columns.tolist()
cols = st.multiselect(
    "🔢 Scatter opcional: selecciona dos columnas numéricas",
    options=numeric_cols,
    default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
)
if len(cols) == 2:
    x_col, y_col = cols
    st.subheader(f"🔎 Scatter: {y_col} vs {x_col}")
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(fig, use_container_width=True)
