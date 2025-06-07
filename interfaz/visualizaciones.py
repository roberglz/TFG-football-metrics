import streamlit as st
import pandas as pd
import altair as alt
from servicios.jugadores import reemplazar_ids_por_nombres, cargar_diccionario_jugadores
from interfaz.visualizaciones_metricas import (
    mostrar_potencia, mostrar_ritmo, mostrar_cambios,
    mostrar_aceleraciones, mostrar_umbral_est, mostrar_umbral_rel
)
from utils.agrupacion_metricas import GRUPOS_METRICAS
import matplotlib.pyplot as plt
import seaborn as sns
from servicios.clustering import clustering_perfiles

def mostrar_metricas(resultados):
    dicc = cargar_diccionario_jugadores()

    funciones_metrica = {
        'potencia': mostrar_potencia,
        'ritmo': mostrar_ritmo,
        'cambios': mostrar_cambios,
        'aceleraciones': mostrar_aceleraciones,
        'umbral_est': mostrar_umbral_est,
        'umbral_rel': mostrar_umbral_rel
    }

    for clave, funcion in funciones_metrica.items():
        if clave in resultados:
            df = reemplazar_ids_por_nombres(resultados[clave], dicc)
            funcion(df)


def _obtener_label_legible(internal_key):
    """
    Dado el identificador interno de la métrica (por ejemplo "HMLe" o "acc_dist_1_2"),
    busca en GRUPOS_METRICAS y devuelve la etiqueta legible correspondiente.
    """
    for grupo, mapping in GRUPOS_METRICAS.items():
        for legible, interno in mapping.items():
            if interno == internal_key:
                return legible
    # Si no se encuentra, devolvemos el mismo internal_key
    return internal_key


def mostrar_evolucion(resultados, metrica_label_legible):


    if not resultados:
        st.warning("No hay datos para mostrar evolución.")
        return

    # 1) Si viene como lista, extraer el primer elemento (clave interna)
    if isinstance(metrica_label_legible, list) and len(metrica_label_legible) > 0:
        metrica_label_legible = metrica_label_legible[0]

    # 2) Obtener el nombre legible real buscando en GRUPOS_METRICAS
    nombre_legible = _obtener_label_legible(metrica_label_legible)

    # 3) Construir DataFrame y renombrar columna 'valor' por el nombre legible
    df = pd.DataFrame(resultados)
    df = df.rename(columns={"valor": nombre_legible})

    # 4) Preparar gráfico de línea con puntos unidos
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('match:N', title='Partido'),
        y=alt.Y(f'{nombre_legible}:Q', title=nombre_legible),
        tooltip=['match', nombre_legible]
    ).properties(
        width=700,
        height=400
    )

    # 5) Mostrar en Streamlit
    st.subheader(f"Evolución de {nombre_legible} a lo largo de los encuentros")
    st.altair_chart(chart, use_container_width=True)

def mostrar_clustering():
    st.header("Clasificación automática de perfiles físicos (K-Means)")


    df_cluster, resumen = clustering_perfiles()

    st.subheader("Visualización 2D de perfiles")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_cluster, x="PCA1", y="PCA2", hue="perfil_fisico", ax=ax, palette="Set2")
    ax.set_title("Perfiles físicos de jugadores (K-Means + PCA)")
    st.pyplot(fig)

    st.subheader("Métricas medias por perfil")
    st.dataframe(resumen.style.format(precision=2))

    st.subheader("Datos con perfil asignado")
    st.dataframe(df_cluster)