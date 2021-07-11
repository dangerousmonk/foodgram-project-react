from rest_framework import serializers

from foodgram.users.serializers import UserSerializer
from .models import Tag, Recipe, Ingredient, IngredientAmount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField('get_amount')
    measurement_unit = serializers.CharField(source='measurement_unit.name')

    def get_amount(self,obj):
        return IngredientAmount.objects.get(ingredient=obj).amount

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit','amount']


class IngredientAmountSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = IngredientAmount
        fields = ['id', 'ingredient', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    text = serializers.CharField(source='description')

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    '''def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data.get('recipe'))
        ingredients = validated_data.pop('')'''

