import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestMovieDetailView:

    @pytest.mark.parametrize('movie_slug', [
        'neuderzhimye-2',
        'gnev-chelovecheskij',
        'besslavnye-ubljudki',
        'dzhon-uik',
    ])
    def test__movie_detail_view__success(self, client, movie_slug):
        response = client.get(f'/{movie_slug}/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_detail.html')

    @pytest.mark.parametrize('movie_slug', [
        'neuderzhimye-3',
        'neuderzhimye-4',
    ])
    def test__movie_detail_view__not_found(self, client, movie_slug):
        response = client.get(f'/{movie_slug}/')
        assert response.status_code == 404

    def test__movie_detail_view__not_allowed(self, client):
        response = client.post('/dzhon-uik/')
        assert response.status_code == 405

    def test__movie_detail_view__not_allowed2(self, client):
        response = client.patch('/dzhon-uik/')
        assert response.status_code == 405
