import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter


def ritmo_juego_individual(data, player_id, frame_duration):
    """
    Calcula las métricas de ritmo de juego únicamente para el jugador especificado.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con una sola fila y columnas:
          ['playerId', 'playingTime', 'totalDistanceRhythm', 'walkingRhythm',
           'joggingRhythm', 'lowSpeedRunningRhythm', 'highSpeedRunningRhythm',
           'sprintRhythm', 'veryHighSpeedRhythm'].
    """
    # 1) Recopilar solo x, y y speed para player_id, respetando saltos de periodo
    x_coords = []
    y_coords = []
    speeds = []
    periods = []

    for idx, frame in enumerate(data):
        if idx == 0:
            # En el primer frame, solo capturamos al jugador si aparece
            for p in frame['homePlayers'] + frame['awayPlayers']:
                if p['playerId'] == player_id:
                    x_coords.append(p['xyz'][0])
                    y_coords.append(p['xyz'][1])
                    speeds.append(p.get('speed', 0.0))
                    periods.append(frame.get('period'))
                    break
            continue

        prev_frame = data[idx - 1]
        current_period = frame.get('period')
        previous_period = prev_frame.get('period')

        # Salta si hay cambio de periodo
        if current_period != previous_period:
            continue

        # Busca al jugador en el frame actual
        found = False
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                x_coords.append(p['xyz'][0])
                y_coords.append(p['xyz'][1])
                speeds.append(p.get('speed', 0.0))
                periods.append(current_period)
                found = True
                break

        # Si no aparece en este frame, lo ignoramos
        if not found:
            continue

    # 2) Si no hay datos, devuelve ceros
    if len(x_coords) < 1:
        row = {
            'playerId': player_id,
            'playingTime': 0.0,
            'totalDistanceRhythm': 0.0,
            'walkingRhythm': 0.0,
            'joggingRhythm': 0.0,
            'lowSpeedRunningRhythm': 0.0,
            'highSpeedRunningRhythm': 0.0,
            'sprintRhythm': 0.0,
            'veryHighSpeedRhythm': 0.0
        }
        return pd.DataFrame([row])

    # 3) Suaviza si hay >= 3 muestras
    x_arr = np.array(x_coords)
    y_arr = np.array(y_coords)
    speeds_arr = np.array(speeds)

    if len(x_arr) >= 3:
        x_smooth = savgol_filter(x_arr, 3, 1)
        y_smooth = savgol_filter(y_arr, 3, 1)
        speeds_smooth = savgol_filter(speeds_arr, 3, 1)
    else:
        x_smooth = x_arr
        y_smooth = y_arr
        speeds_smooth = speeds_arr

    # 4) Calcula distancias totales y por categoría de velocidad
    total_distance = 0.0
    walking_distance = 0.0
    jogging_distance = 0.0
    low_speed_running_distance = 0.0
    high_speed_running_distance = 0.0
    sprint_distance = 0.0
    very_high_speed_distance = 0.0

    for i in range(1, len(x_smooth)):
        # Distancia entre posiciones
        distance = math.dist(
            [x_smooth[i - 1], y_smooth[i - 1]],
            [x_smooth[i], y_smooth[i]]
        )
        total_distance += distance

        # Velocidad suavizada en m/s → km/h
        velocity_kmh = speeds_smooth[i] * 3.6

        # Clasifica
        if velocity_kmh < 7:
            walking_distance += distance
        elif velocity_kmh <= 15:
            jogging_distance += distance
        elif velocity_kmh <= 20:
            low_speed_running_distance += distance
        elif velocity_kmh <= 25:
            high_speed_running_distance += distance
        elif velocity_kmh <= 30:
            sprint_distance += distance
        else:
            very_high_speed_distance += distance

    # 5) Calcula tiempo de juego en minutos 
    playing_time_seconds = len(x_coords) * frame_duration
    playing_time_minutes = playing_time_seconds / 60 if playing_time_seconds > 0 else 0.0

    # 6) Evitar división por cero al calcular ritmos
    if playing_time_minutes == 0:
        rhythms = {
            'totalDistanceRhythm': 0.0,
            'walkingRhythm': 0.0,
            'joggingRhythm': 0.0,
            'lowSpeedRunningRhythm': 0.0,
            'highSpeedRunningRhythm': 0.0,
            'sprintRhythm': 0.0,
            'veryHighSpeedRhythm': 0.0
        }
    else:
        rhythms = {
            'totalDistanceRhythm': total_distance / playing_time_minutes,
            'walkingRhythm': walking_distance / playing_time_minutes,
            'joggingRhythm': jogging_distance / playing_time_minutes,
            'lowSpeedRunningRhythm': low_speed_running_distance / playing_time_minutes,
            'highSpeedRunningRhythm': high_speed_running_distance / playing_time_minutes,
            'sprintRhythm': sprint_distance / playing_time_minutes,
            'veryHighSpeedRhythm': very_high_speed_distance / playing_time_minutes
        }

    # 7) Montar DataFrame de salida
    row = {
        'playerId': player_id,
        'playingTime': round(playing_time_minutes, 2),
        **{k: round(v, 2) for k, v in rhythms.items()}
    }
    return pd.DataFrame([row])
