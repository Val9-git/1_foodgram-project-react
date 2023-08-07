from django.db import IntegrityError
from django.shortcuts import get_object_or_404
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

    def add_or_remove(self, request, pk, model_class, serializer_class):
        instance = get_object_or_404(model_class, pk=pk)

        if request.method == 'DELETE':
            deleted_count, _ = model_class.objects.filter(
                user=request.user, recipe=instance
            ).delete()

            if deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'detail': f'{instance} не найдено для удаления.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        try:
            model_class.objects.get(user=request.user, recipe=instance)
        except model_class.DoesNotExist:
            try:
                model_class.objects.create(user=request.user, recipe=instance)
            except IntegrityError:
                return Response(
                    {'detail': f'{instance} уже добавлено.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = serializer_class(
                data={'user': request.user.id, 'recipe': instance.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            action_serializer = serializer_class(instance)
            return Response(
                action_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_200_OK)
