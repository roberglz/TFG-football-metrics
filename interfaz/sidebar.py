import streamlit as st
import json
from servicios.visualizar_partidos import listar_partidos

def construir_sidebar():
    st.sidebar.header("Opciones disponibles:")

    # Pequeña separación antes del primer bloque
    st.sidebar.write("")

    # -- Cálculo por encuentro --
    st.sidebar.subheader("1. Cálculo de métricas físicas por encuentro")

    lista_partidos = listar_partidos()
    opciones = {nombre_legible: ruta for nombre_legible, ruta in lista_partidos}
    seleccion_partido = st.sidebar.selectbox("Selecciona un partido:", list(opciones.keys()))
    ruta_encuentro = opciones.get(seleccion_partido)

    metricas_grupo = {
        "Variables metabólicas": "potencia",
        "Ritmo de juego": "ritmo",
        "Cambios de dirección": "cambios",
        "Aceleraciones": "aceleraciones",
        "Distancias con umbrales estándar": "umbral_est",
        "Distancias con umbrales relativos": "umbral_rel"
    }
    seleccion_encuentro = st.sidebar.multiselect(
        "Seleccione uno o varios grupos de métricas:", list(metricas_grupo.keys()), key="encuentro"
    )
    claves_encuentro = [metricas_grupo[m] for m in seleccion_encuentro]
    calcular_encuentro = st.sidebar.button("Calcular", key="btn_encuentro")

    # Añadimos varias líneas vacías para espaciar los bloques
    st.sidebar.write("")
    st.sidebar.write("")

    # -- Visualización de evolución de un jugador --
    st.sidebar.subheader("2. Evolución de una métrica de un jugador a través de sus encuentros disputados")

    with open("config/dicc_jugadores.json", "r", encoding="utf-8") as f:
        dicc_jugadores = json.load(f)
    jugadores = {nombre: pid for pid, nombre in dicc_jugadores.items()}
    lista_nombres = sorted(jugadores.keys())
    seleccion_jugador_nombre = st.sidebar.selectbox(
        "Seleccione un jugador:", lista_nombres, key="jugador"
    )
    player_id = jugadores.get(seleccion_jugador_nombre)

    metricas_ind = {
        "Variables metabólicas": "potencia",
        "Ritmo de juego": "ritmo",
        "Cambios de dirección": "cambios",
        "Aceleraciones": "aceleraciones",
        "Distancias con umbrales estándar": "umbral_est",
        "Distancias con umbrales relativos": "umbral_rel"
    }
    seleccion_jugador_metricas = st.sidebar.multiselect(
        "Seleccione una métrica específica:", list(metricas_ind.keys()), key="jugador_met"
    )
    claves_jugador = [metricas_ind[m] for m in seleccion_jugador_metricas]
    calcular_jugador = st.sidebar.button("Comenzar estudio", key="btn_jugador")

    return (
        ruta_encuentro,
        claves_encuentro,
        calcular_encuentro,
        player_id,
        claves_jugador,
        calcular_jugador,
    )