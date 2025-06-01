import streamlit as st
from interfaz.sidebar import construir_sidebar
from interfaz.visualizaciones import mostrar_metricas
from servicios.procesa_partidos import cargar_partido, calcular_metricas
# (la importación de funciones individuales queda pendiente)

# Configuración de la página
st.set_page_config(page_title="App", layout="wide")
st.title("TFG-FOOTBALL-METRICS")

# Construcción de la barra lateral
(
    ruta_seleccionada,
    grupo_metricas_seleccionado,
    pulsa_calcular_encuentro,
    id_jugador_seleccionado,
    metrica_jugador_seleccionada,
    pulsa_evolucion,
) = construir_sidebar()



# -- Calculo de métricas físicas por encuentro --
if pulsa_calcular_encuentro:
    if not ruta_seleccionada:
        st.warning("¡Seleccione un partido!")
    elif not grupo_metricas_seleccionado:
        st.warning("¡Seleccione al menos un grupo de métricas!")
    else:
        st.info("Calcundo métricas...")
        data = cargar_partido(ruta_seleccionada)
        resultados_enc = calcular_metricas(data, grupo_metricas_seleccionado)
        mostrar_metricas(resultados_enc)




# -- Visualización de evolución de un jugador -- 
if pulsa_evolucion:
    if not metrica_jugador_seleccionada:
        st.warning("¡Seleccione una metrica!")
    
    else:
        pass