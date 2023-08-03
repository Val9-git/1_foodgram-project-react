from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
# class UserAdmin(UserAdmin):
class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'first_name', 'last_name')
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_filter = ['username', 'email']


@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('id', 'user', 'author')
