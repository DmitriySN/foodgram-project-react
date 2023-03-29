from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from recipes.models import Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_cart')

    def filter_favorite(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favoriterecipes__user=self.request.user)
        return queryset

    def filter_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
