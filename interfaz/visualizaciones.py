from servicios.jugadores import reemplazar_ids_por_nombres, cargar_diccionario_jugadores
from interfaz.visualizaciones_metricas import (
    mostrar_potencia, mostrar_ritmo, mostrar_cambios,
    mostrar_aceleraciones, mostrar_umbral_est, mostrar_umbral_rel
)

def mostrar_metricas(resultados):
    dicc = cargar_diccionario_jugadores()

    funciones_metrica = {
        'potencia': mostrar_potencia,
        'ritmo': mostrar_ritmo,
        'cambios': mostrar_cambios,
        'aceleraciones': mostrar_aceleraciones,
        'umbral_est': mostrar_umbral_est,
        'umbral_rel': mostrar_umbral_rel
    }

    for clave, funcion in funciones_metrica.items():
        if clave in resultados:
            df = reemplazar_ids_por_nombres(resultados[clave], dicc)
            funcion(df)