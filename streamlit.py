import pandas as pd
import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# =============================================================================
# Usamos un layout 'wide' para aprovechar todo el ancho de la pantalla.
st.set_page_config(
    page_title="Análisis de Acceso a Salud en Perú",
    page_icon="🏥",
    layout="wide"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS (OPCIONAL)
# =============================================================================
# Inyectamos CSS para cambiar colores y estilos de la app.
st.markdown("""
<style>
    /* Color de fondo principal */
    .stApp {
        background-color: #F0F2F6;
    }
    /* Estilo de los títulos */
    h1, h2 {
        color: #1A5276;
        font-weight: bold;
    }
    /* Estilo para las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A5276;
        color: white;
    }
</style>""", unsafe_allow_html=True)


# =============================================================================
# CONFIGURACIÓN DE RUTAS (¡IMPORTANTE!)
# =============================================================================
# Este código asume la siguiente estructura de carpetas:
#
# tu_proyecto/
# ├── data/
# │   ├── IPRESS.csv
# │   ├── CCPP_IGN100K.shp  (y los otros archivos del shapefile)
# │   └── DISTRITOS.shp     (y los otros archivos del shapefile)
# ├── outputs/
# │   ├── mapa_proximidad_Lima.html
# │   ├── ... (todos tus mapas HTML)
# └── app_accesibilidad.py  (este mismo archivo)
#
# Simplemente coloca tus carpetas 'data' y 'outputs' al mismo nivel que este script.

try:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    OUTPUTS_DIR = BASE_DIR / "outputs"

    # Verificar si los directorios existen
    if not DATA_DIR.exists() or not OUTPUTS_DIR.exists():
        st.warning("⚠️ ¡Atención! Asegúrate de que las carpetas 'data' y 'outputs' existan al mismo nivel que este script.")

except NameError:
    # Fallback para cuando el script se ejecuta en entornos donde __file__ no está definido
    BASE_DIR = Path.cwd()
    DATA_DIR = BASE_DIR / "data"
    OUTPUTS_DIR = BASE_DIR / "outputs"


# =============================================================================
# FUNCIONES DE CARGA DE DATOS (CON CACHING)
# =============================================================================
# Usamos @st.cache_data para que Streamlit no recargue los archivos pesados cada vez.
@st.cache_data
def load_data(file_path, file_type):
    """Función genérica para cargar datos CSV o Shapefiles."""
    if not file_path.exists():
        st.error(f"❌ Archivo no encontrado en: {file_path}")
        return None
    try:
        if file_type == 'csv':
            return pd.read_csv(file_path, encoding="latin-1")
        elif file_type == 'shp':
            return gpd.read_file(file_path)
    except Exception as e:
        st.error(f"Error al leer el archivo {file_path.name}: {e}")
    return None

def show_map(filename, height=650):
    """Carga y muestra un archivo de mapa HTML desde la carpeta /outputs/."""
    html_path = OUTPUTS_DIR / filename
    if not html_path.exists():
        st.error(f"❌ Mapa no encontrado: {html_path}. ¿Generaste los mapas en la carpeta 'outputs'?")
        return
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=height, scrolling=True)
    except Exception as e:
        st.error(f"No se pudo cargar el mapa {filename}: {e}")

# =============================================================================
# TÍTULO Y DESCRIPCIÓN PRINCIPAL
# =============================================================================
st.title("🏥 Radiografía del Acceso a la Salud en Perú")
st.markdown("Una exploración geoespacial sobre la distribución y cercanía de los centros de salud a nivel nacional.")
st.markdown("---")

# =============================================================================
# CARGA INICIAL DE DATOS
# =============================================================================
hospitals = load_data(DATA_DIR / "IPRESS.csv", 'csv')
centros_poblados = load_data(DATA_DIR / "CCPP_IGN100K.shp", 'shp')
distritos = load_data(DATA_DIR / "DISTRITOS.shp", 'shp')

