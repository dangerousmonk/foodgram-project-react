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
    queryset = Recipe.objects.all()
    # return Recipe.objects.filter(author=request.user.
    # is favorited

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        Favourites.objects.create(user=user, recipe=recipe)
        return Response({'status': 'Рецепт успешно добавлен в избранное'})
        #else:
        #return Response(serializer.errors,
        #                    status=status.HTTP_400_BAD_REQUEST)



class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavouritesSerializer
    def get_queryset(self):
        user = self.request.user
        return Favourites.objects.filter(user=user)

