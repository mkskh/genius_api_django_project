from django import forms


class SearchForm(forms.Form):
    search = forms.CharField()


class GetLyricsForm(forms.Form):
    track_id = forms.CharField()