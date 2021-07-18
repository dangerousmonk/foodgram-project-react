from django_filters import rest_framework as filters
from django.db.models import Q, Count
from .models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id',lookup_expr='exact')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(
            Q(in_favourites__is_favorited=True) & Q(in_favourites__user=user)
        )
    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(
            Q(in_favourites__is_in_shopping_cart=True) & Q(in_favourites__user=user)
        )