import os
import pandas as pd
import lyricsgenius
from dotenv import load_dotenv

# Cargar keys
load_dotenv()
GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")

# Inicializar Genius
genius = lyricsgenius.Genius(GENIUS_API_KEY, timeout=15, retries=3)

filename = input("Archivo CSV a procesar (ej: ../data/DE_LA_ROSE_top_tracks.csv): ")
artist_name = input("Nombre del artista: ")  # Solo una vez

df = pd.read_csv(filename)

# Detectar la columna de canción automáticamente
columns = set(df.columns)
possible_song_cols = [c for c in columns if 'song' in c.lower() or 'name' in c.lower()]
song_col = possible_song_cols[0] if possible_song_cols else input("Columna de canción: ")

print(f"Usando columna de canción: {song_col}")

def get_lyrics(row):
    try:
        song = genius.search_song(row[song_col], artist_name)
        return song.lyrics if song else ''
    except Exception as e:
        print(f"Error con {row[song_col]}: {e}")
        return ''

df['lyrics'] = df.apply(get_lyrics, axis=1)

outfilename = filename.replace('.csv', '_letras.csv')
df.to_csv(outfilename, index=False)
print(f"Archivo con letras guardado: {outfilename}")