import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuración de credenciales
credentials = service_account.Credentials.from_service_account_file(
    'credentials/bigquery-key.json'  # Cambia esto al path de tu JSON
)

# Configuración del cliente de BigQuery
project_id = "tu-proyecto-id"  # Reemplaza con el ID de tu proyecto
dataset_id = "spotify_dataset"  # Nombre del dataset en BigQuery
table_id = "processed_tracks"  # Nombre de la tabla en BigQuery
client = bigquery.Client(credentials=credentials, project=project_id)

# Cargar el CSV procesado
filename = "../data/de_la_rose_top_tracks_letras_sentiment.csv"  # Cambia si es necesario
df = pd.read_csv(filename)

# Subir los datos a BigQuery
print(f"Subiendo datos a BigQuery: {project_id}.{dataset_id}.{table_id}")
df.to_gbq(f"{dataset_id}.{table_id}", project_id=project_id, if_exists="replace", credentials=credentials)
print("Datos subidos exitosamente.")