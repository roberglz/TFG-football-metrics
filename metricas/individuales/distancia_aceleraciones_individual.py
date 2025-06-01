import math
import numpy as np
import pandas as pd

def dist_aceleraciones_individual(data, player_id, frame_duration):
    # 1. Recoge posiciones y velocidades
    x_vals, y_vals, speeds = [], [], []
    for frame in data:
        encontrado = False
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                x_vals.append(p['xyz'][0])
                y_vals.append(p['xyz'][1])
                speeds.append(p.get('speed', 0.0))
                encontrado = True
                break
        if not encontrado:
            
            x_vals.append(None)
            y_vals.append(None)
            speeds.append(0.0)

    # 2. Convierte a numpy para vectorizar cálculos
    x_arr = np.array([v if v is not None else np.nan for v in x_vals])
    y_arr = np.array([v if v is not None else np.nan for v in y_vals])
    speed_arr = np.array(speeds)

    # 3. Calcula aceleraciones (solo donde tengo datos consecutivos válidos)
    accel = np.zeros_like(speed_arr)
    valid_mask = ~np.isnan(x_arr)  # True en frames donde sí hay posición
    # Por simplicidad: acel[i] = (speed[i] - speed[i-1])/frame_duration
    accel[1:] = np.where(
        valid_mask[1:] & valid_mask[:-1],
        np.abs((speed_arr[1:] - speed_arr[:-1]) / frame_duration),
        0.0
    )

    # 4. Calcula distancias euclídeas entre frames válidos
    dist = np.zeros_like(speed_arr)
    dx = x_arr[1:] - x_arr[:-1]
    dy = y_arr[1:] - y_arr[:-1]
    dist[1:] = np.where(
        valid_mask[1:] & valid_mask[:-1],
        np.sqrt(dx**2 + dy**2),
        0.0
    )

    # 5. Definicion
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
        'num_efforts_max_acc': 0
    }
    in_effort = False

    # 6. Recorre vectores aceleración y distancia (vectorizados parcialmente)
    for i in range(1, len(speed_arr)):
        a = accel[i]
        d = dist[i]
        # Si el frame i o i-1 fue NaN, a=0 y d=0 por máscara
        if a > metrics['max_acceleration']:
            metrics['max_acceleration'] = a
        if a > 6.0:  # esfuerzo pico
            metrics['num_efforts_max_acc'] += 1

        # Acumula según rango
        if 0 <= a < 1:
            metrics['acc_dist_0_1'] += d
            if not in_effort:
                metrics['num_efforts_0_1'] += 1
                in_effort = True
        elif 1 <= a < 2:
            metrics['acc_dist_1_2'] += d
            if not in_effort:
                metrics['num_efforts_1_2'] += 1
                in_effort = True
        elif 2 <= a < 3:
            metrics['acc_dist_2_3'] += d
            if not in_effort:
                metrics['num_efforts_2_3'] += 1
                in_effort = True
        elif 3 <= a < 4:
            metrics['acc_dist_3_4'] += d
            if not in_effort:
                metrics['num_efforts_3_4'] += 1
                in_effort = True
        elif 5 <= a < 6:
            metrics['acc_dist_5_6'] += d
            if not in_effort:
                metrics['num_efforts_5_6'] += 1
                in_effort = True
        else:
            # Si sale de todos los rangos, reseteo flag
            in_effort = False

    row = {'playerId': player_id}
    for k in metrics:
        row[k] = round(metrics[k], 2) if isinstance(metrics[k], float) else metrics[k]
    return pd.DataFrame([row])
