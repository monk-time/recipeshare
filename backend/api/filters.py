from django.db.models import Case, Value, When
from django_filters import rest_framework as filters

from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(method='name_startswith_or_anywhere')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def name_startswith_or_anywhere(self, queryset, name, value):
        queryset = (
            queryset.filter(name__icontains=value)
            .annotate(
                match_ordering=Case(
                    When(name__istartswith=value, then=Value(1)),
                    default=Value(0),
                )
            )
            .order_by('-match_ordering', 'name')
        )
        print(queryset.query)
        return queryset
