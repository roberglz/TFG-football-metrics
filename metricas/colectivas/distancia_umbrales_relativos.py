import math
import pandas as pd
from scipy.signal import savgol_filter
import numpy as np

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




def dist_umbrales_relativos(data, frame_duration):
    player_data = {}

    for frame_index, frame in enumerate(data):

        frame = data[frame_index]
        previous_frame = data[frame_index - 1]


        current_period = frame.get('period')
        previous_period = previous_frame.get('period')

        # Salta si hay un cambio de periodo
        if current_period != previous_period:
            continue





        for player in frame['homePlayers'] + frame['awayPlayers']:
            player_id = player['playerId']
            x, y = player['xyz'][0], player['xyz'][1]
            speed = player['speed']

            if player_id not in player_data:
                player_data[player_id] = {
                    'x_coords': [], 'y_coords': [],
                    'speeds': [],
                    'distance_above_60_percent': 0,
                    'distance_above_75_percent': 0,
                    'distance_above_85_percent': 0,
                    'distance_above_90_percent': 0,
                    'distance_above_95_percent': 0,
                    'maxSpeed': 0,
                    'esfuerzos_high_speed_running': 0,
                    'esfuerzos_sprint': 0,
                    'esfuerzos_velocidad_muy_alta': 0,
                    'esfuerzos_above_75_percent': 0,
                    'esfuerzos_above_85_percent': 0,
                    'esfuerzos_above_90_percent': 0,
                    'esfuerzos_above_95_percent': 0,
                    'esfuerzos_ponderados': 0,

                }

            player_data[player_id]['x_coords'].append(x)
            player_data[player_id]['y_coords'].append(y)
            player_data[player_id]['speeds'].append(speed)
            player_data[player_id]['maxSpeed'] = max(player_data[player_id]['maxSpeed'], speed)

    table_data = []

    for player_id, info in player_data.items():
        x_coords = np.array(info['x_coords'])
        y_coords = np.array(info['y_coords'])
        speeds = np.array(info['speeds'])

        if len(x_coords) >= 3:
            x_smooth = savgol_filter(x_coords, 3, 1)
            y_smooth = savgol_filter(y_coords, 3, 1)
        else:
            x_smooth, y_smooth = x_coords, y_coords

        info['maxSpeed'] = info['maxSpeed'] * 3.6
        in_high_speed_running = False
        in_sprint = False
        in_velocidad_muy_alta = False
        in_above_75_percent = False
        in_above_85_percent = False
        in_above_90_percent = False
        in_above_95_percent = False


        for i in range(1, len(x_smooth)):
            distance = math.dist((x_smooth[i - 1], y_smooth[i - 1]), (x_smooth[i], y_smooth[i]))
            current_speed = speeds[i] * 3.6

            if current_speed > info['maxSpeed'] * 0.6:
                info['distance_above_60_percent'] += distance
            if current_speed > info['maxSpeed'] * 0.75:
                info['distance_above_75_percent'] += distance
            if current_speed > info['maxSpeed'] * 0.85:
                info['distance_above_85_percent'] += distance
            if current_speed > info['maxSpeed'] * 0.9:
                info['distance_above_90_percent'] += distance
            if current_speed > info['maxSpeed'] * 0.95:
                info['distance_above_95_percent'] += distance

            # Calcula número de esfuerzos

            if 20 <= current_speed < 25 and not in_high_speed_running:
                info['esfuerzos_high_speed_running'] += 1
                in_high_speed_running = True
            elif current_speed < 20 and in_high_speed_running:
                in_high_speed_running = False

            if current_speed >= 25 and not in_sprint:
                info['esfuerzos_sprint'] += 1
                in_sprint = True
            elif current_speed < 25 and in_sprint:
                in_sprint = False

            if current_speed >= 30 and not in_velocidad_muy_alta:
                info['esfuerzos_velocidad_muy_alta'] += 1
                in_velocidad_muy_alta = True
            elif current_speed < 30 and in_velocidad_muy_alta:
                in_velocidad_muy_alta = False

            if current_speed > info['maxSpeed'] * 0.75 and not in_above_75_percent:
                info['esfuerzos_above_75_percent'] += 1
                in_above_75_percent = True
            elif current_speed <= info['maxSpeed'] * 0.75 and in_above_75_percent:
                in_above_75_percent = False

            if current_speed > info['maxSpeed'] * 0.85 and not in_above_85_percent:
                info['esfuerzos_above_85_percent'] += 1
                in_above_85_percent = True
            elif current_speed <= info['maxSpeed'] * 0.85 and in_above_85_percent:
                in_above_85_percent = False

            if current_speed > info['maxSpeed'] * 0.90 and not in_above_90_percent:
                info['esfuerzos_above_90_percent'] += 1
                in_above_90_percent = True
            elif current_speed <= info['maxSpeed'] * 0.90 and in_above_90_percent:
                in_above_90_percent = False

            if current_speed > info['maxSpeed'] * 0.95 and not in_above_95_percent:
                info['esfuerzos_above_95_percent'] += 1
                in_above_95_percent = True
            elif current_speed <= info['maxSpeed'] * 0.95 and in_above_95_percent:
                in_above_95_percent = False
        del info['x_coords']
        del info['y_coords']
        del info['speeds']
        table_data.append({'playerId': player_id, **info})


    

    df = pd.DataFrame(table_data)
    
    df = calcular_esfuerzos_ponderados(df)
    
    
    
    return df