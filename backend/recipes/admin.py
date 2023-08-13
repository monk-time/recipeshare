from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (RecipeInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name',)
    search_help_text = 'Поиск по имени ингредиента'


class RecipeIngredientInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not any(self.errors) and not any(
            obj and not obj['DELETE'] for obj in self.cleaned_data
        ):
            raise ValidationError('Укажите хотя бы один ингредиент')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    formset = RecipeIngredientInlineFormset
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'favorite_count',
        'list_ingredients',
    )
    list_editable = ('name',)
    list_filter = ('tags',)
    search_fields = ('author__username', 'name')
    search_help_text = 'Поиск по юзернейму автора или имени рецепта'
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('favorite_count', 'list_ingredients')

    @admin.display(description='Добавления в избранное')
    def favorite_count(self, recipe):
        return recipe.favorited_by.count()

    @admin.display(description='Ингредиенты')
    def list_ingredients(self, recipe):
        names = recipe.ingredients.values_list('name', flat=True)
        return '; '.join(names)
