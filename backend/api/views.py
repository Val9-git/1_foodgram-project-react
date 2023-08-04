from api.filters import IngredientFilter, RecipeFilter
from api.mixins import CustomGetViewSet
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from django.db.models import BooleanField, Case, Count, Sum, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Favorites, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)


class BaseGetAddRemoveMixin:
    """Базовый миксин для получения, добавления и удаления элементов."""
    def get_user_items(self, user, model_class):
        items = model_class.objects.filter(user=user)
        return items

    def perform_add_item(self, user, instance, model_class):
        try:
            model_class.objects.get(user=user, recipe=instance)
        except model_class.DoesNotExist:
            model_class.objects.create(user=user, recipe=instance)
            return True
        return False

    def perform_remove_item(self, user, instance, model_class):
        try:
            model_class.objects.get(user=user, recipe=instance).delete()
            return True
        except model_class.DoesNotExist:
            return False


class UsersViewSet(DjoserUserViewSet, BaseGetAddRemoveMixin):
    """Вьюсет для пользователей и подписок."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ('username',)
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        request_user = self.request.user
        queryset = super().get_queryset()
        if request_user.is_authenticated:
            queryset = (
                super()
                .get_queryset()
                .annotate(
                    is_subscribed=Case(
                        When(
                            subscribing__user=request_user,
                            then=True,
                        ),
                        default=False,
                        output_field=BooleanField(),
                    )
                )
            )
        return queryset

    @action(
        detail=False,
        methods=('get', 'post'),
    )
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscribing__user=request.user
        ).annotate(recipes_count=Count('recipes'))
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        author.recipes_count = author.recipes.count()
        serializer = SubscriptionSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            Subscription.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Subscription.objects.filter(author=author, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(CustomGetViewSet):
    """Вьюсет для ярлыков."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(CustomGetViewSet):
    """Вьюсет для ингредиентов."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet, BaseGetAddRemoveMixin):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(
            IsAuthenticated,
            IsAuthorOrReadOnly,
        ),
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        is_added = self.perform_add_item(request.user, recipe, Favorites)

        if request.method == 'POST':
            if is_added:
                serializer = ShortRecipeSerializer(
                    recipe, context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(
                {'errors': 'Рецепт уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_added:
            self.perform_remove_item(request.user, recipe, Favorites)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Рецепта нет в избранном'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(
            IsAuthenticated,
            IsAuthorOrReadOnly,
        ),
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        is_added = self.perform_add_item(request.user, recipe, ShoppingCart)

        if request.method == 'POST':
            if is_added:
                serializer = ShortRecipeSerializer(
                    recipe, context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(
                {'errors': 'Рецепт уже в корзине'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_added:
            self.perform_remove_item(request.user, recipe, ShoppingCart)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Рецепта нет в корзине'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['get'], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename = shopping_list.txt'
        ingreds = IngredientAmount.objects.filter(
            recipe__shoppingcart__user=request.user
        ).order_by('ingredients__name').values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))
        for item in ingreds:
            name = item['ingredients__name']
            measurement_unit = item['ingredients__measurement_unit']
            amount = item['sum_amount']
            response.write(f'{name} ({measurement_unit}) - {amount}\n')
        return response
