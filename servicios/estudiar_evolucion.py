import os
import json
from metricas.individuales.distancia_aceleraciones_individual import dist_aceleraciones_individual 
from metricas.individuales.distancia_umbrales_estandar_individual import dist_umbrales_estandar_individual
from metricas.individuales.distancia_umbrales_relativos_individual import dist_umbrales_relativos_individual
from metricas.individuales.potencia_metabolica_individual import pot_metabolica_individual
from metricas.individuales.ritmo_de_juego_individual import ritmo_juego_individual

FRAME_STEP = 5      # frecuencia reducida para submuestreo (25 Hz -> 5 Hz)
FRAME_DURATION = 0.2


def cargar_partido(ruta):
    """
    Carga un archivo JSONL de tracking con submuestreo a 5 Hz
    """
    data = []
    with open(ruta, 'r') as f:
        for i, linea in enumerate(f):
            if (i + 1) % FRAME_STEP == 0:
                data.append(json.loads(linea))
    return data


# servicios/estudiar_evolucion.py

import os
import json
from servicios.procesa_partidos import cargar_partido

def recorrer_partidos(func_metrica, player_id, metrica_clave):
    
    resultados = []
    base_datos = "datos"  # Carpeta raíz donde están los subdirectorios de partidos

    for carpeta in sorted(os.listdir(base_datos)):
        if not carpeta.endswith(" All Data Files"):
            continue

        match_id = carpeta.replace(" All Data Files", "")
        ruta_carpeta = os.path.join(base_datos, carpeta)

        # Ruta a metadata
        nombre_meta = f"{match_id}_SecondSpectrum_Metadata.json"
        ruta_metadata = os.path.join(ruta_carpeta, nombre_meta)
        if not os.path.exists(ruta_metadata):
            continue

        with open(ruta_metadata, "r", encoding="utf-8") as f:
            meta = json.load(f)

        # Obtener nombre completo del partido, p.ej. "EVE - CHE : 2022-8-6"
        descripcion_completa = meta.get("description", match_id)
        match_sin_fecha = descripcion_completa.split(" : ")[0]

        # Comprueba participación
        ssi_ids = [p.get("ssiId") for p in meta.get("homePlayers", []) + meta.get("awayPlayers", [])]
        if player_id not in ssi_ids:
            continue

        # Ruta a datos del partido
        nombre_data = f"{match_id}_SecondSpectrum_Data.jsonl"
        ruta_data = os.path.join(ruta_carpeta, nombre_data)
        if not os.path.exists(ruta_data):
            continue

        data = cargar_partido(ruta_data)
        df_metrica = func_metrica(data, player_id, FRAME_DURATION)

        # Extrae valor de la métrica
        if metrica_clave in df_metrica.columns and not df_metrica.empty:
            valor = df_metrica.at[0, metrica_clave]
            # Solo añade si el valor es distinto de cero
            if valor != 0:
                resultados.append({"match": match_sin_fecha, "valor": valor})

    return resultados






def metricas_evolucion(player_id, metrica_seleccionada, grupo_metrica):

    metrica_clave = metrica_seleccionada[0] if metrica_seleccionada else None

    if grupo_metrica == "Aceleraciones":
        return recorrer_partidos(dist_aceleraciones_individual, player_id, metrica_clave)

    elif grupo_metrica == "Umbrales estándar":
        return recorrer_partidos(dist_umbrales_estandar_individual, player_id, metrica_clave)

    elif grupo_metrica == "Umbrales relativos":
        return recorrer_partidos(dist_umbrales_relativos_individual, player_id, metrica_clave)

    elif grupo_metrica == "Metabolicas":
        return recorrer_partidos(pot_metabolica_individual, player_id, metrica_clave)

    elif grupo_metrica == "Ritmo de juego":
        return recorrer_partidos(ritmo_juego_individual, player_id, metrica_clave)

    else:
        return None