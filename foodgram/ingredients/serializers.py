from rest_framework import serializers

from foodgram.users.serializers import UserSerializer
from .models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
