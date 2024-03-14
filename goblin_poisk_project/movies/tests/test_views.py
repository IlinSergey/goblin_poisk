import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestMovieListView():

    def test__movie_list_view__success(self, client):
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_list.html')
        assert response.context['page_obj'].paginator.num_pages == 2
        assert len(response.context['movies'].paginator.object_list) == 7

    @pytest.mark.parametrize('genre_cat, count', [
        (1, 4),
        (2, 2),
        (3, 4),
        (4, 2),
        ])
    def test__movie_list_view__filter_by_genre(self, client, genre_cat, count):
        response = client.get(f'?genre={genre_cat}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/movie_list.html')
        assert response.context['page_obj'].paginator.num_pages == 1
        assert len(response.context['movies'].paginator.object_list) == count
