# Visualizador de métricas físicas 🧠

Este repositorio propone una interfaz gráfica para calcular y visualizar métricas físicas de partidos de fútbol, utilizando datos de tracking y funciones de análisis en Python.
*PENDIENTE DE ACTUALIZAR*

## Estructura del proyecto

```
TFG-football-metrics/
│
├── app.py
│
├── interfaz/
│ ├── sidebar.py
│ ├── visualizaciones.py
│ └── visualizaciones_metricas.py
│
├── servicios/
│ ├── procesa_partidos.py
│ └── visualizar_partidos.py
│
├── utils/
│ └── formato_columnas.py
│
├── config/
│ ├── equipos.json
│ └── dicc_jugadores.json
│
├── requirements.txt
└── README.md       

```

## Instalación

> **Requisitos:** Python 3.10 o superior



1. Instala IPython:

   ```bash
   pip install ipython

   ```

2. Clona el repositorio:

   ```bash
   git clone https://github.com/roberglz/TFG-football-metrics.git
   cd TFG-football-metrics
   ```
3. Crea un entorno virtual (OPCIONAL):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```
4. Instala todas las dependencias desde `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación Streamlit:

   ```bash
   streamlit run app.py
   ```

---

> **Nota**: Todos los imports de librerías externas se gestionan a través de `requirements.txt`. Asegúrate de instalarlo antes de ejecutar la aplicación.
