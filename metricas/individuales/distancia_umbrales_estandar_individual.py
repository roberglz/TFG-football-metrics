import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter


def dist_umbrales_estandar_individual(data, player_id, frame_duration):
    """
    Calcula las distancias por umbrales de velocidad únicamente
    para el jugador especificado (player_id), usando umbrales estándar.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con las siguientes columnas:
          ['playerId', 'totalDistance', 'walkingDistance', 'joggingDistance',
           'lowSpeedRunningDistance', 'highSpeedRunningDistance', 'sprintDistance',
           'veryHighSpeedDistance', 'avgSpeed', 'maxSpeed'].
        Contendrá una única fila con las métricas de este jugador.
    """
    # 1) Primero, recopilar (x, y, speed) solo para player_id, respetando cambios de período
    x_coords = []
    y_coords = []
    speeds = []
    periods = []

    for idx, frame in enumerate(data):
        if idx == 0:
            # No hay frame anterior; lo añadimos a periods para la lógica de salto posterior
            for p in frame['homePlayers'] + frame['awayPlayers']:
                if p['playerId'] == player_id:
                    x_coords.append(p['xyz'][0])
                    y_coords.append(p['xyz'][1])
                    speeds.append(p.get('speed', 0.0))
                    periods.append(frame.get('period'))
                    break
            continue

        previous_frame = data[idx - 1]
        current_period = frame.get('period')
        previous_period = previous_frame.get('period')

        # Saltar si cambio de período
        if current_period != previous_period:
            continue

        # Buscar al jugador en el frame actual
        found = False
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                x_coords.append(p['xyz'][0])
                y_coords.append(p['xyz'][1])
                speeds.append(p.get('speed', 0.0))
                periods.append(current_period)
                found = True
                break

        # Si no aparece el jugador en este frame, lo ignoramos completamente (no sumamos nada)
        if not found:
            continue

    # 2) Si no tenemos datos suficientes, devolvemos ceros básicos
    if len(x_coords) < 1:
        row = {
            'playerId': player_id,
            'totalDistance': 0.0,
            'walkingDistance': 0.0,
            'joggingDistance': 0.0,
            'lowSpeedRunningDistance': 0.0,
            'highSpeedRunningDistance': 0.0,
            'sprintDistance': 0.0,
            'veryHighSpeedDistance': 0.0,
            'avgSpeed': 0.0,
            'maxSpeed': 0.0
        }
        return pd.DataFrame([row])

    # 3) Aplicar filtro Savitzky-Golay a posiciones (x, y) y velocidades si hay suficientes muestras
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

    # 4) Calcular distancias totales y por umbral
    total_distance = 0.0
    walking_distance = 0.0
    jogging_distance = 0.0
    low_speed_running_distance = 0.0
    high_speed_running_distance = 0.0
    sprint_distance = 0.0
    very_high_speed_distance = 0.0

    for i in range(1, len(x_smooth)):
        # Distancia Euclídea entre posiciones consecutivas
        distance = math.dist(
            [x_smooth[i-1], y_smooth[i-1]],
            [x_smooth[i], y_smooth[i]]
        )
        total_distance += distance

        # Velocidad suavizada en m/s → km/h
        velocity_kmh = speeds_smooth[i] * 3.6

        # Clasificar según umbrales estándar
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

    # 5) Calcular velocidad media y máxima en km/h
    avg_speed = float(np.mean(speeds_smooth) * 3.6) if len(speeds_smooth) > 0 else 0.0
    max_speed = float(np.max(speeds_smooth) * 3.6) if len(speeds_smooth) > 0 else 0.0

    # 6) Montar DataFrame de salida
    row = {
        'playerId': player_id,
        'totalDistance': round(total_distance, 2),
        'walkingDistance': round(walking_distance, 2),
        'joggingDistance': round(jogging_distance, 2),
        'lowSpeedRunningDistance': round(low_speed_running_distance, 2),
        'highSpeedRunningDistance': round(high_speed_running_distance, 2),
        'sprintDistance': round(sprint_distance, 2),
        'veryHighSpeedDistance': round(very_high_speed_distance, 2),
        'avgSpeed': round(avg_speed, 2),
        'maxSpeed': round(max_speed, 2)
    }
    return pd.DataFrame([row])