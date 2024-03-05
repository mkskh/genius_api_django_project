from django.shortcuts import render
import requests

from .forms import SearchForm, GetLyricsForm


def search_artist(request):
    form = SearchForm()
    key = request.GET.get('search')

    if key:
        url = "https://genius-song-lyrics1.p.rapidapi.com/search/"

        querystring = {"q":f"{key}","per_page":"10","page":"1"}

        headers = {
            "X-RapidAPI-Key": "df55fa19a6mshd70b63331cfb2cep14f329jsn16f472d61208",
            "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()

        tracks_list = []
        for result in response['hits']:
            track = result['result']
            name = track['full_title']
            id = track['id']
            res = f"- {name}, id: {id}"
            tracks_list.append(res)
        
        return render(request, 'home.html', {'tracks_list': tracks_list, 'form': form})
    
    return render(request, 'home.html', {'form': form})


def get_lyrics(request):
    form = GetLyricsForm()
    key = request.GET.get('track_id')

    if key:
        url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"

        querystring = {"id":f"{key}"}

        headers = {
            "X-RapidAPI-Key": "df55fa19a6mshd70b63331cfb2cep14f329jsn16f472d61208",
            "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        lyrics = response['lyrics']['lyrics']['body']['html']

        return render(request, 'lyrics.html', {'lyrics': lyrics, 'form': form})
    
    return render(request, 'lyrics.html', {'form': form})