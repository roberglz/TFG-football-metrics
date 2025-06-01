import os
import json
import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter





def calcular_velocidades(data, frame_duration=0.2, window_length=7, polyorder=1, maxspeed=12):
    """
    Calcula la velocidad de los jugadores basándose en la diferencia de posición entre frames.

    Args:
        data: Lista de diccionarios con datos de seguimiento.
        frame_duration: Duración de un frame en segundos.
        window_length: Longitud de la ventana para el filtro Savitzky-Golay.
        polyorder: Orden del polinomio para el filtro.
        maxspeed: Velocidad máxima permitida para evitar valores atípicos.

    Returns:
        Una nueva lista de diccionarios con la velocidad calculada y filtrada.
    """
    player_data = {}

    # Recopila posiciones por jugador
    for frame in data:
        for player_type in ['homePlayers', 'awayPlayers']:
            for player in frame[player_type]:
                player_id = player['playerId']
                if player_id not in player_data:
                    player_data[player_id] = {
                        'x': [], 'y': [], 'speed': []
                    }
                player_data[player_id]['x'].append(player['xyz'][0])
                player_data[player_id]['y'].append(player['xyz'][1])

    # Calcula velocidades
    for player_id in player_data:
        x_vals = np.array(player_data[player_id]['x'])
        y_vals = np.array(player_data[player_id]['y'])

        vx = np.diff(x_vals) / frame_duration
        vy = np.diff(y_vals) / frame_duration
        speed = np.sqrt(vx**2 + vy**2)

        # Llena primer valor con 0 para mantener tamaño de lista
        speed = np.insert(speed, 0, 0)

        # Filtra valores atípicos
        speed[speed > maxspeed] = maxspeed

        # Suaviza con Savitzky-Golay si hay suficientes datos
        if len(speed) >= window_length:
            speed = savgol_filter(speed, window_length, polyorder, mode='nearest')

        player_data[player_id]['speed'] = speed

    # Asigna los datos de velocidad calculada de vuelta al dataset
    new_data = []
    frame_counts = {player_id: 0 for player_id in player_data}

    for frame in data:
        new_frame = {key: value if key not in ['homePlayers', 'awayPlayers'] else [] for key, value in frame.items()}

        for player_type in ['homePlayers', 'awayPlayers']:
            for player in frame[player_type]:
                player_id = player['playerId']
                index = frame_counts[player_id]
                new_speed = player_data[player_id]['speed'][index] if index < len(player_data[player_id]['speed']) else 0

                new_player = player.copy()
                new_player['speed'] = new_speed
                new_frame[player_type].append(new_player)

                frame_counts[player_id] += 1

        new_data.append(new_frame)

    return new_data


def dist_aceleraciones(data, frame_duration):
    """
    Calcula las métricas de aceleración, incluyendo distancias en rangos
    de aceleración/desaceleración, la aceleración máxima y el número de esfuerzos.

    Args:
        data: Lista de diccionarios con datos de seguimiento.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con las métricas de aceleración para cada jugador.
    """
    
    data = calcular_velocidades(data)
    
    
    player_metrics = {}

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
            current_position = tuple(player['xyz'])

            speed = player['speed']




            # Inicializar métricas para el jugador si no existe
            if player_id not in player_metrics:
                player_metrics[player_id] = {
                    'acc_dist_0_1': 0,
                    'acc_dist_1_2': 0,
                    'acc_dist_2_3': 0,
                    'acc_dist_3_4': 0,
                    'acc_dist_5_6': 0,
                    'max_acceleration': 0,
                    'num_efforts_0_1': 0,  # Nuevo: Número de esfuerzos
                    'num_efforts_1_2': 0,
                    'num_efforts_2_3': 0,
                    'num_efforts_3_4': 0,
                    'num_efforts_5_6': 0,
                    'num_efforts_max_acc': 0,
                    'previous_position': None,
                    'previous_speed': 0,
                    'in_effort': False  # Nuevo: Flag para controlar si está en un esfuerzo
                }

            # Calcular la distancia desde la posición anterior
            distance = 0
            if player_metrics[player_id]['previous_position'] is not None:
                previous_pos = player_metrics[player_id]['previous_position']
                distance = math.dist(previous_pos, current_position)

            # Calcular la aceleración
            acceleration = (speed - player_metrics[player_id]['previous_speed']) / frame_duration

            # Actualizar las métricas de distancia y número de esfuerzos
            abs_acceleration = abs(acceleration)

            # Definir rangos de aceleración y actualizar métricas
            ranges = [(0, 1, '0_1'), (1, 2, '1_2'), (2, 3, '2_3'), (3, 4, '3_4'), (5, 6, '5_6')]
            for start, end, suffix in ranges:
                if start <= abs_acceleration < end:
                    player_metrics[player_id][f'acc_dist_{suffix}'] += distance
                    if not player_metrics[player_id]['in_effort']:  # Si no está en un esfuerzo, inicia uno
                        player_metrics[player_id][f'num_efforts_{suffix}'] += 1
                        player_metrics[player_id]['in_effort'] = True
                    break
            else:  # Si no está en ningún rango, termina el esfuerzo actual
                player_metrics[player_id]['in_effort'] = False


            # Actualizar la aceleración máxima y el número de esfuerzos
            if abs_acceleration > player_metrics[player_id]['max_acceleration']:
                player_metrics[player_id]['max_acceleration'] = abs_acceleration


            if abs_acceleration > 6:
                player_metrics[player_id]['num_efforts_max_acc'] += 1


            # Actualiza la posición y velocidad previas
            player_metrics[player_id]['previous_position'] = current_position
            player_metrics[player_id]['previous_speed'] = speed

    # Crea una lista de diccionarios para el DataFrame
    table_data = []
    for player_id, metrics in player_metrics.items():
      table_data.append({
        'playerId': player_id,
        'acc_dist_0_1': round(metrics['acc_dist_0_1'], 2),
        'acc_dist_1_2': round(metrics['acc_dist_1_2'], 2),
        'acc_dist_2_3': round(metrics['acc_dist_2_3'], 2),
        'acc_dist_3_4': round(metrics['acc_dist_3_4'], 2),
        'acc_dist_5_6': round(metrics['acc_dist_5_6'], 2),
        'max_acceleration': round(metrics['max_acceleration'], 2),
        'num_efforts_0_1': metrics['num_efforts_0_1'],
        'num_efforts_1_2': metrics['num_efforts_1_2'],
        'num_efforts_2_3': metrics['num_efforts_2_3'],
        'num_efforts_3_4': metrics['num_efforts_3_4'],
        'num_efforts_5_6': metrics['num_efforts_5_6'],
        'num_efforts_max_acc': metrics['num_efforts_max_acc']
    })

    # Crea y devuelve el DataFrame
    df = pd.DataFrame(table_data)
    return df