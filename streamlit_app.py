import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pyarrow.parquet as pq # Necesario para leer .parquet

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Análisis de Hospitales en Perú",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Análisis Geoespacial de Hospitales en Perú")

# --- CREACIÓN DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs([
    "🗂️ Descripción de Datos",
    "🗺️ Mapas Estáticos y Análisis",
    "🌍 Mapas Dinámicos"
])

# --- PESTAÑA 1: DESCRIPCIÓN ---
with tab1:
    st.header("Descripción del Proyecto")
    st.markdown("""
    Este dashboard presenta un análisis de la distribución y acceso a los hospitales públicos operativos en Perú, basado en la tarea del curso.
    **Fuentes de Datos:**
    - **Hospitales:** MINSA - Registro Nacional de IPRESS.
    - **Centros Poblados:** INEI.
    - **Límites Administrativos:** Shapefile de distritos de Perú.
    """)
    st.subheader("Integrantes")
    st.markdown("""
    - Aníbal Daniel Villanueva Hinojosa
    - Bruno Alonso Villacorta Montoya
    - Durqa Valentina Linares Herrera
    - Margarita Mamani Condori
    """)

# --- PESTAÑA 2: ANÁLISIS ESTÁTICO ---
with tab2:
    st.header("Análisis a Nivel Distrital y Departamental")

    st.subheader("Mapas Estáticos de Hospitales por Distrito")
    # Asegúrate de que tus compañeros generen y guarden estas imágenes
    try:
        st.image("outputs/mapa_total_hospitales.png", caption="Mapa 1: Total de hospitales públicos por distrito.")
        st.image("outputs/mapa_distritos_sin_hospitales.png", caption="Mapa 2: Distritos sin hospitales públicos.")
        st.image("outputs/mapa_top_10_distritos.png", caption="Mapa 3: Top 10 distritos con más hospitales.")
    except FileNotFoundError:
        st.warning("Advertencia: Los archivos de mapas estáticos (.png) no se encontraron en la carpeta 'outputs'. Pide a tu equipo que los genere.")

    st.subheader("Análisis por Departamento")
    try:
        # Cargar los datos de departamentos desde el archivo .parquet que ya tienes
        df_deptos = pd.read_parquet("outputs/deptos_enriched.parquet")
        
        st.write("**Tabla Resumen por Departamento**")
        st.dataframe(df_deptos)

        st.write("**Gráfico de Barras por Departamento**")
        # Asumiendo que las columnas se llaman 'NOMBDEP' y 'hospital_count'
        st.bar_chart(df_deptos, x='NOMBDEP', y='hospital_count')

    except FileNotFoundError:
        st.error("Error: No se encontró el archivo 'outputs/deptos_enriched.parquet'.")

# --- PESTAÑA 3: MAPAS DINÁMICOS ---
with tab3:
    st.header("Visualizaciones Geoespaciales Interactivas")

    def mostrar_mapa(ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                mapa_html = f.read()
            components.html(mapa_html, height=600, scrolling=True)
        except FileNotFoundError:
            st.error(f"Error: No se encontró el mapa en la ruta: {ruta_archivo}")

    st.subheader("Mapa Coroplético Nacional y Clúster de Hospitales")
    mostrar_mapa("outputs/mapa_nacional.html")

    st.subheader("Análisis de Proximidad en Lima y Loreto")
    st.write("Círculo verde: zona con mayor concentración de hospitales. Círculo rojo: zona con menor concentración.")
    mostrar_mapa("outputs/mapa_proximidad_lima.html")
    mostrar_mapa("outputs/mapa_proximidad_loreto.html")