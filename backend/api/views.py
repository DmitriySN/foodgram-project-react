from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag
)

from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import CreateUpdateRetrieveViewSet
from .paginators import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    SubscriptionsRecipeSerializer,
    TagSerializer,
)


class TagViewSet(CreateUpdateRetrieveViewSet):
    queryset = Tag.objects.all().order_by('slug')
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientSearchFilter


class RecipesViewSet(CreateUpdateRetrieveViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_to_favorites(request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_favorite(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    def add_to_favorites(self, user, pk):
        if Favorite.objects.filter(recipe__id=pk, user=user).exists():
            return Response(
                {'errors': 'Вы уже добавили этот рецепт'},
                status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, pk=pk)
        Favorite.objects.create(recipe=recipe, user=user)
        serializer = SubscriptionsRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_favorite(self, user, pk):
        fav_recipe = Favorite.objects.filter(user=user, recipe__id=pk)
        if not fav_recipe.exists():
            return Response(
                {'errors': 'Ошибка удаления'},
                status=status.HTTP_400_BAD_REQUEST)
        fav_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_to_shopping_cart(request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_from_cart(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    def add_to_shopping_cart(self, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = SubscriptionsRecipeSerializer(recipe)
        if Cart.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                data='Вы уже добавлили этот рецепт в корзину',
                status=status.HTTP_400_BAD_REQUEST)
        Cart.objects.create(recipe=recipe, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from_cart(self, user, pk):
        recipe = Cart.objects.filter(user=user, recipe__id=pk)
        if not recipe.exists():
            return Response(
                data='Ошибка удаления',
                status=status.HTTP_400_BAD_REQUEST)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredient_list = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount_total=Sum('amount'))
        to_buy = []
        for ingredient in ingredient_list:
            cart_str = (
                ingredient['ingredient__name'] + ' ('
                + ingredient['ingredient__measurement_unit'] + ') кол-во: '
                + str(ingredient['amount_total']) + '\n'
            )
            to_buy.append(cart_str)
        response = HttpResponse(content_type='text/plain')
        response["Content-Disposition"] = "attachment; filename=cart-list.txt"
        response.writelines(to_buy)
        return response
