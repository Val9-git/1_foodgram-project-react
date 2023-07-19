from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Спец класс разделения на страницы."""
    page_size_query_param = "limit"
