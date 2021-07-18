from django_filters import rest_framework as filters
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import csv

from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r

from django.http import HttpResponse

from .filters import RecipeFilter
from .models import Tag, Recipe, IngredientAmount, FavouriteRecipe
from .serializers import TagSerializer, RecipeReadSerializer, IngredientAmountSerializer, RecipeWriteSerializer
from foodgram.ingredients.models import Ingredient
from foodgram.permissions import IsOwnerOrReadOnly


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST', 'PATCH']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            obj, created = FavouriteRecipe.objects.update_or_create(
                user=user, recipe=recipe,
                defaults={'user': user, 'recipe': recipe, 'is_favorited': True})
            return Response({'status': 'Рецепт успешно добавлен в избранное'})
        else:
            fav_recipe = FavouriteRecipe.objects.get(recipe=recipe, user=user)
            if not fav_recipe.is_in_shopping_cart:
                fav_recipe.delete()
            else:
                fav_recipe.is_favorited = False
                fav_recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            obj, created = FavouriteRecipe.objects.update_or_create(
                user=user, recipe=recipe,
                defaults={'user': user, 'recipe': recipe, 'is_in_shopping_cart': True},
            )
            return Response({'status': 'Рецепт успешно добавлен в список покупок'})
        else:
            fav_recipe = FavouriteRecipe.objects.get(recipe=recipe, user=user)
            if not fav_recipe.is_favorited:
                fav_recipe.delete()
            else:
                fav_recipe.is_in_shopping_cart = False
                fav_recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get', 'delete'])
    def download_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipes = Recipe.objects.filter(in_favourites__user=user, in_favourites__is_in_shopping_cart=True)
        ingredients = recipes.values(
            'ingredients__name', 'ingredients__measurement_unit__name').order_by('ingredients__name').annotate(
            ingredients_total=Sum('ingredient_amounts__amount'))
        print(ingredients)
        shopping_list = {}
        for item in ingredients:
            title = item['ingredients__name']
            count = str(item['ingredients_total']) + ' ' + item['ingredients__measurement_unit__name']
            shopping_list[title] = count
        data = ''
        for key, value in shopping_list.items():
            data += f'{key} - {value}\n'
        return HttpResponse(data, content_type='csv')


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer
