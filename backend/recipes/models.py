from django.core.validators import MinValueValidator
from django.db import models
from foodgram.settings import PROJECT_CONSTANTS
from users.models import User


class Tag(models.Model):
    """Ярлыки, задаётся админом."""
    name = models.CharField(
        max_length=PROJECT_CONSTANTS["LENGTH_TAG_NAME"],
        unique=True,
        verbose_name='Имя ярлыка',
    )
    color = models.CharField(
        max_length=PROJECT_CONSTANTS["LENGTH_HEX_COLOR"],
        unique=True,
        verbose_name='Цвет (HEX code)',
        default='#18c4e8',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Ярлык')

    class Meta:
        verbose_name = 'Ярлык'
        verbose_name_plural = 'Ярлыки'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """Ингредиенты, задаётся админом."""
    name = models.CharField(
        blank=False,
        max_length=PROJECT_CONSTANTS["LENGTH_INGRIDIENT_NAME"],
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        blank=False,
        max_length=PROJECT_CONSTANTS["LENGTH_MEASUREMENT_UNIT"],
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Рецепты."""
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=PROJECT_CONSTANTS["LENGTH_RECIPE_NAME"],
        unique=True,
        help_text='Ввод названия рецепта',
    )
    text = models.TextField(
        verbose_name='Шаги рецепта',
        help_text='Ввод текста рецепта'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientAmount'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Ярлыки',
        related_name='recipes'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='recipes/images/',
        blank=True
    )

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(1)],
    )

    # def ingredients_names(self):
    #     return " %s" % (
    #         ", ".join(
    #             [ingredient.name for ingredient in self.ingredients.all()]
    #         )
    #     )

    # ingredients_names.short_description = "Ингредиенты"

    # def tags_slug(self):
    #     return " %s" % (", ".join([tag.slug for tag in self.tags.all()]))

    # tags_slug.short_description = "Теги"

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Количество ингредиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        related_name='ingridient_amount',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='ingredient_amount',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe',)

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredients}"


class UserRecipe(models.Model):
    """Абстрактная модель для базового класса."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True


class Favorites(UserRecipe):
    """Избранные рецепты."""
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorite_user_recipe'
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingCart(UserRecipe):
    """Список покупок."""
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
