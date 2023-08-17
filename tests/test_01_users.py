from http import HTTPStatus
import pytest


@pytest.mark.django_db(transaction=True)
class TestUsers:
    url_create_token = '/api/auth/token/login/'
    url_delete_token = '/api/auth/token/logout/'

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
            f'POST-запрос на {url} залогиненного пользователя '
            'должен возвращать статус 204.'
        )
        response = client.post(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f'POST-запрос на {url} анонимного пользователя '
            'должен возвращать статус 401.'
        )
