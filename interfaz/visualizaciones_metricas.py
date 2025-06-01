import streamlit as st
import pandas as pd
from utils.formato_columnas import añadir_unidades_columnas

def mostrar_potencia(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Potencia Metabólica")
    st.dataframe(df)

def mostrar_ritmo(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Ritmo de Juego")
    st.dataframe(df)

def mostrar_cambios(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Cambios de Dirección")
    st.dataframe(df)

def mostrar_aceleraciones(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Distancia por Aceleraciones")
    st.dataframe(df)

def mostrar_umbral_est(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Distancia por Umbrales Estándar")
    st.dataframe(df)

def mostrar_umbral_rel(df: pd.DataFrame):
    df = añadir_unidades_columnas(df)
    st.subheader("Distancia por Umbrales Relativos")
    st.dataframe(df)
