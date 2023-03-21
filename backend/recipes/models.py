from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Класс описывающий модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name="Ингредиент",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Класс описывающий модель тэга."""

    YELLOW = "ffff00"
    RED = "#ff0000"
    GREEN = "#008000"

    COLORS = [
        (YELLOW, "Завтрак"),
        (RED, "Обед"),
        (GREEN, "Ужин"),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название тэга",
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет",
        choices=COLORS,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name="Текстовый путь, slug",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Класс описывающий модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Изображение",
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                1, "Время приготовления не может быть менше минуты."
            ),
        ],
        verbose_name="Время приготовления в минутах.",
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagRecipe",
        verbose_name="Тэги",
        related_name="recipes",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    """Класс описывающий модель связи Рецепта с Тэгом."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="Тег",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "recipe"], name="unique_tagrecipe"
            )
        ]

    def __str__(self):
        return f"{self.tag} {self.recipe}"


class IngredientRecipe(models.Model):
    """Класс описывающий модель связи Ингредиентов в рецепте"""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredientrecipes",
        verbose_name="Ингредиент в рецепте",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredientrecipes",
        verbose_name="Рецепт",
    )
    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1, "Время приготовления не может быть менше минуты."
            ),
        ],
        verbose_name="Количество ингредиента",
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="unique_ingredientrecipe"
            )
        ]

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class Cart(models.Model):
    """Класс описывающий модель корзины для покупок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь",
        related_name="carts",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Рецепты",
    )

    class Meta:
        ordering = ("user",)
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_cart")
        ]

    def __str__(self):
        return f"{self.user} id - {self.user.pk}, {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ("user",)
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite")
        ]

    def __str__(self):
        return f"{self.user} id - {self.user.pk}, {self.recipe}"
