import pytest
from rest_framework.authtoken.models import Token


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='admin', email='admin@gmail.com', password='admin'
    )

@pytest.fixture
def test_user(django_user_model):
    return django_user_model.objects.create(
        username='dangerousmonk',
        email='dangerousmonk@gmail.com',
        password='test12345',
        first_name='Oleg',
        last_name='Avilov'
    )

@pytest.fixture
def admin_client(admin):
    from rest_framework.test import APIClient
    client = APIClient()
    token, created = Token.objects.get_or_create(user=admin)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture
def user_client(test_user):
    from rest_framework.test import APIClient
    client = APIClient()
    token, created = Token.objects.get_or_create(user=test_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client
