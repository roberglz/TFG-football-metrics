# Physical Metrics Visualizer 🧠

This repository presents an interactive application developed in Python with Streamlit, focused on analyzing physical performance in football through the calculation and visualization of advanced metrics extracted from tracking data. The tool allows dynamic exploration of both individual and collective player information, facilitating the study of physical patterns, anomaly detection, and performance evolution over time.


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
