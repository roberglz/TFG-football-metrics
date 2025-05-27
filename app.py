import streamlit as st
import pandas as pd
from servicios.procesa_partidos import cargar_partido, calcular_metricas
from servicios.visualizar_partidos import listar_partidos
import os


st.title("Visualizador de Métricas Físicas por Partido")

# ----- Sidebar -----
partidos = listar_partidos('datos')
nombres = [p[0] for p in partidos]
rutas   = [p[1] for p in partidos]



sel = st.sidebar.selectbox("Partido", ["<elige>"] + nombres)



# Checkboxes de métricas
st.sidebar.markdown("**Elige métricas a calcular**")
opts = {
    'potencia':     st.sidebar.checkbox("Potencia metabólica"),
    'ritmo':        st.sidebar.checkbox("Ritmo de juego"),
    'cambios':      st.sidebar.checkbox("Cambios de dirección"),
    'aceleraciones':st.sidebar.checkbox("Distancia por aceleraciones"),
    'umbral_est':   st.sidebar.checkbox("Umbrales estándar"),
    'umbral_rel':   st.sidebar.checkbox("Umbrales relativos"),
}
# filtramos solo las elegidas
seleccion = [k for k,v in opts.items() if v]




if st.sidebar.button("Calcular métricas"):
    if sel == "<elige>":
        st.warning("Selecciona un partido primero.")

    elif not seleccion:
        st.warning("Marca al menos una métrica a calcular.")

    else:
        ruta = rutas[nombres.index(sel)]
        data = cargar_partido(ruta)
        resultados = calcular_metricas(data, seleccion)

        # Mostrar cada DataFrame y su gráfico
        for clave, df in resultados.items():
            st.subheader(f"Métrica: **{clave}**")
            st.dataframe(df)

            # Ejemplo de gráfica, adapta por cada métrica:
            if not df.empty:
                # tomamos la primera columna numérica que no sea playerId
                cols = [c for c in df.columns if c != 'playerId']
                st.bar_chart(df.set_index('playerId')[cols[0]])
else:
    st.info("Configura partido y métricas, luego pulsa _Calcular métricas_.")