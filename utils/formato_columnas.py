def añadir_unidades_columnas(df):
    """
    Añade unidades a los nombres de las columnas del DataFrame según palabras clave,
    siguiendo un orden de prioridad establecido. Si el nombre contiene 'esfuerzos',
    no se añade ninguna unidad.
    """

    unidades_keywords = [
        ("rhythm", "m/min"),
        ("distance", "m"),
        ("angle", "°"),
        ("speed", "m/s"),
        ("acc", "m/s²"),
        ("HMLD", "W/kg"),
        ("AVG", "W/kg"),
        ("HMLe", "(high metabolic load efforts)"),
        ("minutes", "min"),
    ]

    nuevas_columnas = []
    for col in df.columns:
        col_lower = col.lower()

        # Excluir unidades si contiene 'esfuerzos'
        if "esfuerzos" in col_lower:
            nuevas_columnas.append(col)
            continue

        unidad = ""
        for palabra, u in unidades_keywords:
            if palabra.lower() in col_lower:
                unidad = f" {u}" if u.startswith("(") else f" ({u})"
                break
        nuevas_columnas.append(col + unidad)

    df.columns = nuevas_columnas
    return df
