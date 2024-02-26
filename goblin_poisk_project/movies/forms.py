from django import forms

from .models import Director, Movie, MovieGenre


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'description']


class MovieGenreForm(forms.ModelForm):
    class Meta:
        model = MovieGenre
        fields = ['name', 'description']


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'release_year',
            'director',
            'description',
            'length',
            'genres',
            'original_rating',
            'poster',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['director'].help_text = '<br>Если Режиссера нет в списке, <a href="/director/add/">добавь его</a>.'
        self.fields['genres'].help_text = '<br>Если жанра нет в списке, <a href="/genre/add/">добавь его</a>.'
