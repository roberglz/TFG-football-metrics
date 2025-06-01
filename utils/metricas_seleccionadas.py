# config/metricas_display.py

"""
Mapeo de nombres internos de métricas a etiquetas más legibles
para mostrar en la interfaz.
"""

METRICAS_DISPLAY = {
    # Ritmo de juego
    "walkingRhythm_ritmo":          "Ritmo caminando (m/min)",
    "joggingRhythm_ritmo":          "Ritmo trotando (m/min)",
    "lowSpeedRunningRhythm_ritmo":  "Ritmo carrera baja (m/min)",
    "highSpeedRunningRhythm_ritmo": "Ritmo carrera alta (m/min)",
    "sprintRhythm_ritmo":           "Ritmo sprint (m/min)",
    "veryHighSpeedRhythm_ritmo":    "Ritmo muy alta velocidad (m/min)",

    # Aceleraciones
    "acc_dist_3_4_aceleraciones":   "Dist. 3–4 m/s² (m)",
    "acc_dist_5_6_aceleraciones":   "Dist. 5–6 m/s² (m)",
    "max_acceleration_aceleraciones":"Aceleración máxima (m/s²)",
    "num_efforts_0_1_aceleraciones": "Esfuerzos 0–1 m/s²",
    "num_efforts_1_2_aceleraciones": "Esfuerzos 1–2 m/s²",
    "num_efforts_2_3_aceleraciones": "Esfuerzos 2–3 m/s²",
    "num_efforts_3_4_aceleraciones": "Esfuerzos 3–4 m/s²",
    "num_efforts_5_6_aceleraciones": "Esfuerzos 5–6 m/s²",
    "num_efforts_max_acc_aceleraciones": "Esfuerzos >6 m/s²",

    # Umbrales estándar
    "walkingDistance_umbral_est":   "Dist. caminando (<7 km/h)",
    "joggingDistance_umbral_est":   "Dist. trotando (7–15 km/h)",

    # Umbrales relativos
    "distance_above_95_percent_umbral_rel": "Dist. >95% velocidad máxima",
    "maxSpeed_umbral_rel":                   "Vel. máxima (umbral rel.)",
    "esfuerzos_above_95_percent_umbral_rel":"Esfuerzos >95% velocidad máxima"
}
