import os
import json
import pandas as pd
from servicios.procesa_partidos import cargar_partido, calcular_metricas

# Ruta local al directorio que contiene las carpetas de los partidos
RUTA_DATOS = "C:/Users/rober/Desktop/UNIVERSIDAD/TFG/code/TFG-football-metrics\datos"
NUM_PARTIDOS = 40

# Métricas a calcular
metricas_a_calcular = [
    "potencia",
    "ritmo",
    "cambios",
    "aceleraciones",
    "umbral_est",
    "umbral_rel"
]

# DataFrame global para acumular métricas
df_global = pd.DataFrame()

# Recorremos carpetas
carpetas_partidos = sorted(os.listdir(RUTA_DATOS))[:NUM_PARTIDOS]

for carpeta in carpetas_partidos:
    ruta_partido = os.path.join(RUTA_DATOS, carpeta, f"{carpeta.split()[0]}_SecondSpectrum_Data.jsonl")
    if os.path.exists(ruta_partido):
        try:
            datos = cargar_partido(ruta_partido)
            resultados = calcular_metricas(datos, metricas_a_calcular)

            df_partido = pd.DataFrame()
            for nombre_metrica, df_metrica in resultados.items():
                df_metrica = df_metrica.copy()
                df_metrica.set_index("playerId", inplace=True)
                df_metrica.columns = [f"{col}_{nombre_metrica}" for col in df_metrica.columns]
                if df_partido.empty:
                    df_partido = df_metrica
                else:
                    df_partido = df_partido.join(df_metrica, how="outer")

            df_global = pd.concat([df_global, df_partido], axis=0)

        except Exception as e:
            print(f"Error procesando {carpeta}: {e}")

# Filtrar solo columnas numéricas y eliminar columnas con muchos NaN
df_global = df_global.select_dtypes(include=["number"]).dropna(axis=1, thresh=int(0.8 * len(df_global)))

# Calcula matriz de correlación
correlacion = df_global.corr()


output_path = "correlaciones_matriz.csv"
correlacion.to_csv(output_path)

print(f"Matriz de correlación guardada en {output_path}")
