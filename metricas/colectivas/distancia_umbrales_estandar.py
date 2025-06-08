import math
import pandas as pd
import numpy as np
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



