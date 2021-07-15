from django.views import generic
from rest_framework import viewsets

from foodgram.recipes.serializers import  SubscriptionSerializer
from .models import UserSubscription

from django.contrib.auth import get_user_model
User = get_user_model()

class IndexView(generic.TemplateView):
    template_name = 'build/index.html'


class SubscriptionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return UserSubscription.objects.filter(subscriber=user).select_related('subscriber')

    serializer_class = SubscriptionSerializer