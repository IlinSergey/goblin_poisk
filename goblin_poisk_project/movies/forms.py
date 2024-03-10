from django import forms
from django.utils import timezone

from .models import Director, Movie, MovieGenre, Review


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


class MovieFilterForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=MovieGenre.objects.all(),
        required=False,
        label='Жанр',
        )
    year = forms.IntegerField(
        min_value=1895,
        max_value=timezone.now().year,
        required=False,
        label='Год',
        )
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        required=False,
        label='Рейтинг',
    )


class MovieSearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 10, 'cols': 40})}
