import pandas as pd

from .ritmo_de_juego import ritmo_juego
from .distancia_aceleraciones import dist_aceleraciones
from .distancia_umbrales_estandar import dist_umbrales_estandar
from .distancia_umbrales_relativos import dist_umbrales_relativos


def metricas_seleccionadas(data, frame_duration, min_minutes=70):
    # Calcular métricas por jugador
    df_ritmo = ritmo_juego(data, frame_duration)
    df_acc = dist_aceleraciones(data, frame_duration)
    df_umbral_est = dist_umbrales_estandar(data, frame_duration)
    df_umbral_rel = dist_umbrales_relativos(data, frame_duration)

    # Filtrar por tiempo mínimo jugado
    df_ritmo = df_ritmo[df_ritmo['playingTime'] >= min_minutes].copy()
    df_ritmo.drop(columns=['playingTime'], inplace=True, errors='ignore')

    # Renombrar columnas para evitar conflictos
    df_ritmo = df_ritmo.rename(columns={
        'walkingRhythm': 'walkingRhythm_ritmo',
        'joggingRhythm': 'joggingRhythm_ritmo',
        'lowSpeedRunningRhythm': 'lowSpeedRunningRhythm_ritmo',
        'highSpeedRunningRhythm': 'highSpeedRunningRhythm_ritmo',
        'sprintRhythm': 'sprintRhythm_ritmo',
        'veryHighSpeedRhythm': 'veryHighSpeedRhythm_ritmo'
    })

    df_acc = df_acc.rename(columns={
        'acc_dist_3_4': 'acc_dist_3_4_aceleraciones',
        'acc_dist_5_6': 'acc_dist_5_6_aceleraciones',
        'max_acceleration': 'max_acceleration_aceleraciones',
        'num_efforts_0_1': 'num_efforts_0_1_aceleraciones',
        'num_efforts_1_2': 'num_efforts_1_2_aceleraciones',
        'num_efforts_2_3': 'num_efforts_2_3_aceleraciones',
        'num_efforts_3_4': 'num_efforts_3_4_aceleraciones',
        'num_efforts_5_6': 'num_efforts_5_6_aceleraciones',
        'num_efforts_max_acc': 'num_efforts_max_acc_aceleraciones'
    })

    df_umbral_est = df_umbral_est.rename(columns={
        'walkingDistance': 'walkingDistance_umbral_est',
        'joggingDistance': 'joggingDistance_umbral_est'
    })

    df_umbral_rel = df_umbral_rel.rename(columns={
        'distance_above_95_percent': 'distance_above_95_percent_umbral_rel',
        'maxSpeed': 'maxSpeed_umbral_rel',
        'esfuerzos_above_95_percent': 'esfuerzos_above_95_percent_umbral_rel'
    })

    # Combinar métricas por playerId
    df = df_ritmo.merge(df_acc, on='playerId', how='inner')
    df = df.merge(df_umbral_est, on='playerId', how='inner')
    df = df.merge(df_umbral_rel, on='playerId', how='inner')

    return df.reset_index(drop=True)