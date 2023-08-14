import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from api_users.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class UserFollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = int(request.query_params.get('recipes_limit', 0))
        queryset = obj.recipes.all()
        if recipes_limit > 0:
            queryset = queryset[:recipes_limit]
        serializer = RecipeMiniSerializer(queryset, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        many=True,
        read_only=True,
        source='recipeingredient_set',
    )
    image = serializers.URLField(source='image.url')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.favorited_by.contains(user)

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.in_shopping_cart.contains(user)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Укажите хотя бы один ингредиент.'
            )
        unique_ingredients = set(ingr['id'] for ingr in ingredients)
        if len(ingredients) != len(unique_ingredients):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        return ingredients

    def create_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )
            for ingredient_data in ingredients_data
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(recipe, ingredients_data)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        recipe = super().update(recipe, validated_data)
        if ingredients_data:
            recipe.ingredients.clear()
            self.create_ingredients(recipe, ingredients_data)
        if tags:
            recipe.tags.set(tags)
        recipe.save()
        return recipe

    def to_representation(self, instance):
        context = {'request': self.context['request']}
        return RecipeReadSerializer(instance, context=context).data
