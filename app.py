import streamlit as st
from interfaz.sidebar import construir_sidebar
from interfaz.visualizaciones import mostrar_metricas
from servicios.procesa_partidos import cargar_partido, calcular_metricas

# Configuración de la página

st.set_page_config(page_title="App", layout="wide")
st.title("TFG-FOOTBALL-METRICS")



# Construcción de la barra lateral

ruta, seleccion, calcular = construir_sidebar()


# Ejecución del análisis al pulsar el botón

if ruta and seleccion and calcular:
    st.info(f"Procesando partido...")
    data = cargar_partido(ruta)
    resultados = calcular_metricas(data, seleccion)
    mostrar_metricas(resultados)  # a estudiar dicha impl

elif calcular and not seleccion:
    st.warning("Selecciona al menos una métrica para calcular.")