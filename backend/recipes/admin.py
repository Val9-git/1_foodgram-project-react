from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag model in admin."""
    list_display = ('id', 'name', 'color', 'slug')


# admin.site.register(Tag)
