import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def clustering_perfiles(k: int = 3):

    df = pd.read_csv("C:/Users/rober/Desktop/UNIVERSIDAD/TFG/code/TFG-football-metrics/config/metricas_con_nombres.csv")  
    
    columnas_metricas = df.columns[1:]  # asume que la primera columna es 'Jugador'
    df_metricas = df[columnas_metricas]


    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_metricas)

    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df_resultado = df_metricas.copy()
    df_resultado['perfil_fisico'] = clusters
    df_resultado['PCA1'] = X_pca[:, 0]
    df_resultado['PCA2'] = X_pca[:, 1]

    resumen = df_resultado.groupby('perfil_fisico').mean(numeric_only=True)

    return df_resultado, resumen
