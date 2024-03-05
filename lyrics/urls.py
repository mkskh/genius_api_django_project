"""Notes URL Configuration."""
from django.urls import path
from .views import search_artist, get_lyrics

app_name = "lyrics"
urlpatterns = [
    path('', search_artist, name="search_artist"),
    path('get_lyrics/', get_lyrics, name="get_lyrics"),
]