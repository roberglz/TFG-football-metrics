# /interfaz/sidebar.py

import streamlit as st
import json
from servicios.visualizar_partidos import listar_partidos
from utils.agrupacion_metricas import GRUPOS_METRICAS
from servicios.jugadores import cargar_diccionario_jugadores

def construir_sidebar():
    st.sidebar.header("Opciones disponibles:")


    st.sidebar.write("")  


    # -- Cálculo por encuentro -- (igual que antes)
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

    
    
    
    st.sidebar.write("")  






    # -- Visualización de evolución de un jugador --
    st.sidebar.subheader("2. Evolución de una métrica de un jugador a través de sus encuentros")


    dicc_jugadores = cargar_diccionario_jugadores()
    
    
    jugadores = {nombre: pid for pid, nombre in dicc_jugadores.items()}
    lista_nombres = sorted(jugadores.keys())
    seleccion_jugador_nombre = st.sidebar.selectbox(
        "Seleccione un jugador:", lista_nombres, key="jugador"
    )
    player_id = jugadores.get(seleccion_jugador_nombre)

   

    grupos = list(GRUPOS_METRICAS.keys())
    grupo_seleccionado = st.sidebar.selectbox(
        "Elija grupo de métricas:", grupos, key="grupo_met_jugador"
    )

  
    opciones_metricas = GRUPOS_METRICAS[grupo_seleccionado]
    
    etiquetas = list(opciones_metricas.keys())
    claves = list(opciones_metricas.values())

    
    seleccion_etiqueta = st.sidebar.selectbox(
        f"Métricas de «{grupo_seleccionado}»:",
        etiquetas,
        key="met_jugador"
    )
   
    indice = etiquetas.index(seleccion_etiqueta)
    clave_metrica = claves[indice]

    
    calcular_jugador = st.sidebar.button("Comenzar estudio", key="btn_jugador")
    metrica_jugador_seleccionada = [clave_metrica] if clave_metrica else []

    return (
        ruta_encuentro,
        claves_encuentro,
        calcular_encuentro,
        player_id,
        metrica_jugador_seleccionada,
        grupo_seleccionado,
        calcular_jugador,
    )