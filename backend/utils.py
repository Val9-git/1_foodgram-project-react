# file utils.py
import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response


class Base64ImageField(serializers.ImageField):
    """Сериализатор изображений."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class BaseGetAddRemoveMixin:
    """Базовый миксин для получения, добавления и удаления элементов."""

    def get_user_items(self, user, model_class):
        items = model_class.objects.filter(user=user)
        return items

    def add_or_remove(self, request, pk, model_class, serializer_class):
        from api.serializers import ShortRecipeSerializer
        instance = get_object_or_404(model_class, pk=pk)

        if request.method == 'DELETE':
            deleted, _ = model_class.objects.filter(
                user=request.user, recipe=instance
            ).delete()
            if deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            model_class.objects.get(user=request.user, recipe=instance)
        except model_class.DoesNotExist:
            model_class.objects.create(user=request.user, recipe=instance)
            serializer = serializer_class(
                data={'user': request.user.id, 'recipe': instance.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            action_serializer = ShortRecipeSerializer(instance)
            return Response(
                action_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_200_OK)
