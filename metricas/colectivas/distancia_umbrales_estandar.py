import os
import json
import math
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import math
from scipy.signal import savgol_filter



def dist_umbrales_estandar(data, frame_duration):
    player_data = {}

    # Recolecta coordenadas y velocidades
    for frame_index, frame in enumerate(data):

        frame = data[frame_index]
        previous_frame = data[frame_index - 1]
        current_period = frame.get('period')
        previous_period = previous_frame.get('period')

        if current_period != previous_period:
            continue


        for player in frame['homePlayers'] + frame['awayPlayers']:
            player_id = player['playerId']
            x, y = player['xyz'][0], player['xyz'][1]
            speed = player['speed']  # en m/s

            if player_id not in player_data:
                player_data[player_id] = {
                    'x_coords': [], 'y_coords': [],
                    'speeds': [], 'totalDistance': 0,
                    'walkingDistance': 0, 'joggingDistance': 0,
                    'lowSpeedRunningDistance': 0, 'highSpeedRunningDistance': 0,
                    'sprintDistance': 0, 'veryHighSpeedDistance': 0,
                    'maxSpeed': 0
                }

            player_data[player_id]['x_coords'].append(x)
            player_data[player_id]['y_coords'].append(y)
            player_data[player_id]['speeds'].append(speed)

    # Lista de resultados finales
    table_data = []

    for player_id, info in player_data.items():
        x_coords = np.array(info['x_coords'])
        y_coords = np.array(info['y_coords'])
        speeds = np.array(info['speeds'])

        # Aplica filtro Savitzky-Golay a las posiciones (x, y) y velocidad (speed)
        if len(x_coords) >= 3:
            x_smooth      = savgol_filter(x_coords, 3, 1)
            y_smooth      = savgol_filter(y_coords, 3, 1)
            speeds_smooth = savgol_filter(speeds, 3, 1)  # Suavizamos la velocidad
        else:
            x_smooth, y_smooth, speeds_smooth = x_coords, y_coords, speeds

        # Calcula la distancia total con posiciones suavizadas
        total_distance = 0
        walking_distance = jogging_distance = low_speed_running_distance = 0
        high_speed_running_distance = sprint_distance = very_high_speed_distance = 0

        for i in range(1, len(x_smooth)):
            # Calculamos la distancia entre posiciones consecutivas (en metros)
            distance = math.dist([x_smooth[i-1], y_smooth[i-1]], [x_smooth[i], y_smooth[i]])
            total_distance += distance

            # Suavizamos la velocidad calculada con el filtro Savitzky-Golay
            velocity_smooth = speeds_smooth[i]  # Ya está suavizada

            # Convertimos la velocidad suavizada a km/h
            velocity_kmh = velocity_smooth * 3.6

            # Clasificación de distancias según velocidad
            if  velocity_kmh < 7:
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

        # Calcula la velocidad media y máxima en km/h
        avg_speed = np.mean(speeds_smooth) * 3.6 if len(speeds_smooth) > 0 else 0
        max_speed = np.max(speeds_smooth) * 3.6 if len(speeds_smooth) > 0 else 0

        # Agrega resultados a la tabla
        table_data.append({
            'playerId': player_id,
            'totalDistance': total_distance,
            'walkingDistance': walking_distance,
            'joggingDistance': jogging_distance,
            'lowSpeedRunningDistance': low_speed_running_distance,
            'highSpeedRunningDistance': high_speed_running_distance,
            'sprintDistance': sprint_distance,
            'veryHighSpeedDistance': very_high_speed_distance,
            'avgSpeed': avg_speed,
            'maxSpeed': max_speed
        })


    df = pd.DataFrame(table_data)
    return df










def calcular_metricas_por_partes(data, frame_duration):
    """
    Calcula las métricas de aceleración por cada período del partido.
    """
    period_metrics = {}

    # Agrupar datos por período
    period_data = {}
    for frame in data:
        period = frame.get('period', 1)  # Asume período 1 si no está definido
        if period not in period_data:
            period_data[period] = []
        period_data[period].append(frame)

    # Calcular métricas por cada período
    for period, frames in period_data.items():
        print(f"Calculando métricas para el período {period}")
        period_metrics[period] = calcular_metricas(frames, frame_duration)

    return period_metrics




def calcular_metricas_por_intervalo(data, frame_duration, intervalo_min=5):
    """
    Calcula las métricas de aceleración en intervalos de tiempo definidos.
    """
    interval_metrics = {}

    # Verificar si hay una variable de tiempo; si no, generar timestamps
    for i, frame in enumerate(data):
        if 'time' not in frame:
            frame['time'] = i * frame_duration  # Genera timestamp basado en la frecuencia

    # Agrupar datos por período e intervalo de tiempo
    interval_data = {}
    for frame in data:

        timestamp = frame['time']  # Ahora siempre tendrá un valor correcto
        interval = (timestamp // (intervalo_min * 60)) + 1

        key = interval
        if key not in interval_data:
            interval_data[key] = []
        interval_data[key].append(frame)

    print(f"Se encontraron {len(interval_data)} intervalos.")

    # Calcular métricas por cada intervalo
    for  interval, frames in interval_data.items():
        print(f"Calculando métricas para el intervalo {interval}")
        interval_metrics[interval] = calcular_metricas(frames, frame_duration)

    return interval_metrics








"""

# AQUÍ SERÍA PARA COMPARAR ENTRE PARTES
metricas_por_partes = calcular_metricas_por_partes(data_5hz, 0.2)

# Mostrar resultados por partes
for period, df in metricas_por_partes.items():
    print(f"\nMétricas para la parte {period}:")
    display(df)







# AQUÍ SERÍA PARA OBTENER LOS FRAGMENTOS DE 5 MIN PARA 5HZ


metricas_por_intervalo = calcular_metricas_por_intervalo(data_5hz, 0.2, 5) # 5 MINUTOS

# Mostrar resultados por intervalo
for interval, df in metricas_por_intervalo.items():
    print(f"\n📊 Métricas para el intervalo {interval}:")
    display(df)  # Asegura que todas las métricas sean visibles """