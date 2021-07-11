from rest_framework import viewsets
from rest_framework import mixins

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