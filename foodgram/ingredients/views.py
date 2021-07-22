from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import mixins

from .filters import IngredientFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
