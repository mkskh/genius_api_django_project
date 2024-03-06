"""Notes URL Configuration."""
from django.urls import path
from .views import search_artist, get_lyrics, get_lyrics_link

app_name = "lyrics"
urlpatterns = [
    path('', search_artist, name="search_artist"),
    path('get_lyrics/', get_lyrics, name="get_lyrics"),
    path('lyrics_view/<int:track_id>/', get_lyrics_link, name="lyrics_view"),
]
