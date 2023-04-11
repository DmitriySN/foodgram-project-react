from django.contrib.auth import get_user_model
from django_filters import rest_framework as django_filter
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(django_filter.FilterSet):
    tags = django_filter.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filter.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = django_filter.BooleanFilter(method='filter_favorite')
    is_in_shopping_cart = django_filter.BooleanFilter(
        method='filter_cart')

    def filter_favorite(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'tags', 'author')


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']
