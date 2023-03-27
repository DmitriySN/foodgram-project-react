from django.contrib.auth.hashers import make_password
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag
)
from rest_framework import serializers
from users.models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    email = serializers.EmailField
    username = serializers.CharField
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password', 'is_subscribed')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(CustomUserSerializer, self).create(validated_data)

    def get_is_subscribed(self, obj):
        user = User.objects.get(pk=1)
        return Subscribe.objects.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecapeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecapeSerializer(
        many=True,
        source='ingredientrecipes',
        read_only=True
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'text', 'image', 'ingredients',
            'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        )

    def set_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get(
                    'amount'))

    def create(self, validated_data):
        ingredients = self.initial_data.get('ingredients')
        tags_data = self.initial_data.get('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags_data)
        self.set_ingredients(ingredients, recipe)
        return recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return Cart.objects.filter(user=user, recipe=obj).exists()


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'recipes', 'recipes_count', 'is_subscribed'
        )

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        if 'recipes_limit' in self.context:
            recipes_limit = int(self.context['recipes_limit'])
            queryset = Recipe.objects.filter(author=obj)[:recipes_limit]
        return SubscriptionsRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.user, author=obj.author
        ).exists()
