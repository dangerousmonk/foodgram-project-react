from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserSubscription
from foodgram.recipes.models import Recipe
from foodgram.recipes.serializers import RecipeFavoriteSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
        return UserSubscription.objects.filter(subscriber=user, subscription=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='subscription.email')
    id = serializers.EmailField(source='subscription.id')
    username = serializers.EmailField(source='subscription.username')
    first_name = serializers.EmailField(source='subscription.first_name')
    last_name = serializers.EmailField(source='subscription.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    #recipes = RecipeFavoriteSerializer(many=True, source='subscription.recipes')
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

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
            'recipes_count'
        ]
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return UserSubscription.objects.filter(subscriber=user, subscription=obj.subscription).exists()

    def get_recipes_count(self, obj):
        return obj.subscription.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.subscription.recipes.all()[:3]
        return RecipeFavoriteSerializer(recipes, many=True).data



class SubscriptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = [
            'subscriber',
            'subscription',
        ]

    def validate_subscription(self, value):
        request = self.context['request']
        if not request.user == value:
            return value
        raise serializers.ValidationError('User cant subscribe for himself')