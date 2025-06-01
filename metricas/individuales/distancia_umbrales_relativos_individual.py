import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter


def calcular_esfuerzos_ponderados(df):
    equivalency_factors = {
        'esfuerzos_above_95_percent': 1.5,
        'esfuerzos_above_90_percent': 1.3,
        'esfuerzos_above_85_percent': 1.1,
        'esfuerzos_above_75_percent': 1.0
    }

    df['esfuerzos_ponderados'] = (
        df['esfuerzos_above_95_percent'] * equivalency_factors['esfuerzos_above_95_percent'] +
        df['esfuerzos_above_90_percent'] * equivalency_factors['esfuerzos_above_90_percent'] +
        df['esfuerzos_above_85_percent'] * equivalency_factors['esfuerzos_above_85_percent'] +
        df['esfuerzos_above_75_percent'] * equivalency_factors['esfuerzos_above_75_percent']
    )
    return df


def dist_umbrales_relativos_individual(data, player_id, frame_duration):
    """
    Calcula las distancias y esfuerzos relativos únicamente para el jugador especificado.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con las siguientes columnas (una sola fila):
            ['playerId', 'distance_above_60_percent', 'distance_above_75_percent',
             'distance_above_85_percent', 'distance_above_90_percent',
             'distance_above_95_percent', 'maxSpeed',
             'esfuerzos_high_speed_running', 'esfuerzos_sprint',
             'esfuerzos_velocidad_muy_alta', 'esfuerzos_above_75_percent',
             'esfuerzos_above_85_percent', 'esfuerzos_above_90_percent',
             'esfuerzos_above_95_percent', 'esfuerzos_ponderados'].
    """
    # 1) Recopilar x, y, speed y rastrear maxSpeed solo para este player_id,
    #    respetando saltos de período.
    x_coords = []
    y_coords = []
    speeds = []
    max_speed_raw = 0.0

    for idx, frame in enumerate(data):
        if idx == 0:
            # En el primer frame no comparamos periodo, solo capturamos si aparece
            for p in frame['homePlayers'] + frame['awayPlayers']:
                if p['playerId'] == player_id:
                    x_coords.append(p['xyz'][0])
                    y_coords.append(p['xyz'][1])
                    v = p.get('speed', 0.0)
                    speeds.append(v)
                    max_speed_raw = max(max_speed_raw, v)
                    break
            continue

        prev_frame = data[idx - 1]
        current_period = frame.get('period')
        previous_period = prev_frame.get('period')

        # Saltar si cambio de período
        if current_period != previous_period:
            continue

        # Buscar al jugador en el frame actual
        found = False
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                x_coords.append(p['xyz'][0])
                y_coords.append(p['xyz'][1])
                v = p.get('speed', 0.0)
                speeds.append(v)
                max_speed_raw = max(max_speed_raw, v)
                found = True
                break

        # Si no aparece, ignoramos este frame por completo
        if not found:
            continue

    # 2) Si no hay datos suficientes, devolvemos ceros
    if len(x_coords) < 1:
        row = {
            'playerId': player_id,
            'distance_above_60_percent': 0.0,
            'distance_above_75_percent': 0.0,
            'distance_above_85_percent': 0.0,
            'distance_above_90_percent': 0.0,
            'distance_above_95_percent': 0.0,
            'maxSpeed': 0.0,
            'esfuerzos_high_speed_running': 0,
            'esfuerzos_sprint': 0,
            'esfuerzos_velocidad_muy_alta': 0,
            'esfuerzos_above_75_percent': 0,
            'esfuerzos_above_85_percent': 0,
            'esfuerzos_above_90_percent': 0,
            'esfuerzos_above_95_percent': 0,
            'esfuerzos_ponderados': 0.0
        }
        return pd.DataFrame([row])

    # 3) Suavizar posiciones (x, y) si hay al menos 3 puntos
    x_arr = np.array(x_coords)
    y_arr = np.array(y_coords)
    speeds_arr = np.array(speeds)

    if len(x_arr) >= 3:
        x_smooth = savgol_filter(x_arr, 3, 1)
        y_smooth = savgol_filter(y_arr, 3, 1)
    else:
        x_smooth = x_arr
        y_smooth = y_arr

    # 4) Convertir max_speed_raw a km/h
    max_speed_kmh = max_speed_raw * 3.6

    # 5) Inicializar contadores de distancias y flags de esfuerzo
    dist_60 = dist_75 = dist_85 = dist_90 = dist_95 = 0.0
    esfuerzos_high_speed_running = 0
    esfuerzos_sprint = 0
    esfuerzos_velocidad_muy_alta = 0
    esfuerzos_above_75_percent = 0
    esfuerzos_above_85_percent = 0
    esfuerzos_above_90_percent = 0
    esfuerzos_above_95_percent = 0

    in_high_speed = False
    in_sprint = False
    in_velocidad_muy_alta = False
    in_75 = False
    in_85 = False
    in_90 = False
    in_95 = False

    # 6) Recorremos i = 1 … len(x_smooth)-1 para calcular distancias y esfuerzos
    for i in range(1, len(x_smooth)):
        # Distancia euclídea entre posiciones consecutivas
        distance = math.dist((x_smooth[i - 1], y_smooth[i - 1]), (x_smooth[i], y_smooth[i]))
        current_speed_kmh = speeds_arr[i] * 3.6

        # Distancias relativas
        if current_speed_kmh > max_speed_kmh * 0.60:
            dist_60 += distance
        if current_speed_kmh > max_speed_kmh * 0.75:
            dist_75 += distance
        if current_speed_kmh > max_speed_kmh * 0.85:
            dist_85 += distance
        if current_speed_kmh > max_speed_kmh * 0.90:
            dist_90 += distance
        if current_speed_kmh > max_speed_kmh * 0.95:
            dist_95 += distance

        # Conteo de esfuerzos
        # – High Speed Running: 20 ≤ v < 25 km/h
        if 20 <= current_speed_kmh < 25 and not in_high_speed:
            esfuerzos_high_speed_running += 1
            in_high_speed = True
        elif current_speed_kmh < 20 and in_high_speed:
            in_high_speed = False

        # – Sprint: v ≥ 25 km/h
        if current_speed_kmh >= 25 and not in_sprint:
            esfuerzos_sprint += 1
            in_sprint = True
        elif current_speed_kmh < 25 and in_sprint:
            in_sprint = False

        # – Velocidad muy alta: v ≥ 30 km/h
        if current_speed_kmh >= 30 and not in_velocidad_muy_alta:
            esfuerzos_velocidad_muy_alta += 1
            in_velocidad_muy_alta = True
        elif current_speed_kmh < 30 and in_velocidad_muy_alta:
            in_velocidad_muy_alta = False

        # – Esfuerzos por percentiles
        if current_speed_kmh > max_speed_kmh * 0.75 and not in_75:
            esfuerzos_above_75_percent += 1
            in_75 = True
        elif current_speed_kmh <= max_speed_kmh * 0.75 and in_75:
            in_75 = False

        if current_speed_kmh > max_speed_kmh * 0.85 and not in_85:
            esfuerzos_above_85_percent += 1
            in_85 = True
        elif current_speed_kmh <= max_speed_kmh * 0.85 and in_85:
            in_85 = False

        if current_speed_kmh > max_speed_kmh * 0.90 and not in_90:
            esfuerzos_above_90_percent += 1
            in_90 = True
        elif current_speed_kmh <= max_speed_kmh * 0.90 and in_90:
            in_90 = False

        if current_speed_kmh > max_speed_kmh * 0.95 and not in_95:
            esfuerzos_above_95_percent += 1
            in_95 = True
        elif current_speed_kmh <= max_speed_kmh * 0.95 and in_95:
            in_95 = False

    # 7) Montar diccionario de salida y DataFrame
    row = {
        'playerId': player_id,
        'distance_above_60_percent': round(dist_60, 2),
        'distance_above_75_percent': round(dist_75, 2),
        'distance_above_85_percent': round(dist_85, 2),
        'distance_above_90_percent': round(dist_90, 2),
        'distance_above_95_percent': round(dist_95, 2),
        'maxSpeed': round(max_speed_kmh, 2),
        'esfuerzos_high_speed_running': esfuerzos_high_speed_running,
        'esfuerzos_sprint': esfuerzos_sprint,
        'esfuerzos_velocidad_muy_alta': esfuerzos_velocidad_muy_alta,
        'esfuerzos_above_75_percent': esfuerzos_above_75_percent,
        'esfuerzos_above_85_percent': esfuerzos_above_85_percent,
        'esfuerzos_above_90_percent': esfuerzos_above_90_percent,
        'esfuerzos_above_95_percent': esfuerzos_above_95_percent,
        'esfuerzos_ponderados': 0.0  # Se calculará en siguiente paso
    }

    df_out = pd.DataFrame([row])
    df_out = calcular_esfuerzos_ponderados(df_out)
    return df_out