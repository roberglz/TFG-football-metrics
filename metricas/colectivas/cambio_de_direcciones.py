import numpy as np
import pandas as pd
import json
import math
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter





def calcular_velocidades(data, frame_duration=0.2):
    """
    Calcula la velocidad de los jugadores basándose en la diferencia de posición entre frames.

    Args:
        data: Lista de diccionarios con datos de seguimiento.
        frame_duration: Duración de un frame en segundos.
        maxspeed: Velocidad máxima permitida para evitar valores atípicos.

    Returns:
        Una nueva lista de diccionarios con la velocidad calculada.
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





def cambios_direccion(data, frame_duration=0.2, min_speed=6.944,  # Categoriza solo > 6.944 m/s (25km/h)
                                 min_acceleration=3):                     # y 3 m/s2
    """
    Calcula los cambios de dirección que cumplen con los criterios de
    velocidad y aceleración.

    Args:
        data: Lista de diccionarios con datos de seguimiento.
        frame_duration: Duración de un frame en segundos.
        min_speed: Velocidad mínima en m/s para considerar un cambio de dirección.
        min_acceleration: Aceleración mínima en m/s² para considerar un cambio de dirección.
        position_tolerance: Distancia mínima entre posiciones para considerar un cambio de dirección.

    Returns:
        Un DataFrame de pandas con la información de los cambios de dirección.
    """
    player_changes = []

    for frame_index in range(1, len(data)):  # Empieza por el segundo frame
        frame = data[frame_index]
        previous_frame = data[frame_index - 1]


        current_period = frame.get('period')
        previous_period = previous_frame.get('period')

        # Salta si hay un cambio de periodo
        if current_period != previous_period:
            continue


        for player in frame['homePlayers'] + frame['awayPlayers']:
            player_id = player['playerId']

            # Get current and previous positions and speeds
            current_position = np.array(player['xyz'])[:2]  # Consider only x, y
            previous_position = next((p['xyz'][:2] for p in previous_frame['homePlayers'] + previous_frame['awayPlayers'] if p['playerId'] == player_id), None)

            # Skip if previous position is not available
            if previous_position is None:
                continue

            distance = np.linalg.norm(current_position - previous_position)  # Calcula la distancia euclidea
            current_speed = player['speed']

            # Obtiene datos del jugador del frame anterior


            previous_player_data = next((p for p in previous_frame['homePlayers'] + previous_frame['awayPlayers'] if p['playerId'] == player_id), None)

            if previous_player_data is not None:
                previous_speed = previous_player_data['speed']
            else:
                previous_speed = 0


            # Calcula el cambio en velocidad y aceleracion
            velocity_change = current_speed - previous_speed
            acceleration = velocity_change / frame_duration



            # Skipea si no se cumple las condiciones minimas de aceleracion y velocidad
            if current_speed < min_speed or abs(acceleration) < min_acceleration:
                continue




                # Calculate direction vectors
            current_direction = current_position - previous_position

                #Get a previous frame where the previous_position was different to ensure
                #previous direction is taken from a different position
            prev_frame_index = frame_index - 1

                # Find the previous position in the previous frames
            previous_position_2_frames_ago = None

                #Iterate through the previous frames
                #Until it finds a frame where the player's position was different.
            while prev_frame_index > 0 and previous_position_2_frames_ago is None:

                    #Search the player in the previous frame
                    previous_player_data_2_frames_ago = next((p for p in data[prev_frame_index]['homePlayers'] + data[prev_frame_index]['awayPlayers'] if p['playerId'] == player_id), None)

                    #If player was in the previous frames , obtain his position
                    if previous_player_data_2_frames_ago:
                        previous_position_2_frames_ago = previous_player_data_2_frames_ago['xyz'][:2]

                        #Check if the previous position has changed, break the loop if changed.
                        if not np.array_equal(previous_position_2_frames_ago, previous_position):
                           break
            prev_frame_index -= 1

                #We only get the previous position to calculate previous direction if current previous position differs from
                #the position of 2 frames before. Otherwise previous direction vector will be 0,0 and lead to errors.

                #If the previous position 2 frames ago has been found
            if previous_position_2_frames_ago is not None:
                   #Calculate the previous direction vector.
                   # Convert lists to NumPy arrays before subtraction
                    previous_direction = np.array(previous_position) - np.array(previous_position_2_frames_ago)

            else :

                    #If no previous positions is found, the direction vector is assumed as 0,0.
                    previous_direction = np.array([0, 0])



            angle_rad = np.arctan2(current_direction[1], current_direction[0]) - np.arctan2(previous_direction[1], previous_direction[0])
            angle_deg = abs(np.degrees(angle_rad))



            # Categoriza los cambios de direccion
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


    # Crea y devuelve el dataframe
    df_changes = pd.DataFrame(player_changes)
    return df_changes