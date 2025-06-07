import os
import json
import math
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import math
from scipy.signal import savgol_filter







def ritmo_juego(data, frame_duration):
    player_data = {}

    for frame_index, frame in enumerate(data):
        previous_frame = data[frame_index - 1] if frame_index > 0 else {}
        current_period = frame.get('period')
        previous_period = previous_frame.get('period')

        if current_period != previous_period:
            continue

        for player in frame['homePlayers'] + frame['awayPlayers']:
            player_id = player['playerId']
            x, y = player['xyz'][0], player['xyz'][1]
            speed = player['speed']

            if player_id not in player_data:
                player_data[player_id] = {
                    'x_coords': [], 'y_coords': [], 'speeds': [],
                    'walkingDistance': 0, 'joggingDistance': 0,
                    'lowSpeedRunningDistance': 0, 'highSpeedRunningDistance': 0,
                    'sprintDistance': 0, 'veryHighSpeedDistance': 0,
                }

            player_data[player_id]['x_coords'].append(x)
            player_data[player_id]['y_coords'].append(y)
            player_data[player_id]['speeds'].append(speed)

    table_data = []

    for player_id, info in player_data.items():
        x_coords = np.array(info['x_coords'])
        y_coords = np.array(info['y_coords'])
        speeds = np.array(info['speeds'])

        if len(x_coords) >= 3:
            x_smooth = savgol_filter(x_coords, 3, 1)
            y_smooth = savgol_filter(y_coords, 3, 1)
            speeds_smooth = savgol_filter(speeds, 3, 1)
        else:
            x_smooth, y_smooth, speeds_smooth = x_coords, y_coords, speeds

        total_distance = 0
        walking = jogging = low_run = high_run = sprint = very_high = 0

        for i in range(1, len(x_smooth)):
            d = math.dist([x_smooth[i-1], y_smooth[i-1]], [x_smooth[i], y_smooth[i]])
            total_distance += d

            v_kmh = speeds_smooth[i] * 3.6
            if v_kmh < 7:
                walking += d
            elif v_kmh <= 15:
                jogging += d
            elif v_kmh <= 20:
                low_run += d
            elif v_kmh <= 25:
                high_run += d
            elif v_kmh <= 30:
                sprint += d
            else:
                very_high += d

        playing_time = len(info['x_coords']) * frame_duration / 60  # en minutos

        table_data.append({
            'playerId': player_id,
            'playingTime': playing_time,
            'walkingRhythm': walking / playing_time if playing_time else 0,
            'joggingRhythm': jogging / playing_time if playing_time else 0,
            'lowSpeedRunningRhythm': low_run / playing_time if playing_time else 0,
            'highSpeedRunningRhythm': high_run / playing_time if playing_time else 0,
            'sprintRhythm': sprint / playing_time if playing_time else 0,
            'veryHighSpeedRhythm': very_high / playing_time if playing_time else 0
        })

    return pd.DataFrame(table_data)