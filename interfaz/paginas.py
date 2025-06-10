import streamlit as st

def mostrar_portada():
    st.markdown("""
        <style>
        .portada-container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 3rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            text-align: center;
        }
        .portada-title {
            font-size: 3rem;
            color: #1f77b4;
            font-weight: bold;
        }
        .portada-subtitle {
            font-size: 1.2rem;
            color: #333333;
            margin-top: 1rem;
        }
        .start-button {
            background-color: #1f77b4;
            color: white;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: background-color 0.3s ease;
        }
        .start-button:hover {
            background-color: #125a8c;
        }
        </style>

        <div class="portada-container">
            <div class="portada-title">⚽ TFG - Football Metrics 📊</div>
            <div class="portada-subtitle">
                Esta aplicación ha sido desarrollada por Roberto Gil López como parte del Trabajo de Fin de Grado "Inteligencia Artificial y 
                Visualización Avanzada aplicada al rendimiento físico en el fútbol".<br>
                Explore métricas individuales, evolución de jugadores, clustering de perfiles, detección de anomalías y más.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("interfaz/imagenes/portada.jpg", use_container_width=True)

    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 Empezar", use_container_width=True):
            st.session_state.inicio = True
            st.rerun()


def mostrar_explicacion():
    with st.expander("ℹ️ Sobre esta aplicación", expanded=True):
        st.markdown("""
        Esta plataforma permite analizar el rendimiento físico de jugadores de fútbol profesional mediante distintas técnicas de visualización y análisis automático. Sus funcionalidades incluyen:

        - 📊 **Cálculo de métricas físicas por partido**: Genera estadísticas por jugador a partir de los datos de tracking de un partido, como distancia, aceleraciones,etc.
        
        - 📈 **Estudio de la evolución individual**: Muestra cómo varía una métrica específica de un jugador a lo largo de varios partidos.

        - 🔍 **Clustering de perfiles físicos**: Agrupa a los jugadores según su rendimiento físico usando K-Means y PCA.

        - 🔗 **Grafo de similitud entre jugadores**: Permite visualizar qué jugadores son más parecidos físicamente a otro, basándose en una o varas métricas.

        - 🚨 **Detección de anomalías**: Utiliza Isolation Forest para detectar partidos atípicos en el rendimiento de un jugador, destacando qué métricas se alejan de su comportamiento habitual.

        Utiliza el menú lateral para comenzar con cada análisis.
        """)