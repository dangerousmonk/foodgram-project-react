from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django_filters import rest_framework as filters


from .serializers import SubscriptionSerializer, SubscriptionWriteSerializer
from .models import UserSubscription

from django.contrib.auth import get_user_model

User = get_user_model()
from .serializers import UserSerializer




class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserSubscription.objects.filter(
            subscriber=user).select_related('subscriber')


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(detail=True, methods=['get', 'delete'],
            serializer_class=SubscriptionWriteSerializer,
            permission_classes=[permissions.IsAuthenticated]
            )
    def subscribe(self, request, id=None):
        user = self.request.user
        subscription = self.get_object()
        if request.method == 'GET':
            data = {
                'subscriber': user.id,
                'subscription': subscription.id
            }
            serializer = self.get_serializer(data=data)
            if not serializer.is_valid(raise_exception=True):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
        instance = get_object_or_404(UserSubscription, subscriber=user, subscription=subscription)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
