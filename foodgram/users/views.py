from django.views import generic
from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

class CustomUserViewSet(UserViewSet):
    @action(detail=True, methods=['get', 'delete'])
    def subscribe(self, request, id=None):
        user = self.request.user
        subscription = self.get_object()
        if request.method == 'GET':
            UserSubscription.objects.create(subscriber=user, subscription=subscription)
            return Response({'status': 'Подписка успешно создана'})
        else:
            subscription = UserSubscription.objects.get(subscriber=user, subscription=subscription)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)