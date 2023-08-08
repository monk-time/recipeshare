import csv
import sys
from dataclasses import dataclass

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Follow, User

BASE_DIR = settings.DATA_ROOT


@dataclass
class CSVModel:
    filename: str
    model: Model

    def load(self):
        try:
            with open(BASE_DIR / self.filename, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.model.objects.bulk_create(  # type: ignore
                    self.model(**row) for row in reader  # type: ignore
                )
        except FileNotFoundError:
            raise CommandError(f'File {self.filename} not found')


CSV_MODELS = (
    CSVModel(filename='users.csv', model=User),  # type: ignore
    CSVModel(filename='follow.csv', model=Follow),  # type: ignore
    CSVModel(filename='tags.csv', model=Tag),  # type: ignore
    CSVModel(filename='ingredients.csv', model=Ingredient),  # type: ignore
    CSVModel(filename='recipes.csv', model=Recipe),  # type: ignore
    CSVModel(
        filename='recipe_ingredient.csv',
        model=RecipeIngredient,  # type: ignore
    ),
    CSVModel(
        filename='recipe_tag.csv',
        model=Recipe.tags.through,
    ),
    CSVModel(
        filename='recipe_favorited.csv',
        model=Recipe.favorited_by.through,
    ),
    CSVModel(
        filename='recipe_shopping_cart.csv',
        model=Recipe.in_shopping_cart.through,
    ),
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stdout.write(
            self.style.MIGRATE_HEADING('Loading into database:\n')
        )
        for csv_model in CSV_MODELS:
            sys.stdout.write(
                f'  Loading model {csv_model.model.__name__} '  # type: ignore
                f'from {csv_model.filename}...'
            )
            csv_model.load()
            sys.stdout.write(self.style.SUCCESS(' OK\n'))
