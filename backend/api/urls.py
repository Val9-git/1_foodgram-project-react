from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UsersViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router_api_v1 = DefaultRouter()

router_api_v1.register('users', UsersViewSet, basename='users')
router_api_v1.register('recipes', RecipeViewSet, basename='recipes')
router_api_v1.register('tags', TagViewSet, basename='tags')
router_api_v1.register('ingredients', IngredientViewSet,
                       basename='ingredients')

urlpatterns = [
    path('', include(router_api_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
