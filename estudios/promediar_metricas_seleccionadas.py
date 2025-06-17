import os
import json
import pandas as pd
from metricas.metricas_seleccionadas import metricas_seleccionadas
from servicios.procesa_partidos import cargar_partido


# CONFIGURACION
DATOS_PATH = 'datos'
FRAME_DURATION = 1 / 5  # por submuestreo

# Cargar diccionario de jugadores
with open('config/dicc_jugadores.json', 'r', encoding='utf-8') as f:
    dicc_jugadores = json.load(f)

# Invertirlo: {nombre: playerId}
jugadores_ids = set(dicc_jugadores.keys())
print("Jugadores del diccionario:", list(jugadores_ids)[:5])

# Acumulador de resultados por jugador
resultados = {pid: [] for pid in jugadores_ids}

# Recorrer todas las carpetas de partidos
for carpeta in os.listdir(DATOS_PATH):
    ruta = os.path.join(DATOS_PATH, carpeta)
    if not os.path.isdir(ruta):
        continue

    archivos = os.listdir(ruta)
    metadata_file = next((f for f in archivos if f.endswith('_Metadata.json')), None)
    data_file = next((f for f in archivos if f.endswith('_Data.jsonl')), None)

    if not all([metadata_file, data_file]):
        continue

    path_metadata = os.path.join(ruta, metadata_file)
    path_data = os.path.join(ruta, data_file)

    print(f"\nProcesando partido: {carpeta}")

    # Leer metadata para mapear optaId -> ssiId
    with open(path_metadata, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    ssi_ids_en_partido = set(p['ssiId'] for p in metadata['homePlayers'] + metadata['awayPlayers'])

    # comprobamos jugadores 
    jugadores_validos = jugadores_ids.intersection(ssi_ids_en_partido)

    if jugadores_validos:
        try:
            data = cargar_partido(path_data)

            for player_id in jugadores_validos:
                df_metricas = metricas_seleccionadas(data, FRAME_DURATION, player_id)
                if not df_metricas.empty:
                    resultados[player_id].append(df_metricas)
        except Exception as e:
            print(f"Error en {carpeta}: {e}")



# Promedia por jugador
filas_finales = []
for player_id, lista_df in resultados.items():
    if lista_df:
        df_concat = pd.concat(lista_df)
        df_media = df_concat.drop(columns=['playerId'], errors='ignore').mean(numeric_only=True)
        df_media = df_media.to_frame().T
        df_media.insert(0, 'playerId', player_id)
        filas_finales.append(df_media)

# Dataframe final y conversión a csv
if not filas_finales:
    print("No se han encontrado métricas válidas para ningún jugador.")
else:
    df_resultado = pd.concat(filas_finales, ignore_index=True)
    df_resultado = df_resultado[['playerId'] + [col for col in df_resultado.columns if col != 'playerId']]
    print(df_resultado.head())
    df_resultado.to_csv('metricas_promediadas.csv', index=False)
