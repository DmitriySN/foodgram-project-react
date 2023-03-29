from django.contrib import admin

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    TagRecipe,
)
from users.models import Subscribe


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


class TagInline(admin.TabularInline):
    model = TagRecipe
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"
    list_filter = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"
    list_filter = ("name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "id",
    )
    search_fields = ("user",)
    empty_value_display = "-пусто-"
    list_filter = ("user",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user",)
    empty_value_display = "-пусто-"
    list_filter = ("user",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientInline,
        TagInline,
    )
    list_display = (
        "name",
        "author",
        "cooking_time",
        "id",
        "count_favorite",
        "pub_date",
    )
    search_fields = (
        "name",
        "author",
        "tags",
    )
    empty_value_display = "-пусто-"
    list_filter = (
        "name",
        "author",
        "tags",
    )

    def count_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    count_favorite.short_description = "Кол-во в избранном"


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    search_fields = ("user",)
    empty_value_display = "-пусто-"
    list_filter = ("user",)
