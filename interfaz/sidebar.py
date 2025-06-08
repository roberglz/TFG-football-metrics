import streamlit as st
import pandas as pd
from servicios.visualizar_partidos import listar_partidos,hay_datos_suficientes
from servicios.jugadores import cargar_diccionario_jugadores
from utils.agrupacion_metricas import GRUPOS_METRICAS
from utils.metricas_seleccionadas import METRICAS_DISPLAY

def construir_sidebar():
    st.sidebar.header("Opciones disponibles:")

    # -- 1. Cálculo por encuentro --
    st.sidebar.subheader("1. Cálculo de métricas físicas por encuentro")

    metricas_grupo = {
        "Variables metabólicas": "potencia",
        "Ritmo de juego": "ritmo",
        "Cambios de dirección": "cambios",
        "Aceleraciones": "aceleraciones",
        "Distancias umbral estándar": "umbral_est",
        "Distancias umbral relativo": "umbral_rel"
    }

    if not hay_datos_suficientes():
        st.sidebar.warning("No hay datos disponibles.")
        seleccion_partido = st.sidebar.selectbox("Seleccione un partido:", ["(sin partidos disponibles)"], index=0, disabled=True)
        ruta_encuentro = None
        seleccion_encuentro = st.sidebar.multiselect(
            "Seleccione métricas por encuentro:",
            list(metricas_grupo.keys()),
            key="encuentro"
        )
        claves_encuentro = []
        calcular_encuentro = False
    else:
        lista_partidos = listar_partidos()
        opciones = {nombre_legible: ruta for nombre_legible, ruta in lista_partidos}
        seleccion_partido = st.sidebar.selectbox("Seleccione un partido:", list(opciones.keys()))
        ruta_encuentro = opciones.get(seleccion_partido)

        seleccion_encuentro = st.sidebar.multiselect(
            "Seleccione métricas por encuentro:",
            list(metricas_grupo.keys()),
            key="encuentro"
        )
        claves_encuentro = [metricas_grupo[m] for m in seleccion_encuentro]
        calcular_encuentro = st.sidebar.button("Calcular", key="btn_encuentro")

    st.sidebar.write("")  # Espacio




    # -- 2. Evolución de métricas de un jugador --
    st.sidebar.subheader("2. Evolución de métricas de un jugador")
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

    calcular_jugador = st.sidebar.button("Mostrar evolución", key="btn_jugador")





    st.sidebar.write("")  # Espacio

    # -- 3. Generación de grafo de similitud --
    st.sidebar.subheader("3. Generación de grafo de similitud")

    df_csv = pd.read_csv("config/metricas_con_nombres.csv")
    opciones_jugadores = df_csv["Jugador"].tolist()
    seleccion_jugador_csv = st.sidebar.selectbox(
        "Seleccione un jugador para el grafo:",
        opciones_jugadores,
        key="select_grafo"
    )

    N = st.sidebar.number_input(
        "Número de jugadores más similares (N):",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
        key="n_similares"
    )

    columnas_metricas = [col for col in df_csv.columns if col != "Jugador"]
    etiquetas_metricas = [
        METRICAS_DISPLAY.get(col, col) for col in columnas_metricas
    ]
    seleccion_metricas_csv = st.sidebar.multiselect(
        "Seleccione métricas para similitud:",
        etiquetas_metricas,
        key="multiselect_metricas_grafo"
    )

    inv_map = {v: k for k, v in METRICAS_DISPLAY.items()}
    claves_metricas_csv = [
        inv_map.get(etiqueta, etiqueta) for etiqueta in seleccion_metricas_csv
    ]

    generar_grafo = st.sidebar.button("Generar grafo", key="btn_grafo")

    st.sidebar.write("")  # Espacio



    # -- 4. Clustering de perfiles físicos --
    
    st.sidebar.subheader("4. Clustering de perfiles físicos")
    ejecutar_clustering = st.sidebar.button("Ejecutar clustering", key="btn_clustering")




    st.sidebar.write("")  # Espacio


    # -- 5. Visualización de anomalías físicas --
    st.sidebar.subheader("5. Visualización de anomalías físicas")

    # Cargamos CSV anotado con nombres
    df_anomalias = pd.read_csv("config/anomalias.csv")
    jugadores_anomalos = df_anomalias["Jugador"].unique().tolist()

    jugador_seleccionado_anomalia = st.sidebar.selectbox(
            "Seleccione un jugador con anomalías:",
            jugadores_anomalos,
            key="select_anomalias"
        )

    visualizar_anomalia = st.sidebar.button("Visualizar anomalías", key="btn_anomalias")

    return (
        ruta_encuentro,
        claves_encuentro,
        calcular_encuentro,
        player_id,
        [clave_metrica] if clave_metrica else [],
        grupo_seleccionado,
        calcular_jugador,
        seleccion_jugador_csv,
        N,
        claves_metricas_csv,
        generar_grafo,
        ejecutar_clustering,
        visualizar_anomalia,
        jugador_seleccionado_anomalia
    )