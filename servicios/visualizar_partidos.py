import os
import json

def listar_partidos():
    base_path = 'datos'  
    partidos = []
    
    # Cargamos el diccionario de abreviaturas a nombres reales
    with open('config/equipos.json', 'r', encoding='utf-8') as f:
        equipos = json.load(f)

    for carpeta in os.listdir(base_path):
        ruta_partido = os.path.join(base_path, carpeta)
        if not os.path.isdir(ruta_partido):
            continue

        # Buscar metadata json dentro de la carpeta del partido
        archivos = os.listdir(ruta_partido)
        metadata_file = next((f for f in archivos if f.endswith('_SecondSpectrum_Metadata.json')), None)
        data_file = next((f for f in archivos if f.endswith('_SecondSpectrum_Data.jsonl')), None)

        if metadata_file and data_file:
            metadata_path = os.path.join(ruta_partido, metadata_file)
            data_path = os.path.join(ruta_partido, data_file)

            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    descripcion = metadata.get("description", "")  # "BOU - AVL : 2022-8-6"
                    if " - " in descripcion:
                        abrevs = descripcion.split(":")[0].strip().split(" - ")
                        if len(abrevs) == 2:
                            eq1 = equipos.get(abrevs[0], abrevs[0])
                            eq2 = equipos.get(abrevs[1], abrevs[1])
                            nombre_legible = f"{eq1} - {eq2}"
                            partidos.append((nombre_legible, data_path))
            except Exception as e:
                print(f"Error leyendo metadata {metadata_path}: {e}")
                continue

    return partidos

import os

import os

def hay_datos_suficientes(min_partidos=3):
    """
    Verifica si existen al menos `min_partidos` carpetas válidas con los archivos requeridos.

    Args:
        min_partidos (int): Número mínimo de partidos necesarios.

    Returns:
        bool: True si hay al menos `min_partidos` partidos válidos, False en caso contrario.
    """
    base_path = 'datos'

    if not os.path.exists(base_path) or not os.path.isdir(base_path):
        return False

    contador = 0

    for carpeta in os.listdir(base_path):
        ruta_partido = os.path.join(base_path, carpeta)
        if not os.path.isdir(ruta_partido):
            continue

        archivos = os.listdir(ruta_partido)
        metadata_file = next((f for f in archivos if f.endswith('_SecondSpectrum_Metadata.json')), None)
        data_file = next((f for f in archivos if f.endswith('_SecondSpectrum_Data.jsonl')), None)

        if metadata_file and data_file:
            contador += 1
            if contador >= min_partidos:
                return True

    return False
