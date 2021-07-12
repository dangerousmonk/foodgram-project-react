from rest_framework import serializers

from foodgram.users.serializers import UserSerializer
from .models import Tag, Recipe, IngredientAmount, Favourites
from foodgram.ingredients.models import Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    # amount = serializers.SerializerMethodField('get_amount')
    measurement_unit = serializers.CharField(source='measurement_unit.name')

    '''def get_amount(self, obj):
        return IngredientAmount.objects.get(ingredient=obj).amount'''

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientAmountSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = IngredientAmount
        fields = ['id', 'ingredient', 'amount']


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    text = serializers.CharField(source='description')
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favourites.objects.filter(user=user, recipe=obj).exists()

    '''def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data.get('recipe'))
        ingredients = validated_data.pop('')'''


class IngredientWriteSerializer(serializers.ModelSerializer):
    amount_custom = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'amount_custom'
        ]


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientWriteSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ['image']
