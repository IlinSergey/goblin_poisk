import pytest
from pytest_django.asserts import assertTemplateUsed

from movies.forms import MovieForm
from movies.models import Movie


@pytest.mark.django_db
class TestMovieEditView:

    def test__movie_edit_view__success(self, client):
        response = client.get('/bolshoj-lebovski/edit/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_edit.html')
        assert response.context['form'].__class__.__name__ == 'MovieForm'
        assert response.context['movie'].title == 'Большой Лебовски'
        response.context['movie'].title = 'Test title'
        udpated_data = {
            'title': 'Test title',
            'release_year': response.context['movie'].release_year,
            'director': response.context['movie'].director.id,
            'description': response.context['movie'].description,
            'length': response.context['movie'].length,
            'genres': response.context['movie'].genres.all().values_list('id', flat=True),
            'original_rating': response.context['movie'].original_rating,
            'poster': response.context['movie'].poster
        }
        form = MovieForm(data=udpated_data)
        assert form.is_valid()
        response = client.post('/bolshoj-lebovski/edit/', form.data)
        assert response.status_code == 302
        updated_movie = Movie.objects.get(title='Test title')
        assert updated_movie is not None
        updated_movie.title = 'Большой Лебовски'
        updated_movie.save()

    def test__movie_edit_view__not_valid_form(self, client):
        response = client.post('/bolshoj-lebovski/edit/', {})
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_edit.html')
        assert response.context['form'].__class__.__name__ == 'MovieForm'
        assert response.context['movie'].title == 'Большой Лебовски'

    def test__movie_edit_view__not_found(self, client):
        response = client.get('/bolshoj-lebovski_2/edit/')
        assert response.status_code == 404

    def test__movie_edit_view__not_allowed(self, client):
        response = client.delete('/bolshoj-lebovski/edit/')
        assert response.status_code == 405
