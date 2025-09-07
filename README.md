# Physical Metrics Visualizer 🧠

This repository presents an interactive application developed in Python with Streamlit, focused on analyzing physical performance in football through the calculation and visualization of advanced metrics extracted from tracking data. The tool allows dynamic exploration of both individual and collective player information, facilitating the study of physical patterns, anomaly detection, and performance evolution over time.

## Estructura del proyecto

```
TFG-football-metrics/
│
├── app.py
├── requirements.txt
├── README.md
│
├── interfaz/
│   ├── sidebar.py
│   ├── paginas.py
│   ├── visualizaciones.py
│   ├── visualizaciones_metricas.py
│   └── imagenes/
│       └── portada.jpg
│
├── servicios/
│   ├── clustering.py
│   ├── estudiar_evolucion.py
│   ├── grafo_similitud.py
│   ├── jugadores.py
│   ├── procesa_partidos.py
│   └── visualizar_partidos.py
│
├── metricas/
│   ├── colectivas/
│   │   ├── cambio_de_direcciones.py
│   │   ├── distancia_aceleraciones.py
│   │   ├── distancia_umbrales_estandar.py
│   │   ├── distancia_umbrales_relativos.py
│   │   ├── metricas_seleccionadas.py
│   │   ├── potencia_metabolica.py
│   │   └── ritmo_de_juego.py
│   └── individuales/
│       ├── cambio_de_direcciones_individual.py
│       ├── distancia_aceleraciones_individual.py
│       ├── distancia_umbrales_estandar_individual.py
│       ├── distancia_umbrales_relativos_individual.py
│       ├── potencia_metabolica_individual.py
│       └── ritmo_de_juego_individual.py
│
├── utils/
│   ├── agrupacion_metricas.py
│   ├── formato_columnas.py
│   └── metricas_seleccionadas.py
│
├── config/
│   ├── equipos.json
│   ├── dicc_jugadores.json
│   ├── unidades_metricas.json
│   ├── anomalias.csv
│   └── metricas_con_nombres.csv
│
├── datos/   ← Optional folder, not included due to confidentiality and size.
├── estudios/ ← Auxiliary scripts used during development.
```

## Installation

> **Requirements:** Python 3.10.7 or higher

1. Clone the repository:

   ```bash
   git clone https://github.com/roberglz/TFG-football-metrics.git
   cd TFG-football-metrics
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Install all dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application with:

```bash
streamlit run app.py
```

---

> **Note**: All external library imports are managed in `requirements.txt`. Make sure to install it before running the application.  
> **Important**: To ensure proper functionality, you must have the `/datos` folder with the dataset used in the project. Without it, metrics cannot be calculated and individual evolution analysis will not be possible.