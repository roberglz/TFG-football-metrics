import math
import pandas as pd





def pot_metabolica(data, frame_duration):
  """Calcula HMLD, HMLe y Power Metabolic AVG."""
  player_metrics = {}

  for frame_index, frame in enumerate(data):

    frame = data[frame_index]
    previous_frame = data[frame_index - 1]


    current_period = frame.get('period')
    previous_period = previous_frame.get('period')


    if current_period != previous_period: # Salta si hay un cambio de parte
        continue


    for player in frame['homePlayers'] + frame['awayPlayers']:
      player_id = player['playerId']
      speed = player['speed']
      current_position = tuple(player['xyz'])



      # Inicializa métricas para el jugador si no existe:
      if player_id not in player_metrics:
        player_metrics[player_id] = {
            'potencia_metabolica_total': 0,
            'num_frames': 0,
            'HMLD': 0,
            'HMLe': 0,
            'in_effort_hm': False,
            'previous_speed': 0,
            'previous_position': None
        }



      acceleration = (speed - player_metrics[player_id]['previous_speed']) / frame_duration

      velocidad = speed
      C1 = 15.5
      C2 = 0.21
      C3 = 0.004
      aceleracion = max(0, acceleration)
      potencia_metabolica = C1 + C2 * velocidad + C3 * velocidad ** 3 + aceleracion * (0.43 * velocidad + 0.32 * velocidad ** 2 + 0.008 * velocidad ** 3)


      # Calcula la distancia desde la posición anterior
      distance = 0
      if player_metrics[player_id]['previous_position'] is not None:
            previous_pos = player_metrics[player_id]['previous_position']
            distance = math.dist(previous_pos, current_position)


      player_metrics[player_id]['potencia_metabolica_total'] += potencia_metabolica
      player_metrics[player_id]['num_frames'] += 1

      if potencia_metabolica > 25.5:
          player_metrics[player_id]['HMLD'] += distance
          if not player_metrics[player_id]['in_effort_hm']:
              player_metrics[player_id]['HMLe'] += 1
              player_metrics[player_id]['in_effort_hm'] = True
      else:
          player_metrics[player_id]['in_effort_hm'] = False



      # Actualiza la posición y velocidad previas
      player_metrics[player_id]['previous_position'] = current_position
      player_metrics[player_id]['previous_speed'] = speed





  # Calcula Power Metabolic AVG
  for player_id, metrics in player_metrics.items():
    metrics['Power_Metabolic_AVG'] = metrics['potencia_metabolica_total'] / metrics['num_frames']

  table_data = []
  for player_id, metrics in player_metrics.items():
      table_data.append({
          'playerId': player_id,
          'HMLD': round(metrics['HMLD'], 2),
          'HMLe': metrics['HMLe'],
          'Power_Metabolic_AVG': round(metrics['Power_Metabolic_AVG'], 2)
      })


  df = pd.DataFrame(table_data)
  return df































# COMPARAR ENTRE PARTES

"""
metricas_por_partes = calcular_metricas_por_partes(data_5hz, 0.2)

# Mostrar resultados por partes
for period, df in metricas_por_partes.items():
    print(f"\nMétricas para el período {period}:")
    display(df) """



  # INTERVALOS DE 5 MIN

"""

metricas_por_intervalo = calcular_metricas_por_intervalo(data_5hz, 0.2, 5) # 5 MINUTOS

# Mostrar resultados por intervalo
for interval, df in metricas_por_intervalo.items():
    print(f"\n📊 Métricas para el intervalo {interval}:")
    display(df)  # Asegura que todas las métricas sean visibles """