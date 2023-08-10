from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Ingredient, Recipe, Tag

from .filters import IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeMiniSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.query_params  # type: ignore

        is_favorited = query_params.get('is_favorited')
        if is_favorited == '1':
            queryset = queryset.filter(favorited_by=self.request.user)

        is_in_shopping_cart = query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(in_shopping_cart=self.request.user)

        author = query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        tags = query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)

        return queryset

    @action(
        methods=['post'],
        detail=True,
        serializer_class=RecipeMiniSerializer,
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.in_shopping_cart.contains(user):
            raise ValidationError('Рецепт уже есть в списке покупок.')
        recipe.in_shopping_cart.add(user)
        serializer = self.serializer_class(recipe)  # type: ignore
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not recipe.in_shopping_cart.contains(user):
            raise ValidationError('Рецепт отсутствует в списке покупок.')
        recipe.in_shopping_cart.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post'],
        detail=True,
        serializer_class=RecipeMiniSerializer,
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if recipe.favorited_by.contains(user):
            raise ValidationError('Рецепт уже есть в избранном.')
        recipe.favorited_by.add(user)
        serializer = self.serializer_class(recipe)  # type: ignore
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not recipe.favorited_by.contains(user):
            raise ValidationError('Рецепт отсутствует в избранном.')
        recipe.favorited_by.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
