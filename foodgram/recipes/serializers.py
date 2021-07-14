from rest_framework import serializers

from foodgram.users.serializers import UserSerializer
from .models import Tag, Recipe, IngredientAmount, Favourites
from foodgram.ingredients.models import Ingredient

from django.core.files.base import ContentFile


import base64, uuid




import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super().to_internal_value(data)


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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

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


class IngredientWriteSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'amount'
        ]


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientWriteSerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    image = Base64ImageField(max_length=False, use_url=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        for tag in tags_data:
            tag_object = Tag.objects.get(id=tag.id)
            new_recipe.tags.add(tag_object)
        for ingredient in ingredients_data:
            ingredient_object = Ingredient.objects.get(id=ingredient['id'])
            new_recipe.ingredients.add(ingredient_object, through_defaults={'amount': ingredient['amount']})
        new_recipe.save()
        return new_recipe

    def to_representation(self, instance):
        serializer_data = RecipeReadSerializer(instance, context=self.context).data
        return serializer_data

    class Meta:
        model = Recipe
        fields = '__all__'

class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model =Favourites
        fields = '__all__'