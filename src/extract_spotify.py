import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configura las credenciales de Spotify
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')

#Inicializar spotify con las credenciales
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-library-read"
))

def get_artist_top_tracks(artist_name, country="US"):
    """
    Función para obtener las canciones más populares de un artista.
    
    Parámetros:
        artist_name (str): Nombre del artista.
        country (str): Código del país para los resultados. Default: "US".
    
    Retorna:
        pd.DataFrame: DataFrame con las canciones más populares del artista.
    """
    # Buscar el artista por nombre
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if not results['artists']['items']:
        print(f"No se encontró el artista: {artist_name}")
        return pd.DataFrame()
    
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    print(f"Artista encontrado: {artist['name']} (ID: {artist_id})")

    # Obtener las canciones más populares del artista
    top_tracks = sp.artist_top_tracks(artist_id, country=country)
    tracks = []
    for track in top_tracks['tracks']:
        tracks.append({
            'song_name': track['name'],
            'popularity': track['popularity'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'preview_url': track['preview_url']
        })
    
    return pd.DataFrame(tracks)

if __name__ == "__main__":
    artist_name = input("Ingresa el nombre del artista: ")
    country = input("Ingresa el código del país (default: US): ") or "US"
    
    # Obtener las canciones del artista
    df = get_artist_top_tracks(artist_name, country)
    if not df.empty:
        # Guardar los datos en un archivo CSV
        output_file = f"../data/{artist_name.replace(' ', '_')}_top_tracks.csv"
        df.to_csv(output_file, index=False)
        print(f"Datos guardados en: {output_file}")
    else:
        print("No se generaron datos para guardar.")