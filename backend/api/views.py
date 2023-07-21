from django.db.models import (BooleanField, Case, Count, When,
                              #   Sum
                              )
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import (permissions, status,
                            #  viewsets
                            )
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (CustomUserSerializer, SubscriptionSerializer,
                          IngredientSerializer,
                          #   RecipeCreateSerializer, RecipeReadSerializer,
                          #   ShortRecipeSerializer,
                          TagSerializer
                          )
from api.filters import IngredientFilter
# ,RecipeFilter
from api.mixins import CustomGetViewSet
from api.permissions import (IsAdminOrReadOnly,
                             #   IsAuthorOrReadOnly
                             )
from recipes.models import (
                            # AmountIngredient, FavoriteRecipe,
                            # Recipe, ShoppingCart,
                            Tag, Ingredient
                             )
from users.models import Subscription, User


class UsersViewSet(DjoserUserViewSet):
    """Вьюсет для пользователей и подписок."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ("username",)
    permission_classes = (permissions.AllowAny,)
    # http_method_names = ['get', 'post', 'patch', 'delete']
    # lookup_field = 'username'

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
                            following__user=request_user,
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
        methods=("get", "post"),
    )
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            following__user=request.user
        ).annotate(recipes_count=Count("recipe_posts"))
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        author.recipes_count = author.recipe_posts.count()
        serializer = SubscriptionSerializer(
            author, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
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
    search_fields = ["^name"]
    pagination_class = None
