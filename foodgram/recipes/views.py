from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import Tag, Recipe, IngredientAmount, Favourites
from .serializers import TagSerializer, RecipeReadSerializer, IngredientAmountSerializer, RecipeWriteSerializer, FavouritesSerializer
from foodgram.ingredients.models import Ingredient


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if not self.request.query_params.get('is_favorited'):
            return Recipe.objects.all()
        user = self.request.user
        return Recipe.objects.filter(in_favourites__user=user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            Favourites.objects.create(user=user, recipe=recipe)
            return Response({'status': 'Рецепт успешно добавлен в избранное'})
        else:
            fav_recipe = Favourites.objects.get(recipe=recipe, user=user)
            fav_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavouritesSerializer
    def get_queryset(self):
        user = self.request.user
        return Favourites.objects.filter(user=user)

