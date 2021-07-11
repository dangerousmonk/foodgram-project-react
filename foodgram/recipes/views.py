from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from .models import Tag, Recipe, IngredientAmount
from .serializers import TagSerializer,RecipeReadSerializer, IngredientAmountSerializer, RecipeWriteSerializer
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

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST']:
            return RecipeWriteSerializer
        return RecipeReadSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        new_recipe = Recipe.objects.create(
            author=self.request.user,
            name=data['name'],
            image=data['image'],
            description=data['description'],
            cooking_time=data['cooking_time']
        )
        for tag in data['tags']:
            tag_object = Tag.objects.get(name=tag['name'])
            new_recipe.tags.add(tag_object)
        for ingredient in data['ingredients']:
            ingredient_object = Ingredient.objects.get(name=ingredient['name'])
            new_recipe.ingredients.add(ingredient_object)
        new_recipe.save()
        serializer = RecipeReadSerializer(new_recipe)
        return Response(serializer.data)

class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer