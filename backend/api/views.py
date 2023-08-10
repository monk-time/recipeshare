from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from recipes.models import Ingredient, Recipe, Tag

from .filters import IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
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
    serializer_class = RecipeReadSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

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
