import pytest
from pytest_django.asserts import assertTemplateUsed

from movies.forms import DirectorForm
from movies.models import Director


@pytest.mark.django_db
class TestDirectorAddView:

    def test__director_add_view__success_get(self, client):
        response = client.get('/director/add/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/director_add.html')
        assert response.context['form'].__class__.__name__ == 'DirectorForm'

    def test__director_add_view__success_post(self, client):
        form = DirectorForm(data={
            'name': 'Test director',
            'description': 'Test description'
        })
        assert form.is_valid()
        response = client.post('/director/add/', form.data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/success_added_director_or_genre.html')
        added_director = Director.objects.get(name='Test director')
        assert added_director is not None
        added_director.delete()

    def test__director_add_view__not_valid_form(self, client):
        response = client.post('/director/add/', {})
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/director_add.html')
        assert response.context['form'].__class__.__name__ == 'DirectorForm'

    def test__director_add_view__exist(self, client):
        form = DirectorForm(data={
            'name': 'Саймон Уэст',
            'description': 'Test description'
        })
        response = client.post('/director/add/', form.data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/director_add.html')
        assert response.context['form'].errors == {'name': ['Режиссер с таким Имя уже существует.']}

    def test__director_add_view__has_not_required_fields(self, client):
        form = DirectorForm(data={
            'description': 'Test description'
        })
        response = client.post('/director/add/', form.data)
        assert response.status_code == 200
        assert response.context['form'].errors == {
            'name': ['Обязательное поле.'],
            }

    def test__director_add_view__not_allowed(self, client):
        response = client.delete('/director/add/')
        assert response.status_code == 405
