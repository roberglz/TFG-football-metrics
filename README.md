# Visualizador de métricas físicas 🧠

Este repositorio presenta una aplicación interactiva desarrollada en Python con Streamlit, orientada al análisis del rendimiento físico en fútbol mediante el cálculo y la visualización de métricas avanzadas extraídas de datos de tracking. La herramienta permite explorar dinámicamente información individual y colectiva de los jugadores, facilitando el estudio de patrones físicos, la detección de anomalías y la evolución del rendimiento a lo largo del tiempo.

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
├── datos/   ← Carpeta opcional, no incluida por motivos de confidencialidad y tamaño.
```

## Instalación

> **Requisitos:** Python 3.10.7 o superior

1. Clona el repositorio:

   ```bash
   git clone https://github.com/roberglz/TFG-football-metrics.git
   cd TFG-football-metrics
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Instala todas las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación con:

```bash
streamlit run app.py
```

---

> **Nota**: Todos los imports de librerías externas están gestionados en `requirements.txt`. Asegúrate de instalarlo antes de ejecutar la aplicación.  
> **Importante**: Para que la aplicación funcione correctamente, es necesario disponer de la carpeta `/datos` con el dataset utilizado en el proyecto. Sin ella, no será posible calcular métricas ni realizar el estudio de la evolución individual.
