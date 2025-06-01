import math
import pandas as pd


def pot_metabolica_individual(data, player_id, frame_duration):
    """
    Calcula HMLD, HMLe y Power Metabolic AVG únicamente para el jugador especificado.

    Args:
        data: Lista de diccionarios con datos de seguimiento (cada frame).
        player_id: ID del jugador al que queremos limitar el cálculo.
        frame_duration: Duración de un frame en segundos.

    Returns:
        Un DataFrame de pandas con una sola fila y columnas:
          ['playerId', 'HMLD', 'HMLe', 'Power_Metabolic_AVG'].
    """
    # Variables para acumular métricas de este jugador
    potencia_metabolica_total = 0.0
    num_frames = 0
    HMLD = 0.0
    HMLe = 0
    in_effort_hm = False
    previous_speed = 0.0
    previous_position = None

    # Recorremos frames desde el segundo (índice 1) para comparar con el anterior
    for frame_index in range(1, len(data)):
        frame = data[frame_index]
        prev_frame = data[frame_index - 1]

        # Saltar si hay cambio de periodo
        if frame.get('period') != prev_frame.get('period'):
            continue

        # Buscar al jugador en el frame actual
        current_player = None
        for p in frame['homePlayers'] + frame['awayPlayers']:
            if p['playerId'] == player_id:
                current_player = p
                break
        if current_player is None:
            continue

        speed = current_player.get('speed', 0.0)
        current_position = tuple(current_player['xyz'])

        # Calcular aceleración (solo positiva)
        acceleration = (speed - previous_speed) / frame_duration
        aceleracion = max(0.0, acceleration)

        # Constantes del modelo
        C1 = 15.5
        C2 = 0.21
        C3 = 0.004

        # Fórmula de potencia metabólica
        potencia_metabolica = (
            C1
            + C2 * speed
            + C3 * (speed ** 3)
            + aceleracion * (0.43 * speed + 0.32 * speed ** 2 + 0.008 * speed ** 3)
        )

        # Cálculo de distancia recorrida desde posición anterior
        distance = 0.0
        if previous_position is not None:
            distance = math.dist(previous_position, current_position)

        # Acumulamos potencia y frames
        potencia_metabolica_total += potencia_metabolica
        num_frames += 1

        # Si supera el umbral, acumulamos HMLD y comprobamos HMLe
        if potencia_metabolica > 25.5:
            HMLD += distance
            if not in_effort_hm:
                HMLe += 1
                in_effort_hm = True
        else:
            in_effort_hm = False

        # Actualizamos posición y velocidad para la siguiente iteración
        previous_position = current_position
        previous_speed = speed

    # Calcular Power Metabolic AVG
    if num_frames > 0:
        Power_Metabolic_AVG = potencia_metabolica_total / num_frames
    else:
        Power_Metabolic_AVG = 0.0

    # Construir DataFrame de salida (solo una fila)
    row = {
        'playerId': player_id,
        'HMLD': round(HMLD, 2),
        'HMLe': HMLe,
        'Power_Metabolic_AVG': round(Power_Metabolic_AVG, 2)
    }
    return pd.DataFrame([row])