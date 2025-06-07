import streamlit as st
import pandas as pd
import altair as alt
from servicios.jugadores import reemplazar_ids_por_nombres, cargar_diccionario_jugadores
from interfaz.visualizaciones_metricas import (
    mostrar_potencia, mostrar_ritmo, mostrar_cambios,
    mostrar_aceleraciones, mostrar_umbral_est, mostrar_umbral_rel
)
from utils.agrupacion_metricas import GRUPOS_METRICAS
import matplotlib.pyplot as plt
import seaborn as sns
from servicios.clustering import clustering_perfiles

def mostrar_metricas(resultados):
    dicc = cargar_diccionario_jugadores()

    funciones_metrica = {
        'potencia': mostrar_potencia,
        'ritmo': mostrar_ritmo,
        'cambios': mostrar_cambios,
        'aceleraciones': mostrar_aceleraciones,
        'umbral_est': mostrar_umbral_est,
        'umbral_rel': mostrar_umbral_rel
    }

    for clave, funcion in funciones_metrica.items():
        if clave in resultados:
            df = reemplazar_ids_por_nombres(resultados[clave], dicc)
            funcion(df)


def _obtener_label_legible(internal_key):
    """
    Dado el identificador interno de la métrica (por ejemplo "HMLe" o "acc_dist_1_2"),
    busca en GRUPOS_METRICAS y devuelve la etiqueta legible correspondiente.
    """
    for grupo, mapping in GRUPOS_METRICAS.items():
        for legible, interno in mapping.items():
            if interno == internal_key:
                return legible
    # Si no se encuentra, devolvemos el mismo internal_key
    return internal_key


def mostrar_evolucion(resultados, metrica_label_legible):


    if not resultados:
        st.warning("No hay datos para mostrar evolución.")
        return

    # 1) Si viene como lista, extraer el primer elemento (clave interna)
    if isinstance(metrica_label_legible, list) and len(metrica_label_legible) > 0:
        metrica_label_legible = metrica_label_legible[0]

    # 2) Obtener el nombre legible real buscando en GRUPOS_METRICAS
    nombre_legible = _obtener_label_legible(metrica_label_legible)

    # 3) Construir DataFrame y renombrar columna 'valor' por el nombre legible
    df = pd.DataFrame(resultados)
    df = df.rename(columns={"valor": nombre_legible})

    # 4) Preparar gráfico de línea con puntos unidos
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('match:N', title='Partido'),
        y=alt.Y(f'{nombre_legible}:Q', title=nombre_legible),
        tooltip=['match', nombre_legible]
    ).properties(
        width=700,
        height=400
    )

    # 5) Mostrar en Streamlit
    st.subheader(f"Evolución de {nombre_legible} a lo largo de los encuentros")
    st.altair_chart(chart, use_container_width=True)

def mostrar_clustering():
    st.header("Clasificación automática de perfiles físicos (K-Means)")


    df_cluster, resumen = clustering_perfiles()

    st.subheader("Visualización 2D de perfiles")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_cluster, x="PCA1", y="PCA2", hue="perfil_fisico", ax=ax, palette="Set2")
    ax.set_title("Perfiles físicos de jugadores (K-Means + PCA)")
    st.pyplot(fig)

    st.subheader("Métricas medias por perfil")
    st.dataframe(resumen.style.format(precision=2))

    st.subheader("Datos con perfil asignado")
    st.dataframe(df_cluster)


def mostrar_anomalias(nombre_jugador):
    # Cargar el CSV con anotaciones
    df = pd.read_csv("config/anomalias.csv")

    # Lista de métricas numéricas
    metricas = [col for col in df.columns if col not in ['Jugador', 'partido', 'anómalo']]
    df[metricas] = df[metricas].apply(pd.to_numeric, errors='coerce')  # Forzar tipo numérico

    # Media y desviación estándar global
    media_global = df[metricas].mean()
    std_global = df[metricas].std()
    jugador_df = df[df["Jugador"] == nombre_jugador].copy()
    jugador_df = jugador_df.sort_values("partido")

    if jugador_df.empty:
        st.warning(f"No hay datos para el jugador {nombre_jugador}")
        return

    df_anomalo = jugador_df[jugador_df["anómalo"] == -1]
    if df_anomalo.empty:
        st.info(f"Jugador {nombre_jugador} no tiene partidos anómalos.")
        return

    for _, row in df_anomalo.iterrows():
        partido = row["partido"]
        st.subheader(f"🔍 Partido anómalo detectado: {partido}")

        z_scores = (row[metricas] - media_global) / std_global
    

        # Mostrar gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(metricas, z_scores, color='tab:blue', alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='--')
        ax.axhline(y=1.75, color='red', linestyle=':', label='Z = ±1.75')
        ax.axhline(y=-1.75, color='red', linestyle=':')
        ax.set_xticklabels(metricas, rotation=45, ha='right')
        ax.set_title(f"Z-score de métricas - Partido anómalo: {partido}")
        ax.set_ylabel("Z-score")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
