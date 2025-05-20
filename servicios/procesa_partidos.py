import os, json
from functools import lru_cache
import re


# importamos todas las funciones de métricas
from metricas.potencia_metabolica       import pot_metabolica
from metricas.ritmo_de_juego            import ritmo_juego
from metricas.cambio_de_direcciones     import cambios_direccion
from metricas.distancia_aceleraciones   import dist_aceleraciones
from metricas.distancia_umbrales_estandar import dist_umbrales_estandar
from metricas.distancia_umbrales_relativos import dist_umbrales_relativos

FRAME_STEP = 5      # submuestreo para 5Hz
FRAME_DURATION = 0.2  # segundos

def listar_partidos(directorio='datos'):
    """
    Devuelve la lista de rutas a archivos .jsonl en 'datos/',
    ordenadas de forma natural según el número de partido al inicio
    del nombre de fichero.
    """
    archivos = [f for f in os.listdir(directorio) if f.lower().endswith('.jsonl')]

    # Orden natural: extraemos el número al principio de cada nombre
    def clave_natural(nombre_fichero):
        m = re.match(r'^(\d+)', nombre_fichero)
        return int(m.group(1)) if m else float('inf')

    archivos_sorted = sorted(archivos, key=clave_natural)
    return [os.path.join(directorio, f) for f in archivos_sorted]


@lru_cache(maxsize=16)
def cargar_partido(ruta):
    """Lee un JSONL y devuelve lista de frames submuestra 5Hz."""
    data = []
    with open(ruta, 'r') as f:
        for i, linea in enumerate(f):
            if (i + 1) % FRAME_STEP == 0:
                data.append(json.loads(linea))
    return data

def calcular_metricas(data, seleccion):
    """
    Dada una lista de frames y una lista de claves de métricas,
    devuelve un dict {clave: DataFrame} para cada métrica pedida.
    Claves válidas: 'potencia', 'ritmo', 'cambios', 'aceleraciones',
                   'umbral_est', 'umbral_rel'
    """
    resultados = {}
    if 'potencia' in seleccion:
        resultados['potencia'] = pot_metabolica(data, FRAME_DURATION)
    if 'ritmo' in seleccion:
        resultados['ritmo'] = ritmo_juego(data, FRAME_DURATION)
    if 'cambios' in seleccion:
        resultados['cambios'] = cambios_direccion(data, FRAME_DURATION)
    if 'aceleraciones' in seleccion:
        resultados['aceleraciones'] = dist_aceleraciones(data, FRAME_DURATION)
    if 'umbral_est' in seleccion:
        resultados['umbral_est'] = dist_umbrales_estandar(data, FRAME_DURATION)
    if 'umbral_rel' in seleccion:
        resultados['umbral_rel'] = dist_umbrales_relativos(data, FRAME_DURATION)
    return resultados
