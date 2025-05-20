# Interfaz de usuario

Este repositorio propone una interfaz gráfica para calcular y visualizar métricas físicas de partidos de fútbol, utilizando datos de tracking y funciones de análisis en Python.

## Estructura del proyecto

```
analisis-rendimiento-futbol/
│
├─ app.py                        
├─ requirements.txt
│
├─ datos/                       
│
├─ metricas/                      
│   ├─ potencia_metabolica.py
│   ├─ ritmo_de_juego.py
│   ├─ cambio_de_direcciones.py
│   ├─ distancia_aceleraciones.py
│   ├─ distancia_umbrales_estandar.py
│   └─ distancia_umbrales_relativos.py
│
└─ servicios/                    
    ├─ __init__.py
    └─ procesa_partidos.py       

```

## Instalación

> **Requisitos:** Python 3.10 o superior

1. Clona el repositorio:

   ```bash
   git clone https://github.com/roberglz/TFG-football-metrics.git
   cd TFG-football-metrics
   ```
2. Crea un entorno virtual (OPCIONAL):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```
3. Instala todas las dependencias desde `requirements.txt`:

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
