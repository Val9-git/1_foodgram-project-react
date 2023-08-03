from django.contrib import admin

from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель ярлыков в админпанели."""
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель ингредиентов в админпанели."""
    search_fields = ('name',)
    list_display = ('id', 'name', 'measurement_unit')


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель рецептов в админпанели."""
    list_display = ('id', 'name', 'author', 'text', 'added_to_favorites',)
    list_filter = ['name', 'author', 'tags']
    inlines = (IngredientsInline,)
    readonly_fields = ("added_to_favorites",)

    @staticmethod
    def added_to_favorites(obj):
        return obj.favorites.count()


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    """Модель избранных рецептов в админпанели."""
    list_display = ('id', 'recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель списка покупок в админпанели."""
    list_display = ('id', 'recipe', 'user')
