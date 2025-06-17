import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from servicios.procesa_partidos import cargar_partido, calcular_metricas

# Configuración
RUTA_DATOS = ""
NUM_PARTIDOS = 1
UMBRAL = 0.75

# Métricas a calcular
metricas_a_calcular = [
    "potencia",
    "ritmo",
    "cambios",
    "aceleraciones",
    "umbral_est",
    "umbral_rel"
]

# Acumulador de métricas por jugador
df_global = pd.DataFrame()

# Procesamiento de partidos
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

# Limpieza y cálculo de correlaciones
df_global = df_global.select_dtypes(include=["number"]).dropna(axis=1, thresh=int(0.8 * len(df_global)))
df_corr = df_global.corr()
df_corr.to_csv("correlaciones_matriz.csv")

# Reducción por umbral de correlación
abs_corr = df_corr.abs()
columnas_eliminar = set()
columnas = abs_corr.columns

for i in range(len(columnas)):
    for j in range(i + 1, len(columnas)):
        col1, col2 = columnas[i], columnas[j]
        if abs_corr.loc[col1, col2] >= UMBRAL:
            suma1 = abs_corr[col1].sum()
            suma2 = abs_corr[col2].sum()
            eliminar = col1 if suma1 > suma2 else col2
            columnas_eliminar.add(eliminar)

columnas_finales = [col for col in df_corr.columns if col not in columnas_eliminar]
df_reducida = df_corr.loc[columnas_finales, columnas_finales]
df_reducida.to_csv("correlaciones_reducidas.csv")

# Heatmap de la matriz reducida
plt.figure(figsize=(14, 12))
sns.heatmap(df_reducida, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, square=True)
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.title(f"Matriz reducida de correlaciones (umbral = {UMBRAL})", fontsize=16)
plt.tight_layout()
plt.savefig("heatmap_correlaciones_reducido.png")
plt.show()
