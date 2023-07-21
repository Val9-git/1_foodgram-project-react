# from django_filters import rest_framework
# from rest_framework.filters import SearchFilter


# class IngredientFilter(SearchFilter):
#     search_param = "name"


# class RecipeFilter(rest_framework.FilterSet):
#     is_favorited = rest_framework.BooleanFilter(method="filter_is_favorited")
#     tags = rest_framework.AllValuesMultipleFilter(field_name="tags__slug")

#     def filter_is_favorited(self, queryset, name, value):
#         if value and self.request.user.is_authenticated:
#             return queryset.filter(favoriterecipe__user=self.request.user)
#         return queryset
