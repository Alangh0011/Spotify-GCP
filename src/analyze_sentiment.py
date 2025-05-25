import pandas as pd
from textblob import TextBlob

# Leer el CSV con las letras
filename = input("Archivo CSV con letras (ej: ../data/DE_LA_ROSE_top_tracks_letras.csv): ")
df = pd.read_csv(filename)

def get_sentiment(text):
    try:
        blob = TextBlob(str(text))
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except Exception as e:
        print(f"Error analizando: {e}")
        return 0, 0

# Analizar sentimiento para cada letra
df[['sentiment_polarity', 'sentiment_subjectivity']] = df['lyrics'].apply(lambda x: pd.Series(get_sentiment(x)))

# Guardar resultado
outfilename = filename.replace('.csv', '_sentiment.csv')
df.to_csv(outfilename, index=False)
print(f"Archivo con sentimiento guardado: {outfilename}")