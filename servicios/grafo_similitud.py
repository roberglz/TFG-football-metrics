import pandas as pd
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

    return df_vecinos