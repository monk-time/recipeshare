from http import HTTPStatus
import pytest


@pytest.mark.django_db(transaction=True)
class TestUsers:
    url_create_token = '/api/auth/token/login/'
    url_delete_token = '/api/auth/token/logout/'
    url_create_user = '/api/users/'

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
            f'POST-запрос на `{url}` авторизованного пользователя '
            'должен возвращать статус 204.'
        )
        response = client.post(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'POST-запрос на `{url}` анонимного пользователя '
            'должен возвращать статус 401.'
        )

    def test_create_user_no_data(self, client):
        url = self.url_create_user
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
        'invalid_data, invalid_fields',
        (
            (
                {
                    'email': 'invalid_email',
                    'username': ' ',
                    'password': '1234567',
                    'first_name': 'John',
                    'last_name': 'Smith',
                },
                ('email', 'username'),
            ),
            (
                {
                    'email': 'valid_email@test.com',
                    'username': ' ',
                    'password': '1234567',
                    'first_name': 'John',
                    'last_name': 'Smith',
                },
                ('username',),
            ),
            (
                {
                    'email': 'valid_email@test.com',
                    'username': 'valid_username',
                    'password': '1234567',
                },
                ('first_name', 'last_name'),
            ),
        ),
    )
    def test_create_user_invalid_data(
        self, invalid_data, invalid_fields, client, django_user_model
    ):
        url = self.url_create_user
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
        url = self.url_create_user
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
