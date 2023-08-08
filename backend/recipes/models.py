from django.db import models

from .validators import HEXColorValidator

MAX_LENGTH_TAG_NAME = 200
MAX_LENGTH_TAG_COLOR = 7
MAX_LENGTH_TAG_SLUG = 200
MAX_LENGTH_INGREDIENT_NAME = 200
MAX_LENGTH_INGREDIENT_UNIT = 200


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_TAG_NAME,
        unique=True,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=MAX_LENGTH_TAG_COLOR,
        unique=True,
        validators=[HEXColorValidator()],
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=MAX_LENGTH_TAG_SLUG,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGTH_INGREDIENT_UNIT,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
