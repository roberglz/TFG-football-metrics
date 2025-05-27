import os
import json
import re

EQUIPOS_PATH = os.path.join("config", "equipos.json")

with open(EQUIPOS_PATH, "r", encoding="utf-8") as f:
    EQUIPOS = json.load(f)

def traducir_nombre_archivo(nombre_archivo):
    """
    Convierte '1 TOT-SOU.jsonl' en '1. Tottenham - Southampton'
    """
    nombre_sin_ext = nombre_archivo.replace(".jsonl", "")
    m = re.match(r"(\d+)\s+([A-Z]{3})-([A-Z]{3})", nombre_sin_ext)
    if m:
        jornada, eq1, eq2 = m.groups()
        nombre_real = f"{jornada}. {EQUIPOS.get(eq1, eq1)} - {EQUIPOS.get(eq2, eq2)}"
        return nombre_real
    return nombre_archivo  # Fallback si no cumple el formato

def listar_partidos(directorio='datos'):
    """
    Devuelve lista de partidos disponibles con nombre visible y ruta:
    [('1. Tottenham - Southampton', 'datos/1 TOT-SOU.jsonl'), ...]
    """
    archivos = [f for f in os.listdir(directorio) if f.lower().endswith('.jsonl')]

    def clave_natural(nombre):
        m = re.match(r"^(\d+)", nombre)
        return int(m.group(1)) if m else float('inf')

    archivos_ordenados = sorted(archivos, key=clave_natural)
    rutas = [os.path.join(directorio, f) for f in archivos_ordenados]
    nombres_visibles = [traducir_nombre_archivo(f) for f in archivos_ordenados]

    return list(zip(nombres_visibles, rutas))