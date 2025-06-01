import json
from functools import lru_cache

from metricas.colectivas.potencia_metabolica import pot_metabolica
from metricas.colectivas.ritmo_de_juego import ritmo_juego
from metricas.colectivas.cambio_de_direcciones import cambios_direccion
from metricas.colectivas.distancia_aceleraciones import dist_aceleraciones
from metricas.colectivas.distancia_umbrales_estandar import dist_umbrales_estandar
from metricas.colectivas.distancia_umbrales_relativos import dist_umbrales_relativos

FRAME_STEP = 5      # frecuencia reducida para submuestreo (25 Hz -> 5 Hz)
FRAME_DURATION = 0.2

@lru_cache(maxsize=16)
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

def calcular_metricas(data, seleccion):
    """
    Ejecuta el cálculo de métricas físicas según la selección.
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