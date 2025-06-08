import streamlit as st
from interfaz.sidebar import construir_sidebar
from interfaz.visualizaciones import (
    mostrar_metricas, mostrar_evolucion, mostrar_clustering,
    mostrar_anomalias, mostrar_grafo
)
from servicios.procesa_partidos import cargar_partido, calcular_metricas
from servicios.estudiar_evolucion import metricas_evolucion
from interfaz.paginas import mostrar_portada, mostrar_explicacion  # Importadas

# Configuración de la página
st.set_page_config(page_title="TFG Football Metrics", layout="wide")

# Estado inicial de la app
if "inicio" not in st.session_state:
    st.session_state.inicio = False

# ------------------- PORTADA -------------------
if not st.session_state.inicio:
    mostrar_portada()
    st.stop()

# ------------------- SIDEBAR -------------------
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
    pulsa_clustering,
    pulsa_anomalias,
    id_jugador_anomalia,
) = construir_sidebar()

# ------------------- BLOQUE EXPLICATIVO -------------------
mostrar_explicacion()

# ------------------- CÁLCULO DE MÉTRICAS -------------------
if pulsa_calcular_encuentro:
    st.subheader("📌 Cálculo de métricas por encuentro")
    if not ruta_seleccionada:
        st.warning("¡Seleccione un partido!")
    elif not grupo_metricas_seleccionado:
        st.warning("¡Seleccione al menos un grupo de métricas!")
    else:
        info = st.empty()
        info.info("Cargando datos y generando métricas...")
        data = cargar_partido(ruta_seleccionada)
        resultados_enc = calcular_metricas(data, grupo_metricas_seleccionado)
        info.empty()
        mostrar_metricas(resultados_enc)

# ------------------- EVOLUCIÓN -------------------
if pulsa_evolucion:
    st.subheader("📈 Evolución de un jugador")
    if not metrica_jugador_seleccionada:
        st.warning("¡Seleccione una métrica!")
    else:
        info = st.empty()
        info.info("Estudiando evolución del jugador...")
        resultados_evol = metricas_evolucion(
            id_jugador_seleccionado,
            metrica_jugador_seleccionada,
            grupo_metrica_jugador_seleccionado
        )
        info.empty()
        mostrar_evolucion(resultados_evol, metrica_jugador_seleccionada)
        st.success("Estudio finalizado con éxito")

# ------------------- GRAFO -------------------
if pulsa_generar_grafo:
    st.subheader("🔗 Generación de grafo de similitud")
    if not metricas_grafo:
        st.warning("¡Seleccione una o varias métricas!")
    else:
        mostrar_grafo(seleccion_jugador_grafo, metricas_grafo, N_jugadores_cercanos)
        st.success("Grafo generado con éxito")

# ------------------- CLUSTERING -------------------
if pulsa_clustering:
    st.subheader("🔍 Clustering de jugadores")
    mostrar_clustering()
    st.success("Clustering ejecutado con éxito")

# ------------------- ANOMALÍAS -------------------
if pulsa_anomalias:
    st.subheader("🚨 Detección de anomalías")
    if not id_jugador_anomalia:
        st.warning("Seleccione un jugador:")
    else:
        mostrar_anomalias(id_jugador_anomalia)
        st.success(f"Anomalías del jugador {id_jugador_anomalia} visualizadas correctamente.")
