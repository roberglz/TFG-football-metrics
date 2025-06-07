import streamlit as st
from interfaz.sidebar import construir_sidebar
from interfaz.visualizaciones import mostrar_metricas,mostrar_evolucion,mostrar_clustering
from servicios.procesa_partidos import cargar_partido, calcular_metricas
from servicios.estudiar_evolucion import metricas_evolucion
from servicios.grafo_similitud import generar_grafo


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
    grupo_metrica_jugador_seleccionado,
    pulsa_evolucion,
    seleccion_jugador_grafo,
    N_jugadores_cercanos,
    metricas_grafo,
    pulsa_generar_grafo,
    pulsa_clustering
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
        st.info("Estudiando evolución...")
        resultados_evol = metricas_evolucion(id_jugador_seleccionado,metrica_jugador_seleccionada,grupo_metrica_jugador_seleccionado)
        st.info("Estudio finalizado con éxito")
        mostrar_evolucion(resultados_evol,metrica_jugador_seleccionada)
        pass



# -- Generación de grafo de similitud -- 
if pulsa_generar_grafo:
    if not metricas_grafo:
        st.warning("¡Seleccione una o varias metricas!")
    else:
        st.info("Generando grafo...")
        generar_grafo(seleccion_jugador_grafo,metricas_grafo,N_jugadores_cercanos)


# -- Clustering -- 
if pulsa_clustering:
    mostrar_clustering()