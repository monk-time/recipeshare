from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


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
    list_filter = ('name',)
    search_fields = ('name',)


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
    list_display = ('pk', 'name', 'author', 'favorite_count')
    list_editable = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('favorite_count',)

    @admin.display(description='Добавления в избранное')
    def favorite_count(self, instance):
        return instance.favorited_by.count()
