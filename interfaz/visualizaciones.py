import streamlit as st
import pandas as pd

def mostrar_potencia(df):
    st.subheader("Potencia metabólica")
    st.dataframe(df)

def mostrar_ritmo(df):
    st.subheader("Ritmo de juego")
    st.dataframe(df)

def mostrar_cambios(df):
    st.subheader("Cambios de dirección")
    st.dataframe(df)

def mostrar_aceleraciones(df):
    st.subheader("Distancia por aceleraciones")
    st.dataframe(df)

def mostrar_umbral_est(df):
    st.subheader("Distancia por umbrales estándar")
    st.dataframe(df)

def mostrar_umbral_rel(df):
    st.subheader("Distancia por umbrales relativos")
    st.dataframe(df)

def mostrar_metricas(resultados):
    if 'potencia' in resultados:
        mostrar_potencia(resultados['potencia'])
    if 'ritmo' in resultados:
        mostrar_ritmo(resultados['ritmo'])
    if 'cambios' in resultados:
        mostrar_cambios(resultados['cambios'])
    if 'aceleraciones' in resultados:
        mostrar_aceleraciones(resultados['aceleraciones'])
    if 'umbral_est' in resultados:
        mostrar_umbral_est(resultados['umbral_est'])
    if 'umbral_rel' in resultados:
        mostrar_umbral_rel(resultados['umbral_rel'])

