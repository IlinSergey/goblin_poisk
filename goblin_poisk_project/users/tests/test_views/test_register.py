import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestRegisterView:
    def test__register_view__success_get(self, client):
        response = client.get('/user/register/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')

    def test__register_view__success_post(self, client):
        response = client.post('/user/register/', {
            'username': 'test_user',
            'first_name': 'test_name',
            'email': 'test@test.com',
            'password': 'test_password',
            'password2': 'test_password',
            })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register_done.html')
        created_user = User.objects.get(username='test_user')
        assert created_user is not None
        assert created_user.check_password('test_password')
        assert created_user.first_name == 'test_name'
        created_user.delete()

    def test__register_view__different_passwords(self, client):
        response = client.post('/user/register/', {
            'username': 'test_user',
            'first_name': 'test_name',
            'email': 'test@test.com',
            'password': 'test_password',
            'password2': 'test_password2',
            })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {'password2': ['Пароли не совпадают']}

    def test__register_view__ot_valid_email(self, client):
        response = client.post('/user/register/', {
            'username': 'test_user',
            'first_name': 'test_name',
            'email': 'testtestcom',
            'password': 'test_password',
            'password2': 'test_password',
            })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'email': ['Введите правильный адрес электронной почты.']
            }

    def test__register_view__username_exists(self, client, user):
        response = client.post('/user/register/', {
            'username': 'test_user',
            'first_name': 'test_name',
            'email': 'test@test.com',
            'password': 'test_password',
            'password2': 'test_password',
            })
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'username': ['Пользователь с таким именем уже существует.']
            }

    def test__register_view__empty_form(self, client):
        response = client.post('/user/register/', {})
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')
        assert response.context['form'].errors == {
            'username': ['Обязательное поле.'],
            'password': ['Обязательное поле.'],
            'password2': ['Обязательное поле.'],
            }
