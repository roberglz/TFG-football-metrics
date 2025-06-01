aceleraciones = {
    "Distancia 0–1 m/s² (m)":          "acc_dist_0_1",
    "Distancia 1–2 m/s² (m)":          "acc_dist_1_2",
    "Distancia 2–3 m/s² (m)":          "acc_dist_2_3",
    "Distancia 3–4 m/s² (m)":          "acc_dist_3_4",
    "Distancia 5–6 m/s² (m)":          "acc_dist_5_6",
    "Aceleración máxima (m/s²)":       "max_acceleration",
    "Esfuerzos 0–1 m/s²":              "num_efforts_0_1",
    "Esfuerzos 1–2 m/s²":              "num_efforts_1_2",
    "Esfuerzos 2–3 m/s²":              "num_efforts_2_3",
    "Esfuerzos 3–4 m/s²":              "num_efforts_3_4",
    "Esfuerzos 5–6 m/s²":              "num_efforts_5_6",
    "Esfuerzos > 6 m/s²":               "num_efforts_max_acc"
}

umbrales_estandar = {
    "Dist. total recorrida (m)":               "totalDistance",
    "Dist. recorrida a < 7 km/h (m)":          "walkingDistance",
    "Dist. recorrida entre 7–15 km/h (m)":     "joggingDistance",
    "Dist. recorrida entre 15–20 km/h (m)":    "lowSpeedRunningDistance",
    "Dist. recorrida entre 20-25 km/h (m)":    "highSpeedRunningDistance",
    "Dist. recorrida entre 25-30 km/h (m)":    "sprintDistance",
    "Dist. recorrida a > 30 km/h (m)":         "veryHighSpeedDistance",
    "Velocidad media (km/h)":                  "avgSpeed",
    "Velocidad máxima (km/h)":                 "maxSpeed"
}

umbrales_relativos = {
    "Dist. > 60 % máx (m)":                     "distance_above_60_percent",
    "Dist. > 75 % máx (m)":                     "distance_above_75_percent",
    "Dist. > 85 % máx (m)":                     "distance_above_85_percent",
    "Dist. > 90 % máx (m)":                     "distance_above_90_percent",
    "Dist. > 95 % máx (m)":                     "distance_above_95_percent",
    "Esfuerzos 20–25 km/h":                     "esfuerzos_high_speed_running",
    "Esfuerzos > 25 km/h":                      "esfuerzos_sprint",
    "Esfuerzos > 30 km/h":                      "esfuerzos_velocidad_muy_alta",
    "Esfuerzos > 75 % máx":                     "esfuerzos_above_75_percent",
    "Esfuerzos > 85 % máx":                     "esfuerzos_above_85_percent",
    "Esfuerzos > 90 % máx":                     "esfuerzos_above_90_percent",
    "Esfuerzos > 95 % máx":                     "esfuerzos_above_95_percent",
    "Esfuerzos ponderados":                     "esfuerzos_ponderados"
}

metabolicas = {
    "HMLD":                                     "HMLD",
    "HMLe":                                     "HMLe",
    "Power Metabolic AVG (W/kg)":               "Power_Metabolic_AVG"
}

ritmo_juego = {
    "Total (m/min)":                            "totalDistanceRhythm",
    "Caminar < 7 km/h (m/min)":                  "walkingRhythm",
    "Trote 7–15 km/h (m/min)":                   "joggingRhythm",
    "Carrera baja 15–20 km/h (m/min)":           "lowSpeedRunningRhythm",
    "Carrera alta 20–25 km/h (m/min)":           "highSpeedRunningRhythm",
    "Sprint 25–30 km/h (m/min)":                 "sprintRhythm",
    "Vel. muy alta > 30 km/h (m/min)":           "veryHighSpeedRhythm"
}

GRUPOS_METRICAS = {
    "Aceleraciones":       aceleraciones,
    "Umbrales estándar":   umbrales_estandar,
    "Umbrales relativos":  umbrales_relativos,
    "Metabólicas":         metabolicas,
    "Ritmo de juego":      ritmo_juego
}
