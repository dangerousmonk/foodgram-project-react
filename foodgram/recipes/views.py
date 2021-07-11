from rest_framework import viewsets

from .models import Tag, Recipe, IngredientAmount
from .serializers import TagSerializer,RecipeSerializer, IngredientAmountSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer