import streamlit as st
from servicios.visualizar_partidos import listar_partidos

def construir_sidebar():
    st.sidebar.header("Cálculo de grupo de métricas físicas por encuentro")

    lista_partidos = listar_partidos()
    opciones = {nombre_legible: ruta for nombre_legible, ruta in lista_partidos}

    seleccion_partido = st.sidebar.selectbox("Selecciona un partido", list(opciones.keys()))
    ruta = opciones.get(seleccion_partido)

    metricas = {
        "Variables metabólicas": "potencia",
        "Ritmo de juego": "ritmo",
        "Cambios de dirección": "cambios",
        "Aceleraciones": "aceleraciones",
        "Distancias con umbrales estándar": "umbral_est",
        "Distancias con umbrales relativos": "umbral_rel"
    }

    seleccion = st.sidebar.multiselect("Selecciona las métricas a calcular", list(metricas.keys()))
    seleccion_claves = [metricas[metrica] for metrica in seleccion]

    calcular = st.sidebar.button("Calcular métricas")

    return ruta, seleccion_claves, calcular