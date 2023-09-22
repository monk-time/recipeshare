from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

from .validators import HEXColorValidator


class Tag(models.Model):
    """Модель тегов рецептов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_LENGTH_TAG_NAME,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=settings.MAX_LENGTH_TAG_COLOR,
        unique=True,
        validators=[HEXColorValidator()],
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=settings.MAX_LENGTH_TAG_SLUG,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов для рецептов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_LENGTH_INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.MAX_LENGTH_INGREDIENT_UNIT,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_LENGTH_RECIPE_NAME,
    )
    text = models.TextField('Описание')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=settings.UPLOAD_URL,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        related_name='recipes',
    )
    favorited_by = models.ManyToManyField(
        User,
        verbose_name='В избранном у пользователей',
        related_name='favorited',
        db_table='recipes_favorited',
        blank=True,
    )
    in_shopping_cart = models.ManyToManyField(
        User,
        verbose_name='В корзине у пользователей',
        related_name='shopping_cart',
        db_table='recipes_shopping_cart',
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ('ingredient',)
        verbose_name = 'Ингредиент к рецепту'
        verbose_name_plural = 'Ингредиенты к рецептам'
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe_ingredient',
                fields=['recipe', 'ingredient'],
            ),
        ]

    def __str__(self):
        return (
            f'{self.recipe.name}: {self.ingredient.name} - '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )
