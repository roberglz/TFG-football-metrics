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

    # Collect coordinates and speeds
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
            speed = player['speed']

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
        walking_distance = jogging_distance = low_speed_running_distance = 0
        high_speed_running_distance = sprint_distance = very_high_speed_distance = 0

        for i in range(1, len(x_smooth)):
            distance = math.dist([x_smooth[i-1], y_smooth[i-1]], [x_smooth[i], y_smooth[i]])
            total_distance += distance

            velocity_smooth = speeds_smooth[i]
            velocity_kmh = velocity_smooth * 3.6

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

        avg_speed = np.mean(speeds_smooth) * 3.6 if len(speeds_smooth) > 0 else 0
        max_speed = np.max(speeds_smooth) * 3.6 if len(speeds_smooth) > 0 else 0

        # Calculate playing time in minutes
        playing_time_seconds = len(info['x_coords']) * frame_duration
        playing_time_minutes = playing_time_seconds / 60

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
            'maxSpeed': max_speed,
            'playingTime': playing_time_minutes,
            'totalDistanceRhythm': total_distance / playing_time_minutes,
            'walkingRhythm': walking_distance / playing_time_minutes,
            'joggingRhythm': jogging_distance / playing_time_minutes,
            'lowSpeedRunningRhythm': low_speed_running_distance / playing_time_minutes,
            'highSpeedRunningRhythm': high_speed_running_distance / playing_time_minutes,
            'sprintRhythm': sprint_distance / playing_time_minutes,
            'veryHighSpeedRhythm': very_high_speed_distance / playing_time_minutes
        })


    df = pd.DataFrame(table_data)
    columns_to_display = ['playerId'] + [col for col in df.columns if col.endswith('Rhythm')]
    df_display = df[columns_to_display]



    return df_display