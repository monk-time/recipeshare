from http import HTTPStatus
import pytest

from tests.utils import (
    check_pagination,
    check_user_fields,
    invalid_data_for_user,
)


@pytest.mark.django_db(transaction=True)
class TestUsers:
    url_create_token = '/api/auth/token/login/'
    url_delete_token = '/api/auth/token/logout/'
    url_users = '/api/users/'
    url_user = '/api/users/{id}/'
    url_user_me = '/api/users/me/'
    url_reset_password = '/api/users/set_password/'

    def test_create_auth_token_with_valid_data(self, client, user, user_token):
        url = self.url_create_token
        valid_data = {
            'email': user.email,
            'password': '1234567',
        }
        response = client.post(url, data=valid_data)
        assert response.status_code == HTTPStatus.OK, (
            f'POST-запрос на `{url}` с корректными данными должен '
            'возвращать статус 200.'
        )

        field = 'auth_token'
        assert field in response.json(), (
            f'Ответ на POST-запрос на `{url}` с корректными '
            f'данными должен содержать поле `{field}` с токеном.'
        )

        assert response.json()[field] == user_token[field], (
            f'Ответ на POST-запрос на `{url}` с корректными '
            f'данными должен содержать в поле `{field}` корректный токен.'
        )

    def test_create_auth_token_with_invalid_data(self, client, user):
        url = self.url_create_token
        invalid_data = (
            {'username': 'invalid_username', 'password': 'invalid pwd'},
            {'email': user.email, 'password': 'invalid pwd'},
            {'username': user.username, 'password': '1234567'},
        )
        for data in invalid_data:
            response = client.post(url, data=data)
            assert response.status_code == HTTPStatus.BAD_REQUEST, (
                f'POST-запрос с некорректными данными на `{url} `'
                'должен возвращать статус 400.'
            )

    def test_delete_auth_token(self, user_client, client):
        url = self.url_delete_token
        response = user_client.post(url)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос на `{url}` от авторизованного пользователя '
            'должен возвращать статус 204.'
        )
        response = client.post(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'POST-запрос на `{url}` от анонимного пользователя '
            'должен возвращать статус 401.'
        )

    def test_create_user_no_data(self, client):
        url = self.url_users
        response = client.post(url)
        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), f'Эндпоинт `{url}` не найден.'
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос на `{url}` без необходимых данных '
            'должен возвращать ответ со статусом 400.'
        )
        response_json = response.json()
        empty_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        for field in empty_fields:
            assert field in response_json and isinstance(
                response_json[field], list
            ), (
                f'Ответ на POST-запрос к `{url}` без необходимых данных '
                'должен возвращать информацию об обязательных полях.'
            )
        for field in response_json:
            assert field in empty_fields, (
                f'POST-запрос к `{url}` без необходимых данных'
                'не должен требовать лишние поля.'
            )

    @pytest.mark.parametrize(
        'invalid_data, invalid_fields', invalid_data_for_user
    )
    def test_create_user_invalid_data(
        self, invalid_data, invalid_fields, client, django_user_model
    ):
        url = self.url_users
        users_count = django_user_model.objects.count()
        response = client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос на `{url}` с некорректными данными '
            'должен возвращать статус 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'POST-запрос на `{url}` с некорректными данными '
            'не должен создавать нового пользователя.'
        )

        response_json = response.json()
        for field in invalid_fields:
            assert field in response_json and isinstance(
                response_json[field], list
            ), (
                f'POST-запрос на `{url}` с некорректными данными '
                'должен возвращать информацию о некорректных полях.'
            )

    @pytest.mark.parametrize(
        'duplicate_data, duplicate_fields',
        (
            ({'email': 'valid_email@test.com'}, ('username',)),
            ({'username': 'valid_username'}, ('email',)),
        ),
    )
    def test_create_user_duplicate_data(
        self, duplicate_data, duplicate_fields, client, django_user_model, user
    ):
        url = self.url_users
        keys = ['username', 'email', 'first_name', 'last_name', 'password']
        invalid_data = {
            key: getattr(user, key) for key in keys
        } | duplicate_data
        users_count = django_user_model.objects.count()
        response = client.post(url, data=invalid_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'POST-запрос на `{url}` с некорректными данными '
            'должен возвращать статус 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'POST-запрос на `{url}` с некорректными данными '
            'не должен создавать нового пользователя.'
        )

        response_json = response.json()
        for field in duplicate_fields:
            assert field in response_json and isinstance(
                response_json[field], list
            ), (
                f'POST-запрос на `{url}` с некорректными данными '
                'должен возвращать информацию о некорректных полях.'
            )

    def test_create_user_valid_data(self, client, django_user_model):
        url = self.url_users
        valid_data = {
            'email': 'valid_email@test.com',
            'username': 'valid_username',
            'password': 'valid_password',
            'first_name': 'John',
            'last_name': 'Smith',
        }
        users_count = django_user_model.objects.count()
        response = client.post(url, data=valid_data)

        assert response.status_code == HTTPStatus.CREATED, (
            f'POST-запрос на `{url}` с корректными данными '
            'должен возвращать статус 201.'
        )
        new_users_count = django_user_model.objects.count()
        valid_data.pop('password')
        new_user = django_user_model.objects.filter(**valid_data)
        assert new_users_count == users_count + 1 and new_user.exists(), (
            f'POST-запрос на `{url}` с корректными данными '
            'должен создавать нового пользователя.'
        )

        response_data = response.json()
        assert 'id' in response_data, (
            f'Ответ на POST-запрос на `{url}` с корректными данными '
            'должен содержать ключ `id`.'
        )
        response_data.pop('id')
        assert valid_data == response_data, (
            f'Ответ на POST-запрос на `{url}` с корректными данными '
            'содержит некорректные данные.'
        )

    @pytest.mark.parametrize(
        'client_fixture, msg',
        (
            ('client', 'от анонимного пользователя'),
            ('user_client', 'от зарегистрированного пользователя'),
        ),
    )
    def test_read_users(self, client_fixture, msg, request, user, user_2):
        url = self.url_users
        client = request.getfixturevalue(client_fixture)
        response = client.get(url)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'GET-запрос на `{url}` {msg} должен возвращать статус 200.'

        response_data = response.json()
        check_pagination(url, response_data, 2)
        for data_user in response_data['results']:
            check_user_fields(data_user, url, msg)

    def test_read_user(
        self,
        client,
        user_client,
        user,
        user_2,
        superuser,
        follow_user_to_user_2,
    ):
        url = self.url_user.format(id=user_2.id)
        response = client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'GET-запрос на `{url}` от анонимного пользователя '
            'должен возвращать статус 401.'
        )

        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос на `{url}` от зарегистрированного пользователя '
            'должен возвращать статус 200.'
        )

        response_data = response.json()
        check_user_fields(
            response_data, url, 'от зарегистрированного пользователя'
        )
        assert response_data['is_subscribed'] is True, (
            f'Ответ на GET-запрос на `{url}` от подписанного пользователя '
            'должен содержать поле `is_subscribed` со значением `True`'
        )

        url = f'{self.url_users}{superuser.id}/'
        response = user_client.get(url)
        response_data = response.json()
        assert response_data['is_subscribed'] is False, (
            f'Ответ на GET-запрос на `{url}` от неподписанного пользователя '
            'должен содержать поле `is_subscribed` со значением `False`'
        )

    def test_read_me(self, user_client, user):
        url = f'{self.url_user_me}'
        response = user_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            f'GET-запрос на `{url}` от зарегистрированного пользователя '
            'должен возвращать статус 200.'
        )

    def test_reset_password(self, user_client):
        url = self.url_reset_password
        data = {
            'new_password': 'new_valid_password',
            'current_password': '1234567',
        }
        response = user_client.post(url, data=data)
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            f'POST-запрос на `{url}` от зарегистрированного пользователя '
            'должен возвращать статус 204.'
        )
