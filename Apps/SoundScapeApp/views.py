from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from django.conf import settings
from django.shortcuts import render

# Initialize OAuth globally
sp_oauth = SpotifyOAuth(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIFY_REDIRECT_URI,
    scope='user-top-read'
)

sp = None  # Global Spotify instance

# Create your views here.
def index(request):
    return render(request, 'AppBase.html')

def fetch_spotify_data(request):
    # Spotify API authorization
    sp2 = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    ))

    # Get the search query from the request, or default to an empty string
    query = request.GET.get('q', '')  # Use an empty string if no query is provided

    try:
        results = sp2.search(q=query, limit=10)
        songs = results['tracks']['items']
    except Exception as e:
        songs = []
        print(f"Error fetching data from Spotify: {e}")

    # Pass the data to the template
    return render(request, 'SpotifyData.html', {
        'songs': songs,
        'query': query,  # Pass the query back to the template for the form
    })


def spotify_authenticate(request):
    return None


def spotify_callback(request):
    return None


def top_tracks(request):
    return None


def top_artists(request):
    return None