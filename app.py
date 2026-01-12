import streamlit as st
import pandas as pd
import plotly.express as px

# --- Cargar datos ---
path="gs://datos_excel_dashboard2026/1000-Registros-de-ventas.xlsx"
df = pd.read_excel(path)
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard Interactivo de Ventas")
df

# --- Filtros ---
categorias = df["Categoría"].unique()
zonas = df["Zona"].unique()

categoria_sel = st.sidebar.multiselect("Seleccionar Categoría", categorias, default=categorias)
zona_sel = st.sidebar.multiselect("Seleccionar Zona", zonas, default=zonas)

df_filtrado = df[
    (df["Categoría"].isin(categoria_sel)) &
    (df["Zona"].isin(zona_sel))
]

# --- Métricas principales ---
total_ventas = df_filtrado["Importe venta total"].sum()
total_unidades = df_filtrado["Unidades"].sum()
col1, col2 = st.columns(2)
with col1:
     st.metric("Total Ventas", f"${total_ventas:,.0f}")
with col2:
     st.metric("Unidades Vendidas", f"{total_unidades:,}")

# --- Gráficas ---
col3, col4 = st.columns(2)

with col3:
    fig1 = px.bar(df_filtrado, x="Zona", y="Importe venta total", color="Categoría", title="Ventas por Zona y Categoría")
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    fig2 = px.line(df_filtrado, x="Categoría", y="Importe venta total", color="Categoría",
                  title="Ventas por Categoría")
    st.plotly_chart(fig2, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    fig3 = px.pie(df_filtrado, names="Zona", values="Importe venta total", title="Distribución de Ventas por Zona")
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    top_prod = df_filtrado.groupby("Categoría")["Importe venta total"].sum().nlargest(10).reset_index()
    fig4 = px.bar(top_prod, x="Importe venta total", y="Categoría", orientation="h",
                  title="Top 10 Productos Más Vendidos")
    st.plotly_chart(fig4, use_container_width=True)

st.caption("Dashboard generado con Streamlit y Plotly")


