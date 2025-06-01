import pandas as pd

from .ritmo_de_juego import ritmo_juego
from .distancia_aceleraciones import dist_aceleraciones
from .distancia_umbrales_estandar import dist_umbrales_estandar
from .distancia_umbrales_relativos import dist_umbrales_relativos


def metricas_seleccionadas(data, frame_duration, player_id, min_minutes=65):
    # Calcular métricas completas con funciones ya implementadas
    df_ritmo = ritmo_juego(data, frame_duration)

    # Verificar si el jugador jugó al menos min_minutes
    fila_ritmo = df_ritmo[df_ritmo['playerId'] == player_id]
    if fila_ritmo.empty or fila_ritmo.iloc[0]['playingTime'] < min_minutes:
        return pd.DataFrame()  # No jugó lo suficiente

    df_acc = dist_aceleraciones(data, frame_duration)
    df_umbral_est = dist_umbrales_estandar(data, frame_duration)
    df_umbral_rel = dist_umbrales_relativos(data, frame_duration)

    # Renombrar columnas para hacerlas únicas y claras
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

    # Filtrar solo el jugador deseado
    df_ritmo = df_ritmo[df_ritmo['playerId'] == player_id]
    df_acc = df_acc[df_acc['playerId'] == player_id]
    df_umbral_est = df_umbral_est[df_umbral_est['playerId'] == player_id]
    df_umbral_rel = df_umbral_rel[df_umbral_rel['playerId'] == player_id]

    # Combinar todas las métricas por playerId (una única fila)
    df = df_ritmo[['playerId',
                   'walkingRhythm_ritmo', 'joggingRhythm_ritmo', 'lowSpeedRunningRhythm_ritmo',
                   'highSpeedRunningRhythm_ritmo', 'sprintRhythm_ritmo', 'veryHighSpeedRhythm_ritmo']]

    df = df.merge(df_acc[['playerId',
                          'acc_dist_3_4_aceleraciones', 'acc_dist_5_6_aceleraciones', 'max_acceleration_aceleraciones',
                          'num_efforts_0_1_aceleraciones', 'num_efforts_1_2_aceleraciones', 'num_efforts_2_3_aceleraciones',
                          'num_efforts_3_4_aceleraciones', 'num_efforts_5_6_aceleraciones', 'num_efforts_max_acc_aceleraciones']],
                  on='playerId', how='left')

    df = df.merge(df_umbral_est[['playerId', 'walkingDistance_umbral_est', 'joggingDistance_umbral_est']],
                  on='playerId', how='left')

    df = df.merge(df_umbral_rel[['playerId', 'distance_above_95_percent_umbral_rel',
                                 'maxSpeed_umbral_rel', 'esfuerzos_above_95_percent_umbral_rel']],
                  on='playerId', how='left')

    return df.reset_index(drop=True)


