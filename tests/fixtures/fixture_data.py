import pytest

from recipes.models import Ingredient, Tag


@pytest.fixture
def ingredient_1():
    return Ingredient.objects.create(
        name='Ингредиент 1',
        measurement_unit='г',
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='Ингредиент 2',
        measurement_unit='г',
    )


@pytest.fixture
def ingredients_for_search():
    names = (
        'масло подсолнечное',
        'сливочное масло',
        'масло авокадо',
        'льняное масло',
    )
    return Ingredient.objects.bulk_create(
        Ingredient(
            name=name,
            measurement_unit='г',
        )
        for name in names
    )


@pytest.fixture
def tag_1():
    return Tag.objects.create(
        name='Тег 1',
        color='#111111',
        slug='tag1',
    )


@pytest.fixture
def tag_2():
    return Tag.objects.create(
        name='Тег 2',
        color='#222222',
        slug='tag2',
    )
