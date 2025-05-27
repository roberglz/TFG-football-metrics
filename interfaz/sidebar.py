import streamlit as st
from servicios.visualizar_partidos import listar_partidos

def construir_sidebar():
    """
    Construye el menú lateral: selector de partido y checkboxes de métricas.
    Devuelve la ruta del partido seleccionado y la lista de métricas elegidas.
    """
    partidos = listar_partidos("datos")
    nombres = [p[0] for p in partidos]
    rutas = [p[1] for p in partidos]

    if not nombres:
        st.sidebar.warning("No hay archivos de partido disponibles en la carpeta 'datos'.")
        return None, []

    st.sidebar.header("Selecciona un partido")
    partido_seleccionado = st.sidebar.selectbox("", nombres)
    ruta = rutas[nombres.index(partido_seleccionado)]

    st.sidebar.markdown("---")
    st.sidebar.subheader("Métricas a calcular")
    seleccion = []
    if st.sidebar.checkbox("Potencia metabólica"):
        seleccion.append("potencia")
    if st.sidebar.checkbox("Ritmo de juego"):
        seleccion.append("ritmo")
    if st.sidebar.checkbox("Cambios de dirección"):
        seleccion.append("cambios")
    if st.sidebar.checkbox("Distancia por aceleraciones"):
        seleccion.append("aceleraciones")
    if st.sidebar.checkbox("Umbrales estándar"):
        seleccion.append("umbral_est")
    if st.sidebar.checkbox("Umbrales relativos"):
        seleccion.append("umbral_rel")

    st.sidebar.markdown("---")
    calcular = st.sidebar.button("Calcular métricas")

    return ruta, seleccion, calcular
