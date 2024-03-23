import pytest
from pytest_django.asserts import assertTemplateUsed

from movies.forms import MovieGenreForm
from movies.models import MovieGenre


@pytest.mark.django_db
class TestGenreAddView:

    def test__genre_add_view__get(self, client):
        response = client.get('/genre/add/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/genre_add.html')
        assert response.context['form'].__class__.__name__ == 'MovieGenreForm'

    def test__genre_add_view__success_post(self, client):
        form = MovieGenreForm(data={
            'name': 'Test genre',
            'description': 'Test description'
        })
        assert form.is_valid()
        response = client.post('/genre/add/', form.data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/success_added_director_or_genre.html')
        added_genre = MovieGenre.objects.get(name='Test genre')
        assert added_genre is not None
        added_genre.delete()

    def test__genre_add_view__not_valid_form(self, client):
        response = client.post('/genre/add/', {})
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/genre_add.html')
        assert response.context['form'].__class__.__name__ == 'MovieGenreForm'

    def test__genre_add_view__exist(self, client):
        form = MovieGenreForm(data={
            'name': 'Комедия',
        })
        response = client.post('/genre/add/', form.data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/genre_add.html')
        assert response.context['form'].errors == {
            'name': ['Жанр с таким Название жанра уже существует.']
            }

    def test__genre_add_view__has_not_required_fields(self, client):
        form = MovieGenreForm(data={
            'description': 'Test description'
        })
        response = client.post('/genre/add/', form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            'name': ['Обязательное поле.'],
            }

    def test__genre_add_view__not_allowed(self, client):
        response = client.delete('/genre/add/')
        assert response.status_code == 405
