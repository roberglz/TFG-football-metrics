import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter


def calcular_velocidades_individual(data, player_id, frame_duration=0.2,
                                    window_length=7, polyorder=1, maxspeed=12):
    """
    Calcula la velocidad únicamente para el jugador especificado (player_id),
    aplicando filtro Savitzky-Golay y limitando por maxspeed.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador cuyo vector de velocidades queremos calcular.
        frame_duration: Duración de un frame en segundos.
        window_length: Longitud de la ventana para el filtro Savitzky-Golay.
        polyorder: Orden del polinomio para el filtro.
        maxspeed: Velocidad máxima permitida para evitar valores atípicos.

    Returns:
        new_data: Lista de diccionarios igual al dataset original, pero con
                  la clave 'speed' solo actualizada para el player_id; el resto
                  de jugadores tendrá 'speed'=0.0.
    """
    # 1) Recoge todas las posiciones (x, y) de este player_id a lo largo de los frames
    x_vals = []
    y_vals = []
    frame_indices = []

    for idx, frame in enumerate(data):
        encontrado = False
        for player_type in ('homePlayers', 'awayPlayers'):
            for p in frame[player_type]:
                if p['playerId'] == player_id:
                    x_vals.append(p['xyz'][0])
                    y_vals.append(p['xyz'][1])
                    frame_indices.append(idx)
                    encontrado = True
                    break
            if encontrado:
                break

        if not encontrado:
            x_vals.append(None)
            y_vals.append(None)
            frame_indices.append(idx)

    # 2) Calcula velocidades solo en los instantes en que el jugador aparece consecutivamente
    speeds = [0.0] * len(x_vals)
    for i in range(1, len(x_vals)):
        if x_vals[i] is None or x_vals[i-1] is None:
            speeds[i] = 0.0
        else:
            dx = x_vals[i] - x_vals[i-1]
            dy = y_vals[i] - y_vals[i-1]
            v = math.hypot(dx, dy) / frame_duration
            # Limitar a maxspeed
            speeds[i] = min(v, maxspeed)

    # Aplicar Savitzky-Golay si hay suficientes datos válidos
    # Se considera que la serie "speeds" tiene longitud >= window_length
    if len(speeds) >= window_length:
        # Para filtrar, convertimos a array, aplicamos filtro y volvemos a lista
        arr = np.array(speeds)
        arr_filtered = savgol_filter(arr, window_length, polyorder, mode='nearest')
        speeds = arr_filtered.tolist()

    
    new_data = []
    for idx, frame in enumerate(data):
        new_frame = {k: v if k not in ('homePlayers', 'awayPlayers') else [] for k, v in frame.items()}

        # Posición en speeds para este frame
        pos_list = [pos for pos, fidx in enumerate(frame_indices) if fidx == idx]
        speed_val = 0.0
        if len(pos_list) > 0:
            speed_val = speeds[pos_list[0]]

        for player_type in ('homePlayers', 'awayPlayers'):
            for p in frame[player_type]:
                new_p = p.copy()
                if p['playerId'] == player_id:
                    new_p['speed'] = speed_val
                else:
                    new_p['speed'] = 0.0
                new_frame[player_type].append(new_p)

        new_data.append(new_frame)

    return new_data


def dist_aceleraciones_individual(data, player_id, frame_duration=0.2):
    """
    Calcula las métricas de aceleración únicamente para el jugador especificado.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con las métricas de aceleración para solo ese player_id.
        Las columnas son:
          ['playerId', 'acc_dist_0_1', 'acc_dist_1_2', 'acc_dist_2_3',
           'acc_dist_3_4', 'acc_dist_5_6', 'max_acceleration',
           'num_efforts_0_1', 'num_efforts_1_2', 'num_efforts_2_3',
           'num_efforts_3_4', 'num_efforts_5_6', 'num_efforts_max_acc']
    """
    # 1) Primero obtenemos data con velocidades solo de este jugador
    data_vel = calcular_velocidades_individual(data, player_id, frame_duration)

    # 2) Inicializamos métricas para este player_id
    metrics = {
        'acc_dist_0_1': 0.0,
        'acc_dist_1_2': 0.0,
        'acc_dist_2_3': 0.0,
        'acc_dist_3_4': 0.0,
        'acc_dist_5_6': 0.0,
        'max_acceleration': 0.0,
        'num_efforts_0_1': 0,
        'num_efforts_1_2': 0,
        'num_efforts_2_3': 0,
        'num_efforts_3_4': 0,
        'num_efforts_5_6': 0,
        'num_efforts_max_acc': 0,
        'previous_position': None,
        'previous_speed': 0.0,
        'in_effort': False
    }

    # 3) Bucle sobre frames (desde el segundo en adelante)
    for frame_index in range(1, len(data_vel)):
        frame = data_vel[frame_index]
        prev_frame = data_vel[frame_index - 1]

        # Si cambia de periodo, saltamos
        if frame.get('period') != prev_frame.get('period'):
            continue

        # Buscamos solo a este jugador en current_frame
        current_player = None
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                current_player = p
                break
        if current_player is None:
            continue

        # Buscamos al jugador en el frame anterior
        previous_player = None
        for p in prev_frame['homePlayers'] + prev_frame['awayPlayers']:
            if p['playerId'] == player_id:
                previous_player = p
                break
        if previous_player is None:
            continue

        # Extraemos posición (x, y) y velocidad
        current_position = tuple(current_player['xyz'])
        speed = current_player.get('speed', 0.0)

        distance = 0.0
        if metrics['previous_position'] is not None:
            prev_pos = metrics['previous_position']
            distance = math.dist(prev_pos, current_position)

        #
        acceleration = (speed - metrics['previous_speed']) / frame_duration
        abs_accel = abs(acceleration)

        
        ranges = [
            (0, 1, '0_1'),
            (1, 2, '1_2'),
            (2, 2.9999, '2_3'),
            (3, 3.9999, '3_4'),
            (5, 6, '5_6')
        ]
        categorized = False
        for start, end, suffix in ranges:
            if start <= abs_accel < end:
                metrics[f'acc_dist_{suffix}'] += distance
                if not metrics['in_effort']:
                    metrics[f'num_efforts_{suffix}'] += 1
                    metrics['in_effort'] = True
                categorized = True
                break

        if not categorized:
            
            metrics['in_effort'] = False

        
        if abs_accel > metrics['max_acceleration']:
            metrics['max_acceleration'] = abs_accel
        if abs_accel > 6.0:
            metrics['num_efforts_max_acc'] += 1

        
        metrics['previous_position'] = current_position
        metrics['previous_speed'] = speed

   
    row = {
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
    }
    df = pd.DataFrame([row])
    return df
