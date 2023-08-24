import pytest
from rest_framework.test import APIClient

from users.models import Follow


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='test_super@test.com',
        username='TestSuperuser',
        password='1234567',
        first_name='Super',
        last_name='User',
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='test@test.com',
        username='TestUser',
        password='1234567',
        first_name='John',
        last_name='Smith',
    )


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(
        email='test2@test.com',
        username='TestUser2',
        password='1234567',
        first_name='Mary',
        last_name='Johnson',
    )


@pytest.fixture
def superuser_token(superuser):
    from djoser.conf import settings

    token_model = settings.TOKEN_MODEL  # type: ignore
    token, _ = token_model.objects.get_or_create(user=superuser)
    return {
        'auth_token': str(token),
    }


@pytest.fixture
def user_token(user):
    from djoser.conf import settings

    token_model = settings.TOKEN_MODEL  # type: ignore
    token, _ = token_model.objects.get_or_create(user=user)
    return {
        'auth_token': str(token),
    }


@pytest.fixture
def superuser_client(superuser_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {superuser_token["auth_token"]}'
    )
    return client


@pytest.fixture
def user_client(user_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {user_token["auth_token"]}',
    )
    return client


@pytest.fixture
def follow_user_to_user_2(user, user_2):
    return Follow.objects.create(follower=user, following=user_2)
