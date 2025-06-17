import streamlit as st
import pandas as pd
import networkx as nx
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import io

from servicios.jugadores import reemplazar_ids_por_nombres, cargar_diccionario_jugadores
from interfaz.visualizaciones_metricas import (
    mostrar_potencia, mostrar_ritmo, mostrar_cambios,
    mostrar_aceleraciones, mostrar_umbral_est, mostrar_umbral_rel
)
from utils.agrupacion_metricas import GRUPOS_METRICAS
from servicios.clustering import clustering_perfiles
from servicios.grafo_similitud import generar_grafo


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
    for grupo, mapping in GRUPOS_METRICAS.items():
        for legible, interno in mapping.items():
            if interno == internal_key:
                return legible
    return internal_key


def mostrar_evolucion(resultados, metrica_label_legible):
    if not resultados:
        st.warning("No hay datos para mostrar evolución.")
        return

    if isinstance(metrica_label_legible, list) and len(metrica_label_legible) > 0:
        metrica_label_legible = metrica_label_legible[0]

    nombre_legible = _obtener_label_legible(metrica_label_legible)
    df = pd.DataFrame(resultados).rename(columns={"valor": nombre_legible})

    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('match:N', title='Partido'),
        y=alt.Y(f'{nombre_legible}:Q', title=nombre_legible),
        tooltip=['match', nombre_legible]
    ).properties(
        width=700,
        height=400
    )

    st.subheader(f"Evolución de {nombre_legible} a lo largo de los encuentros")
    st.altair_chart(chart, use_container_width=True)


def _mostrar_figura_en_streamlit(fig, ancho_px):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)
    st.image(buf, width=ancho_px)
    plt.close(fig)


def mostrar_clustering():
    st.header("Clasificación automática de perfiles físicos (K-Means)")

    df_cluster, resumen = clustering_perfiles()

    st.subheader("Visualización 2D de perfiles")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df_cluster, x="PCA1", y="PCA2", hue="perfil_fisico", ax=ax, palette="Set2")
    ax.set_title("Perfiles físicos de jugadores (K-Means + PCA)")
    _mostrar_figura_en_streamlit(fig, ancho_px=1400)

    st.subheader("Métricas medias por perfil")
    st.dataframe(resumen.style.format(precision=2), use_container_width=True)

def mostrar_grafo(jugador_base, metricas_grafo, N):
    df_vecinos = generar_grafo(jugador_base, metricas_grafo, N)

    G = nx.Graph()
    G.add_node(jugador_base)
    for _, row in df_vecinos.iterrows():
        jugador_similar = row["Jugador"]
        G.add_node(jugador_similar)
        G.add_edge(jugador_base, jugador_similar)

    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color="skyblue",
        edge_color="gray",
        font_size=7
    )
    ax.set_title(
        f"{N} jugadores más similares a {jugador_base}\n"
        f"según las métricas seleccionadas",
        pad=10
    )
    ax.axis("off")
    plt.tight_layout()
    _mostrar_figura_en_streamlit(fig, ancho_px=1800)





def mostrar_anomalias(nombre_jugador):
    df = pd.read_csv("config/anomalias.csv")
    metricas = [col for col in df.columns if col not in ['Jugador', 'partido', 'anómalo']]
    df[metricas] = df[metricas].apply(pd.to_numeric, errors='coerce')
    media_global = df[metricas].mean()
    std_global = df[metricas].std()

    jugador_df = df[df["Jugador"] == nombre_jugador].copy().sort_values("partido")

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

        fig, ax = plt.subplots(figsize=(12, 4))  # ⬅️ Más ancho y menos alto
        ax.bar(metricas, z_scores, color='tab:blue', alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='--')
        ax.axhline(y=1.75, color='red', linestyle=':', label='Z = ±1.75')
        ax.axhline(y=-1.75, color='red', linestyle=':')
        ax.set_xticklabels(metricas, rotation=90, ha='center', fontsize=6)
        ax.set_title(f"Z-score de métricas - Partido anómalo: {partido}", fontsize=10)
        ax.set_ylabel("Z-score", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
        buf.seek(0)
        st.image(buf, width=2300)
        plt.close(fig)