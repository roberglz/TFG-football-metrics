import json
import os
import pandas as pd

def cargar_diccionario_jugadores(ruta='config/dicc_jugadores.json'):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def reemplazar_ids_por_nombres(df, diccionario, columna='playerId'):
    df = df.copy()
    if columna in df.columns:
        df[columna] = df[columna].map(diccionario).fillna(df[columna])
    return df
