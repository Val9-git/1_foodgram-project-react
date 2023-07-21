# import base64

# from django.core.files.base import ContentFile
# from django.db.models import F
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# from rest_framework.serializers import PrimaryKeyRelatedField

from recipes.models import (
                            # AmountIngredient, FavoriteRecipe, Ingredient,
                            # Recipe, ShoppingCart,
                            Tag
                            )
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Спец сериализатор Пользователя. """
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class SubscriptionSerializer(CustomUserSerializer):
    """Сериализатор подписок."""
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes_count",
        )

    # def get_recipes(self, obj):
    #     request = self.context.get("request")
    #     recipes_limit = request.GET.get("recipes_limit")
    #     recipes = obj.recipe_posts.all()
    #     if recipes_limit:
    #         recipes = recipes[: int(recipes_limit)]
    #     serializer = ShortRecipeSerializer(recipes, many=True)
    #     return serializer.data

    def validate(self, data):
        request = self.context.get("request")
        author = self.instance
        check_exist_sibscribe = Subscription.objects.filter(
            user=request.user, author=author
        ).exists()
        if request.method == "DELETE":
            if not check_exist_sibscribe:
                raise ValidationError("Подписки не было")
        else:
            if check_exist_sibscribe:
                raise ValidationError("Повторая подписка")
            if author == request.user:
                raise ValidationError("Подписка на себя")
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
