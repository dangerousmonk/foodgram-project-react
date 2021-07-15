from django.core.files.base import ContentFile
import base64, uuid
from rest_framework import serializers

from foodgram.ingredients.models import Ingredient
from foodgram.users.serializers import UserSerializer
from foodgram.users.models import UserSubscription
from .models import Tag, Recipe, IngredientAmount, Favourites


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit.name')

    class Meta:
        model = IngredientAmount
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]

# to remove
'''class IngredientSerializer(serializers.ModelSerializer):
    amount = IngredientAmountSerializer(source='ingredient_amounts')
    measurement_unit = serializers.CharField(source='measurement_unit.name')

    def get_amount(self, obj):
        return IngredientAmount.objects.filter(ingredient=obj, recipe='ingredient_amounts.recipe').amount

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit', 'amount']'''



class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(many=True, source='ingredient_amounts')
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
        model = Favourites
        fields = '__all__'


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    # subscription = UserSerializer(read_only=True)
    email = serializers.EmailField(source='subscription.email')
    id = serializers.EmailField(source='subscription.id')
    username = serializers.EmailField(source='subscription.username')
    first_name = serializers.EmailField(source='subscription.first_name')
    last_name = serializers.EmailField(source='subscription.first_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = RecipeFavoriteSerializer(many=True, source='subscription.recipes')

    class Meta:
        model = UserSubscription
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        ]
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return UserSubscription.objects.filter(subscriber=user, subscription=obj.subscription).exists()
