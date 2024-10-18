from django.utils.crypto import get_random_string
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from django.shortcuts import redirect, render

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

def get_spotify_oauth(state):
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,  # Use the redirect URI you set in the dashboard
        scope="user-top-read",  # Adjust scope based on your app's needs
        state=state
    )

def get_spotify_object(request):
    token_info = request.session.get('token_info', None)
    state = get_random_string(16)
    # Refresh token if needed
    sp_oauth = get_spotify_oauth(state)
    if token_info and sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        request.session['token_info'] = token_info  # Update the session with new token

    # Return Spotify object if token is available
    if token_info:
        return spotipy.Spotify(auth=token_info['access_token'])
    return None

# Spotify OAuth settings (Authorization Code Flow)
def spotify_authenticate(request):
    state = get_random_string(16)
    request.session['oauth_state'] = state

    sp_oauth = get_spotify_oauth(state)
    auth_url = sp_oauth.get_authorize_url()
    print(request.session.get('next_url'))
    return redirect(auth_url)

# Callback view where Spotify will redirect the user after authentication
def spotify_callback(request):
    print("hey2", request.session.get('next_url'))
    print("hey2", request.session.get('test'))
    state = get_random_string(16)
    sp_oauth = get_spotify_oauth(state)

    # Spotify returns the authorization code in the callback URL
    code = request.GET.get('code')

    # Use the code to get the token
    token_info = sp_oauth.get_access_token(code)

    # Store token in session
    request.session['token_info'] = token_info

    next_url = request.session.get('next_url' 'top-tracks/')
    if 'next_url' in request.session:
        del request.session['next_url']

    return redirect('top_tracks')

def top_tracks(request):
    try:
        sp = get_spotify_object(request)
    except Exception as e:
        next_url = request.GET.get('next', request.path)
        request.session['next_url'] = next_url
        request.session['test'] = 'yes'
        print("hey", request.session['next_url'])
        request.session.save()
        return redirect('spotify_authenticate')  # Redirect to log in if token is not available

    print("hello")
    # Default time range (e.g., 'medium_term')
    time_range = request.GET.get('time_range', 'medium_term')

    # Fetch the user's top tracks
    results = sp.current_user_top_tracks(limit=10, time_range=time_range)
    # Extract track details
    top_tracks = []
    for track in results['items']:
        top_tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
        })
    print(top_tracks)
    return render(request, 'UsersTopTracks.html', {'top_tracks': top_tracks, 'time_range': time_range})

def top_artists(request):
    sp = get_spotify_object(request)
    if sp is None:
        return redirect('spotify_authenticate')  # Redirect to log in if token is not available

    # Default time range (e.g., 'medium_term')
    time_range = request.GET.get('time_range', 'medium_term')

    # Fetch the user's top artists
    results = sp.current_user_top_artists(limit=20, time_range=time_range)

    # Extract artist details
    top_artists = []
    for artist in results['items']:
        top_artists.append({
            'name': artist['name'],
            'popularity': artist['popularity'],
            'genres': artist['genres'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None,
        })

    return render(request, 'UsersTopArtists.html', {'top_artists': top_artists, 'time_range': time_range})