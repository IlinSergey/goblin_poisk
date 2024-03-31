import pytest
from pytest_django.asserts import assertTemplateUsed

from movies.models import Review


@pytest.mark.django_db
class TestReviewAddView:
    def test__review_add_view__success(self, client, user):
        data = {
            'text': 'Test review',
            }
        client.force_login(user)
        response = client.post('/gnev-chelovecheskij/review/add/', data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/review.html')
        added_review = Review.objects.get(text='Test review')
        assert added_review is not None
        added_review.delete()

    def test__review_add_view__not_valid_form(self, client, user):
        data = {}
        client.force_login(user)
        response = client.post('/gnev-chelovecheskij/review/add/', data)
        assert response.status_code == 200
        assertTemplateUsed(response, 'movies/review.html')

    def test__review_add_view__not_allowed(self, client):
        response = client.put('/gnev-chelovecheskij/review/add/')
        assert response.status_code == 405
