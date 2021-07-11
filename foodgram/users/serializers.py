from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UserSubscription

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
