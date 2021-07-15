from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserSubscription
from foodgram.recipes.models import Recipe


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

'''class SubscriptionSerializer(serializers.ModelSerializer):
    #subscription = UserSerializer(read_only=True)
    email = serializers.EmailField(source='subscription.email')
    id = serializers.EmailField(source='subscription.id')
    username = serializers.EmailField(source='subscription.username')
    first_name = serializers.EmailField(source='subscription.first_name')
    last_name = serializers.EmailField(source='subscription.first_name')

    class Meta:
        model = UserSubscription
        fields = ['email', 'id', 'first_name', 'last_name', 'username']'''