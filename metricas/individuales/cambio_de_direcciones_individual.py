import numpy as np
import pandas as pd

def calcular_velocidades_individual(data, player_id, frame_duration=0.2):
    """
    Calcula la velocidad únicamente para el jugador especificado (player_id).

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador cuyo vector de velocidades queremos calcular.
        frame_duration: Duración de un frame en segundos.

    Returns:
        new_data: Lista de diccionarios igual al dataset original, pero con
                  la clave 'speed' solo actualizada para el player_id; el resto
                  de jugadores tendrá 'speed'=0 o conserva su valor previo si
                  existiera.
    """
    # 1) Recoger todas las posiciones (x, y) de este player_id a lo largo de los frames
    x_vals = []
    y_vals = []

    # También guardamos el índice de frame para reconstruir luego
    # Si en un frame no aparece, guardamos None (se asumirá velocidad 0)
    frame_indices = []

    for idx, frame in enumerate(data):
        encontrado = False

        # Buscar dentro de homePlayers y awayPlayers
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
            # Si no encontramos al jugador en este frame, metemos un marcador
            x_vals.append(None)
            y_vals.append(None)
            frame_indices.append(idx)

    # 2) Calcular velocidades solo en los instantes en que el jugador aparece consecutivamente
    speeds = [0.0] * len(x_vals)  # velocidad 0 por defecto para el primer frame o ausencias

    # Recorremos y calculamos diferencias siempre que tengamos dos posiciones consecutivas válidas
    for i in range(1, len(x_vals)):
        if x_vals[i] is None or x_vals[i-1] is None:
            speeds[i] = 0.0
        else:
            dx = x_vals[i] - x_vals[i-1]
            dy = y_vals[i] - y_vals[i-1]
            speed = np.sqrt(dx * dx + dy * dy) / frame_duration
            speeds[i] = speed

    # 3) Reconstruir new_data: para cada frame, asignar velocidad solo a este player_id
    new_data = []
    # Llevamos contador de cuántas veces hemos añadido un speed no nulo
    # (en realidad, speeds[i] ya está alineado con frame_indices[i])
    # Pero si en un mismo frame hubiera múltiples apariciones (no debería),
    # tomamos el primero que coincida
    for idx, frame in enumerate(data):
        new_frame = {k: v if k not in ('homePlayers', 'awayPlayers') else [] for k, v in frame.items()}

        # Índice en speeds/formas de x_vals coincide con idx vía frame_indices
        # Lo localizamos:
        pos_list = [pos for pos, fidx in enumerate(frame_indices) if fidx == idx]
        speed_val = 0.0
        if len(pos_list) > 0:
            # Debe haber exactamente uno, pero tomamos el primero
            speed_val = speeds[pos_list[0]]
        else:
            speed_val = 0.0

        # Reconstruimos homePlayers y awayPlayers
        for player_type in ('homePlayers', 'awayPlayers'):
            for p in frame[player_type]:
                new_p = p.copy()
                if p['playerId'] == player_id:
                    new_p['speed'] = speed_val
                else:
                    # Si existía algún valor previo en 'speed', lo dejamos; 
                    # sino forzamos a 0
                    new_p['speed'] = p.get('speed', 0.0)
                new_frame[player_type].append(new_p)

        new_data.append(new_frame)

    return new_data


def cambios_direccion_individual(data, player_id, frame_duration=0.2,
                                 min_speed=6.944, min_acceleration=3):
    """
    Calcula los cambios de dirección únicamente para el jugador especificado.

    Args:
        data: Lista de diccionarios con datos de seguimiento (ya con 'speed' calculado).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.
        min_speed: Velocidad mínima en m/s para considerar un cambio de dirección.
        min_acceleration: Aceleración mínima en m/s² para considerar un cambio de dirección.

    Returns:
        df_changes: DataFrame de pandas con la información de los cambios de dirección
                    de ese único jugador (columns: playerId, frame, speed, acceleration,
                    angle_change, category).
    """
    player_changes = []

    # Para cada frame (empezamos en 1 para comparar con anterior)
    for frame_index in range(1, len(data)):
        frame = data[frame_index]
        prev_frame = data[frame_index - 1]

        # Si hay cambio de periodo, saltamos
        if frame.get('period') != prev_frame.get('period'):
            continue

        # Buscar al jugador actual en el frame
        current_player = None
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                current_player = p
                break
        if current_player is None:
            continue

        # Buscar al jugador en el frame anterior
        previous_player = None
        for p in prev_frame['homePlayers'] + prev_frame['awayPlayers']:
            if p['playerId'] == player_id:
                previous_player = p
                break
        if previous_player is None:
            continue

        # Extraer posiciones (solo x,y) y velocidades
        current_position = np.array(current_player['xyz'][:2])
        previous_position = np.array(previous_player['xyz'][:2])
        current_speed = current_player.get('speed', 0.0)
        previous_speed = previous_player.get('speed', 0.0)

        # Cálculo de aceleración
        velocity_change = current_speed - previous_speed
        acceleration = velocity_change / frame_duration

        # Si no cumple mínimos, saltamos
        if current_speed < min_speed or abs(acceleration) < min_acceleration:
            continue

        # Vector de dirección actual
        current_direction = current_position - previous_position

        # Buscamos la posición un frame atrás que sea distinta, para vector previo
        prev_frame_idx = frame_index - 1
        previous_position_2 = None
        while prev_frame_idx > 0 and previous_position_2 is None:
            candidate = None
            for p in data[prev_frame_idx]['homePlayers'] + data[prev_frame_idx]['awayPlayers']:
                if p['playerId'] == player_id:
                    candidate = np.array(p['xyz'][:2])
                    break
            if candidate is not None and not np.array_equal(candidate, previous_position):
                previous_position_2 = candidate
                break
            prev_frame_idx -= 1

        if previous_position_2 is not None:
            previous_direction = previous_position - previous_position_2
        else:
            previous_direction = np.array([0.0, 0.0])

        # Cálculo del ángulo entre vectores
        angle_rad = np.arctan2(current_direction[1], current_direction[0]) \
                    - np.arctan2(previous_direction[1], previous_direction[0])
        angle_deg = abs(np.degrees(angle_rad))

        # Categorizar por rango de ángulo
        if 0 < angle_deg < 45:
            category = '<45º'
        elif 45 <= angle_deg < 90:
            category = '45-90º'
        elif 90 <= angle_deg < 135:
            category = '90-135º'
        elif 135 <= angle_deg <= 180:
            category = '135-180º'
        else:
            category = 'other'

        player_changes.append({
            'playerId': player_id,
            'frame': frame_index,
            'speed': current_speed,
            'acceleration': acceleration,
            'angle_change': angle_deg,
            'category': category
        })

    df_changes = pd.DataFrame(player_changes)
    return df_changes
