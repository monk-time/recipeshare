from http import HTTPStatus
import pytest

from recipes.models import Ingredient, Tag


@pytest.mark.django_db(transaction=True)
class TestTagsIngredients:
    url_tags = '/api/tags/'
    url_tag = '/api/tags/{id}/'
    url_ingredients = '/api/ingredients/'
    url_ingredient = '/api/ingredients/{id}/'
    url_ingredient_search = '/api/ingredients/?name={name}'

    def check_tag_info(self, tag_info: dict, url: str):
        for field in ('id', 'name', 'color', 'slug'):
            assert field in tag_info, (
                f'Ответ на GET-запрос к `{url}` должен содержать '
                f'информацию о теге с полем `{field}`.'
            )

    def check_ingredient_info(self, ingredient_info: dict, url: str):
        for field in ('id', 'name', 'measurement_unit'):
            assert field in ingredient_info, (
                f'Ответ на GET-запрос к `{url}` должен содержать '
                f'информацию об ингредиенте с полем `{field}`.'
            )

    def test_read_tags(self, client, tag_1, tag_2):
        url = self.url_tags
        response = client.get(url)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'GET-запрос на `{url}` должен возвращать статус 200.'
        data = response.json()
        assert isinstance(data, list), (
            f'GET-запрос к `{url}` должен возвращать информацию о тегах '
            'в виде списка.'
        )
        assert len(data) == Tag.objects.count(), (
            f'GET-запрос к `{url}` должен возвращать информацию '
            'о всех существующих тегах.'
        )
        for tag_info in data:
            self.check_tag_info(tag_info, url)

    def test_read_tag(self, client, tag_1):
        url = self.url_tag.format(id=tag_1.id)
        response = client.get(url)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'GET-запрос на `{url}` должен возвращать статус 200.'
        tag_info = response.json()
        assert isinstance(tag_info, dict), (
            f'GET-запрос к `{url}` должен возвращать информацию о теге '
            'в виде словаря.'
        )
        self.check_tag_info(tag_info, url)

    def test_read_ingredients(self, client, ingredient_1, ingredient_2):
        url = self.url_ingredients
        response = client.get(url)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'GET-запрос на `{url}` должен возвращать статус 200.'
        data = response.json()
        assert isinstance(data, list), (
            f'GET-запрос к `{url}` должен возвращать информацию о тегах '
            'в виде списка.'
        )
        assert len(data) == Ingredient.objects.count(), (
            f'GET-запрос к `{url}` должен возвращать информацию '
            'о всех существующих тегах.'
        )
        for ingredient_info in data:
            self.check_ingredient_info(ingredient_info, url)

    def test_read_ingredient(self, client, ingredient_1):
        url = self.url_ingredient.format(id=ingredient_1.id)
        response = client.get(url)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'GET-запрос на `{url}` должен возвращать статус 200.'
        ingredient_info = response.json()
        assert isinstance(ingredient_info, dict), (
            f'GET-запрос к `{url}` должен возвращать информацию о теге '
            'в виде словаря.'
        )
        self.check_ingredient_info(ingredient_info, url)

    def test_search_ingredients(self, client, ingredients_for_search):
        url = self.url_ingredient_search.format(name='масло')
        response = client.get(url)
        data = response.json()
        ingr_names = tuple(ingr['name'] for ingr in data)
        expected = (
            'масло авокадо',
            'масло подсолнечное',
            'льняное масло',
            'сливочное масло',
        )
        assert ingr_names == expected, (
            f'GET-запрос на `{url}` должен возвращать ингредиенты '
            'в корректном порядке.'
        )
