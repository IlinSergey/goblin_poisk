import pytest
from pytest_django.asserts import assertTemplateUsed

from movies.forms import MovieForm
from movies.models import Movie


@pytest.mark.django_db
class TestMovieAddView:

    def test__movie_add_view__success_get(self, client):
        response = client.get('/movie/add/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_add.html')
        assert response.context['form'] is not None
        assert response.context['form'].__class__.__name__ == 'MovieForm'

    def test__movie_add_view__success_post(self, client, create_movie_form):
        form = create_movie_form
        assert form.is_valid()
        response = client.post('/movie/add/', form.data)
        assert response.status_code == 302
        assert response.url == '/'
        assert Movie.objects.get(title='Test movie') is not None
        added_movie = Movie.objects.get(title='Test movie')
        added_movie.delete()

    def test__movie_add_view__exist(self, client):
        form = MovieForm(data={
            'title': 'Джон Уик',
            'release_year': 2014,
            'director': 4,
            'description': 'Test description',
            'genres': [1],
            'length': 120,
            'original_rating': 8.5,
        })
        response = client.post('/movie/add/', form.data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_add.html')
        assert response.context['form'].errors == {
            '__all__': ['Фильм с такими значениями полей Название фильма, Год и Режиссер уже существует.']
            }

    def test__movie_add_view__has_not_required_fields(self, client):
        form = MovieForm(data={
            'release_year': 2014,
            'director': 4,
            'description': 'Test description',
            'genres': [1],
            'length': 120,
            'original_rating': 8.5,
        })
        response = client.post('/movie/add/', form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            'title': ['Обязательное поле.'],
            }

    def test__movie_add_view__not_valid_form(self, client):
        response = client.post('/movie/add/', {})
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_add.html')
        assert response.context['form'] is not None
        assert response.context['form'].__class__.__name__ == 'MovieForm'

    def test__movie_add_view__not_allowed(self, client):
        response = client.put('/movie/add/')
        assert response.status_code == 405
