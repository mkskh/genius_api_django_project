from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
load_dotenv()

from .forms import SearchForm, GetLyricsForm


GENIUS_API_KEY = os.getenv('GENIUS_API_KEY')


def search_artist(request):
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
    
    else:
        tracks = {}
        
    return render(request, 'home.html', {'tracks': tracks, 'form': form})
    
    # return render(request, 'home.html', {'form': form})


def get_lyrics(request, track_id):
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

        # clean_html = re.sub(r'<a.*?>(.*?)</a>', r'\1', lyrics)

        # modified_content = re.sub(r'<a\s+([^>]*)>', r'<p \1>', lyrics)
        # modified_content = modified_content.replace("</a>", "</p>")
        # modified_content = modified_content.replace("</p><br>", "</p>")

        return render(request, 'lyrics.html', {'lyrics': lyrics, 'form': form})
    
    return render(request, 'lyrics.html', {'form': form})


def get_lyrics_link(request, track_id):

    url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"

    querystring = {"id":f"{track_id}"}

    headers = {
        "X-RapidAPI-Key": GENIUS_API_KEY, # get your own api - https://rapidapi.com/Glavier/api/genius-song-lyrics1/pricing
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    lyrics = response['lyrics']['lyrics']['body']['html']

    return render(request, 'lyrics_view.html', {'lyrics': lyrics})