import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestMovieSearchView():

    def test__movie_search_view__success_no_query(self, client):
        response = client.get('/movie/search/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/search.html')
        assert response.context['form']
        assert response.context['movies'] == []
        assert response.context['query'] == ''

    def test__movie_search_view__success(self, client):
        response = client.get('/movie/search/?query=Большой Лебовски')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/search.html')
        assert response.context['form']
        assert len(response.context['movies']) == 1
        assert response.context['query'] == 'Большой Лебовски'

    def test__movie_search_view__success_with_typo(self, client):
        response = client.get('/movie/search/?query=БАлшой Лебовски')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/search.html')
        assert response.context['form']
        assert len(response.context['movies']) == 1
        assert response.context['movies'][0].title == 'Большой Лебовски'
        assert response.context['query'] == 'БАлшой Лебовски'

    def test__movie_search_view__not_found(self, client):
        response = client.get('/movie/search/?query=Форсаж')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/search.html')
        assert response.context['form']
        assert len(response.context['movies']) == 0
        assert response.context['query'] == 'Форсаж'

    def test__movie_search_view__not_allowed_method(self, client):
        response = client.post('/movie/search/', {})
        assert response.status_code == 405
