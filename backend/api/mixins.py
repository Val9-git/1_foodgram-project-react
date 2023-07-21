from rest_framework import mixins, viewsets


class CustomGetViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Спец вьюсет для получения экземпляров."""
    pass
