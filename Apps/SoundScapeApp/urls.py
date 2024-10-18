from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify/', views.fetch_spotify_data, name='fetch_spotify_data'),
    path('spotify-authenticate/', views.spotify_authenticate, name='spotify_authenticate'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('top-tracks/', views.top_tracks, name='top_tracks'),
    path('top-artists/', views.top_artists, name='top_artists'),
]