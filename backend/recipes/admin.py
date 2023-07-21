from django.contrib import admin

from .models import Tag, Ingredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag model in admin."""
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "measurement_unit")

# admin.site.register(Tag)
