from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CustomGetViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Спец вьюсет для получения экземпляров."""
    pass


class BaseGetAddRemoveMixin:
    """Базовый миксин для получения, добавления и удаления элементов."""

    def get_user_items(self, user, model_class):
        items = model_class.objects.filter(user=user)
        return items

    @staticmethod
    def add_or_remove(
            request, pk, model_class, serializer_class
    ):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'DELETE':
            del_count, _ = model_class.objects.filter(
                user=request.user, recipe=recipe
            ).delete()

            if del_count > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'detail': f'{recipe} не найдено для удаления.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        existing_favorite = model_class.objects.filter(
            user=request.user, recipe=recipe).first()
        if existing_favorite is not None:
            return Response(
                {'detail': f'{recipe} уже добавлено.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializer_class(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        action_serializer = serializer_class(instance)
        return Response(
            action_serializer.data, status=status.HTTP_201_CREATED
        )