# =============================================================================
# ESTRUCTURA DE PESTAÑAS
# =============================================================================
tab1, tab2, tab3 = st.tabs([
    "🔎 **Fuentes de Datos**",
    "🏙️ **Análisis Regional**",
    "🌐 **Explorador Interactivo**"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: FUENTES DE DATOS
# -----------------------------------------------------------------------------
with tab1:
    st.header("Explorando los Cimientos del Análisis")
    st.markdown("""
    Para entender la accesibilidad a la salud, combinamos tres fuentes de datos geoespaciales clave que nos permiten construir una imagen completa del panorama peruano.
    
    - **🏥 Establecimientos de Salud (IPRESS):** Contiene la ubicación y características de los centros de salud públicos registrados por el MINSA. Es la base para medir la oferta sanitaria.
    - **🏡 Centros Poblados (CCPP):** El Directorio Nacional de Centros Poblados nos ayuda a identificar dónde vive la gente, un factor crucial para evaluar si los servicios están cerca de las comunidades.
    - **📍 Límites Distritales:** La cartografía oficial de distritos nos sirve como marco para agregar y comparar datos a nivel territorial, revelando desigualdades entre diferentes zonas del país.
    """)

    if hospitals is not None:
        st.subheader("Dataset de Establecimientos de Salud (IPRESS)")
        st.dataframe(hospitals.head(10), use_container_width=True)
        st.info(f"**Total de registros encontrados:** {len(hospitals):,} establecimientos de salud.")

    if centros_poblados is not None:
        st.subheader("Directorio Nacional de Centros Poblados")
        st.dataframe(centros_poblados.head(10), use_container_width=True)
        st.info(f"**Total de registros encontrados:** {len(centros_poblados):,} centros poblados.")

    if distritos is not None:
        st.subheader("Cartografía Nacional de Distritos")
        st.dataframe(distritos.head(10), use_container_width=True)
        st.info(f"**Total de registros encontrados:** {len(distritos):,} distritos.")

# -----------------------------------------------------------------------------
# PESTAÑA 2: ANÁLISIS REGIONAL
# -----------------------------------------------------------------------------
with tab2:
    st.header("Análisis Comparativo: Lima vs. Loreto")
    st.markdown("Los mapas a continuación revelan las profundas diferencias en la distribución de la infraestructura sanitaria entre la capital urbana y una de las regiones más extensas de la Amazonía.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Concentración Urbana en Lima")
        show_map("Lima_hospitales_buffer_analysis.html")
        st.markdown("""
        **Observación:** En Lima, los hospitales se aglomeran en los distritos con mayor densidad poblacional y conectividad vial. Esto crea un núcleo de alta accesibilidad, aunque la calidad y especialización de los centros puede variar.
        """)

    with col2:
        st.subheader("Dispersión Amazónica en Loreto")
        show_map("Loreto_hospitales_buffer_analysis.html")
        st.markdown("""
        **Observación:** La geografía de Loreto impone un reto mayúsculo. Los servicios se concentran en Iquitos, dejando vastas áreas, especialmente comunidades ribereñas, con un acceso extremadamente limitado a la atención médica.
        """)

    st.markdown("---")
    st.subheader("Distribución Nacional de Hospitales por Distrito")
    show_map("mapa_hospitales_distrital_nacional.html")
    st.markdown("""
    **Análisis General:** Este mapa a nivel nacional subraya la desigualdad territorial. Mientras la costa y las principales ciudades andinas muestran una mayor densidad de servicios, la sierra rural y la selva enfrentan un déficit crónico de infraestructura sanitaria.
    """)

# -----------------------------------------------------------------------------
# PESTAÑA 3: EXPLORADOR INTERACTIVO DE PROXIMIDAD
# -----------------------------------------------------------------------------
with tab3:
    st.header("¿Qué tan cerca está el hospital más cercano?")
    st.markdown("Estos mapas interactivos utilizan buffers de 10 km alrededor de los centros poblados para simular áreas de cobertura y visualizar las brechas de acceso de manera más clara.")

    st.subheader("Cobertura y Proximidad en Lima Metropolitana")
    show_map("mapa_proximidad_Lima.html")
    st.markdown("""
    **Interpretación:** En Lima, los círculos de cobertura se superponen constantemente, indicando que la mayoría de la población vive a menos de 10 km de múltiples centros de salud. El desafío aquí es menos la distancia y más la congestión o la capacidad de los servicios.
    """)

    st.subheader("Aislamiento y Distancia en Loreto")
    show_map("mapa_proximidad_Loreto.html")
    st.markdown("""
    **Interpretación:** El panorama en Loreto es el opuesto. Grandes "vacíos" entre los círculos de cobertura demuestran que para muchas comunidades, el centro de salud más cercano está a varias horas o incluso días de viaje, usualmente por vía fluvial.
    """)

    st.markdown("---")
    st.subheader("💡 Conclusiones Clave")
    st.success("""
    - **La geografía es destino:** El acceso a la salud en Perú está profundamente marcado por la geografía, creando una brecha entre las zonas urbanas conectadas y las rurales aisladas.
    - **Más allá de la construcción:** El análisis revela que no solo se trata de construir más hospitales, sino de planificar estratégicamente su ubicación para cerrar las brechas más críticas.
    - **Herramientas para la acción:** Visualizaciones como esta son fundamentales para que los gestores públicos puedan identificar áreas prioritarias y diseñar políticas de salud más equitativas y efectivas.
    """)
