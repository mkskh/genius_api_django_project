from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
load_dotenv()

from .forms import SearchForm, GetLyricsForm


GENIUS_API_KEY = os.getenv('GENIUS_API_KEY')


def search_artist(request):
    '''Write artist and get top10 tracks '''
    form = SearchForm()
    key = request.GET.get('search')

    if key:
        url = "https://genius-song-lyrics1.p.rapidapi.com/search/"

        querystring = {"q":f"{key}","per_page":"10","page":"1"}

        headers = {
            "X-RapidAPI-Key": GENIUS_API_KEY, # get your own api - https://rapidapi.com/Glavier/api/genius-song-lyrics1/pricing
            "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()

        tracks = {}

        for result in response['hits']:
            track = result['result']
            name = track['full_title']
            id = track['id']
            res = f"- {name}, id: {id}"
            id = int(id)
            tracks[id] = res

        artist = response['hits'][0]['result']['artist_names']

        return render(request, 'home.html', {'tracks': tracks, 'form': form, 'artist': artist})

    else:
        tracks = {}

        return render(request, 'home.html', {'tracks': tracks, 'form': form})


def get_lyrics(request):
    '''Enter track ID and get the lyrics'''
    form = GetLyricsForm()
    key = request.GET.get('track_id')

    if key:
        url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"

        querystring = {"id":f"{key}"}

        headers = {
            "X-RapidAPI-Key": GENIUS_API_KEY, # get your own api - https://rapidapi.com/Glavier/api/genius-song-lyrics1/pricing
            "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        lyrics = response['lyrics']['lyrics']['body']['html']

        modified_content = lyrics.replace('href', 'class="text-link" href')

        artist = response['lyrics']['tracking_data']['primary_artist']
        track = response['lyrics']['tracking_data']['title']

        name = f'{artist} - {track}'

        return render(request, 'lyrics.html', {'lyrics': modified_content, 'form': form, 'name': name})
    
    return render(request, 'lyrics.html', {'form': form})


def get_lyrics_link(request, track_id):
    '''Click View and got directly to the lyrics'''
    url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"

    querystring = {"id":f"{track_id}"}

    headers = {
        "X-RapidAPI-Key": GENIUS_API_KEY, # get your own api - https://rapidapi.com/Glavier/api/genius-song-lyrics1/pricing
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    lyrics = response['lyrics']['lyrics']['body']['html']

    modified_content = lyrics.replace('href', 'class="text-link" href')

    artist = response['lyrics']['tracking_data']['primary_artist']
    track = response['lyrics']['tracking_data']['title']

    name = f'{artist} - {track}'

    return render(request, 'lyrics_view.html', {'lyrics': modified_content, 'name': name})