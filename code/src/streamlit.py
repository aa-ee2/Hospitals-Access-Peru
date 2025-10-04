import os
import pandas as pd
import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------
# CONFIGURACIÓN DE LA APP
# -------------------------------------------
st.set_page_config(
    page_title="Accesibilidad a Hospitales en el Perú",
    layout="wide"
)

# TÍTULO PRINCIPAL
st.title("🏥 Accesibilidad a Hospitales en el Perú")
st.caption("Análisis geoespacial de la distribución y accesibilidad hospitalaria a nivel nacional")

# Directorio base del proyecto (2 niveles arriba de este script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -------------------------------------------
# FUNCIONES DE CARGA
# -------------------------------------------
def load_hospitals():
    """Carga el dataset de hospitales (CSV en raíz)."""
    try:
        filepath = os.path.join(BASE_DIR, "IPRESS.csv")
        return pd.read_csv(filepath, encoding="latin-1")
    except Exception as e:
        st.error(f"Error cargando hospitales: {e}")
        return None

def load_centros_poblados():
    """Carga el shapefile de centros poblados."""
    try:
        filepath = os.path.join(BASE_DIR, "code", "bases", "CCPP_0", "CCPP_IGN100K.shp")
        return gpd.read_file(filepath)
    except Exception as e:
        st.warning(f"No se pudo cargar centros poblados: {e}")
        return None

def load_distritos():
    """Carga el shapefile distrital."""
    try:
        filepath = os.path.join(BASE_DIR, "code", "bases", "Distritos", "DISTRITOS.shp")
        return gpd.read_file(filepath)
    except Exception as e:
        st.warning(f"No se pudo cargar distritos: {e}")
        return None

# -------------------------------------------
# FUNCIÓN PARA MOSTRAR MAPAS HTML
# -------------------------------------------
def show_map(filename, height=600):
    """Carga y muestra un archivo HTML de mapa desde /outputs/"""
    html_path = os.path.join(BASE_DIR, "outputs", filename)
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=height, scrolling=True)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {html_path}")

# -------------------------------------------
# CARGA DE DATOS
# -------------------------------------------
hospitals = load_hospitals()
centros = load_centros_poblados()
distritos = load_distritos()

# -------------------------------------------
# PESTAÑAS
# -------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Descripción de Datos",
    "🗺️ Mapas Estáticos y Análisis Departamental",
    "🌍 Mapas Dinámicos"
])

# TAB 1 - DESCRIPCIÓN DE DATOS
with tab1:
    st.header("📊 Descripción de los Datos")
    st.markdown("""
    Esta sección presenta las **fuentes de información** que sirven de base para el análisis geoespacial 
    de accesibilidad hospitalaria en el Perú.  
    Se utilizan tres tipos principales de datos:
    
    1. **Datos de hospitales públicos**: contienen información administrativa y georreferenciada 
       de establecimientos de salud operativos registrados por el MINSA – IPRESS.  
    2. **Directorio Nacional de Centros Poblados**: delimita la ubicación y extensión de los centros poblados 
       a nivel nacional, permitiendo contextualizar la accesibilidad hospitalaria en función de la población y el territorio.  
    3. **Límites distritales oficiales**: provienen de la cartografía censal nacional y sirven para realizar 
       análisis espaciales comparativos por distrito y departamento.

    A partir de estos datos se construyen los mapas que permiten visualizar la **concentración, dispersión y brechas 
    de cobertura hospitalaria** en diferentes regiones del país.
    """)

    if hospitals is not None:
        st.subheader("📋 Dataset de Hospitales (MINSA – IPRESS)")
        st.dataframe(hospitals.head(10))
        st.write(f"**Total de registros:** {len(hospitals)} establecimientos")

    if centros is not None:
        st.subheader("🏘️ Directorio Nacional de Centros Poblados")
        st.dataframe(centros.head(10))
        st.write(f"**Total de registros:** {len(centros)} centros poblados")

    if distritos is not None:
        st.subheader("🗺️ Límites Distritales a Nivel Nacional")
        st.dataframe(distritos.head(10))
        st.write(f"**Total de registros:** {len(distritos)} distritos")

# TAB 2 - MAPAS ESTÁTICOS
with tab2:
    st.header("🗺️ Mapas Estáticos y Análisis por Departamento")

    st.subheader("📌 Lima Metropolitana – Hospitales")
    show_map("Lima_hospitales_buffer.html")
    st.markdown("""
    **Análisis:** Se observa una alta concentración de establecimientos operativos en la zona urbana de Lima Metropolitana, 
    especialmente en los ejes viales principales y en distritos consolidados. Esta distribución responde a patrones de densidad 
    poblacional y mejor infraestructura vial, lo que implica una mejor accesibilidad relativa respecto a otras regiones.
    """)

    st.subheader("🌿 Loreto – Hospitales")
    show_map("Loreto_hospitales_buffer.html")
    st.markdown("""
    **Análisis:** Los hospitales en Loreto presentan una distribución más dispersa, concentrándose principalmente en la ciudad de Iquitos. 
    Se evidencian extensas áreas rurales y amazónicas sin presencia hospitalaria cercana, lo que refleja brechas estructurales en la oferta sanitaria.
    """)

    st.subheader("🏢 Distribución Distrital de Hospitales")
    show_map("mapa_hospitales_distrital.html")
    st.markdown("""
    **Análisis:** Este mapa permite visualizar desigualdades territoriales en la oferta hospitalaria por distritos, destacando zonas con alta densidad 
    de infraestructura frente a otras con marcada carencia, especialmente en la Amazonía y zonas andinas.
    """)

# TAB 3 - MAPAS DINÁMICOS
with tab3:
    st.header("🌍 Mapas Dinámicos con Folium")

    st.subheader("📍 Proximidad de Hospitales en Lima Metropolitana")
    show_map("mapa_proximidad_Lima.html")
    st.markdown("""
    **Análisis:** Se visualizan buffers de accesibilidad hospitalaria en Lima que muestran una cobertura densa en zonas urbanas, 
    con redundancia de servicios y buena conectividad. Las zonas periféricas, aunque menos densas, aún presentan cierto acceso cercano.
    """)

    st.subheader("📍 Proximidad de Hospitales en Loreto")
    show_map("mapa_proximidad_Loreto.html")
    st.markdown("""
    **Análisis:** En Loreto, los buffers muestran grandes áreas sin cobertura cercana, especialmente en zonas ribereñas y de la Amazonía profunda. 
    Esto evidencia importantes brechas en infraestructura y accesibilidad, que podrían orientar futuras inversiones públicas.
    """)

    # Sección final opcional de conclusiones generales
    st.subheader("📌 Conclusiones Generales")
    st.markdown("""
    - La accesibilidad hospitalaria presenta **fuertes contrastes territoriales** entre Lima Metropolitana y regiones como Loreto.  
    - Lima concentra gran parte de la infraestructura hospitalaria, favorecida por su urbanización y red vial consolidada.  
    - Loreto, en cambio, refleja las dificultades geográficas y de planificación sanitaria para alcanzar una cobertura equitativa.  
    - Los mapas permiten identificar zonas críticas para la **priorización de políticas públicas y expansión de servicios de salud**.
    """)