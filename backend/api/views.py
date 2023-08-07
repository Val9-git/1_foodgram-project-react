from api.filters import IngredientFilter, RecipeFilter
from api.mixins import CustomGetViewSet
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from django.db.models import BooleanField, Case, Count, Sum, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from mixins import BaseGetAddRemoveMixin
from recipes.models import (Favorites, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Subscription, User

from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeReadSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)


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
    def manage_subscriptions(self, request, pk):
        """Подписка/отписка от авторов."""
        return self.add_or_remove(
            request, pk, Subscription, SubscriptionSerializer
        )


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
    def manage_favorite(self, request, pk):
        """Добавление/удаление рецепта в избранное."""
        return self.add_or_remove(
            request, pk, Favorites, ShortRecipeSerializer
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(
            IsAuthenticated,
            IsAuthorOrReadOnly,
        ),
    )
    def manage_shopping_cart(self, request, pk):
        """Добавление/удаление рецепта в корзину покупок."""
        return self.add_or_remove(
            request, pk, ShoppingCart, ShortRecipeSerializer
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
