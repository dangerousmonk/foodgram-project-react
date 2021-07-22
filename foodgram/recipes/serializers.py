import base64
import uuid
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework import serializers

from foodgram.ingredients.models import Ingredient
from foodgram.users.models import UserSubscription
from .models import Tag, Recipe, IngredientAmount
from .services import add_recipe_with_ingredients_tags
from .services import update_recipe_with_ingredients_tags

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Define here to avoid circular imports
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return UserSubscription.objects.filter(
            subscriber=user, subscription=obj
        ).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext
            )
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = IngredientAmount
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts'
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]


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
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(max_length=False, use_url=True)
    is_favorited = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        instance = add_recipe_with_ingredients_tags(validated_data)
        return instance

    def update(self, instance, validated_data):
        updated_instance = update_recipe_with_ingredients_tags(
            validated_data,
            instance)
        return updated_instance

    def to_representation(self, instance):
        serializer_data = RecipeReadSerializer(
            instance, context=self.context
        ).data
        return serializer_data

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'ingredients',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
            'is_favorited'
        ]


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
