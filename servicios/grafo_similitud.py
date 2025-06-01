import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances

def generar_grafo(jugador_base, metricas_seleccionadas, N):
    csv_path = "config/metricas_con_nombres.csv"

    # Cargar CSV
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo '{csv_path}'.")
        return

    # Verificar que el jugador_base existe
    if jugador_base not in df["Jugador"].values:
        st.error(f"El jugador '{jugador_base}' no se encuentra en la columna 'Jugador'.")
        return

    # Verificar que todas las métricas seleccionadas existen en el DataFrame
    faltantes = [m for m in metricas_seleccionadas if m not in df.columns]
    if faltantes:
        st.error(f"Las siguientes métricas no están en el CSV: {faltantes}")
        return

    # Copiar DataFrame y normalizar las columnas de métricas en rango [0, 1]
    df_norm = df.copy()
    scaler = MinMaxScaler()
    df_norm[metricas_seleccionadas] = scaler.fit_transform(df[metricas_seleccionadas])

    # Obtener valores normalizados del jugador_base
    valores_base = df_norm.loc[df_norm["Jugador"] == jugador_base, metricas_seleccionadas].values.reshape(1, -1)

    # Calcular distancias euclídeas contra todos los jugadores (incluyendo base)
    valores_otros = df_norm[metricas_seleccionadas].values
    distancias = pairwise_distances(valores_base, valores_otros, metric="euclidean")[0]
    df_norm["distancia"] = distancias

    # Filtrar los N más cercanos, excluyendo jugador_base
    df_vecinos = df_norm[df_norm["Jugador"] != jugador_base].nsmallest(N, "distancia")

    # Crear grafo
    G = nx.Graph()
    G.add_node(jugador_base)

    for _, row in df_vecinos.iterrows():
        jugador_similar = row["Jugador"]
        G.add_node(jugador_similar)
        G.add_edge(jugador_base, jugador_similar)

    # Dibujar grafo en un Figure de Matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color="skyblue",
        edge_color="gray",
        font_size=8
    )

    ax.set_title(
        f"{N} jugadores más similares a {jugador_base}\n"
        f"según las métricas seleccionadas",
        pad=20
    )
    ax.axis("off")
    plt.tight_layout()

    # Mostrar grafo en Streamlit
    st.pyplot(fig)
