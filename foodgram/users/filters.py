from django_filters import rest_framework as filters
from django.db.models import Q, Count
from .models import UserSubscription


class UserSubscriptionFilter(filters.FilterSet):
    recipes_limit = filters.NumberFilter(method='recipes_limit_filter')

    class Meta:
        model = UserSubscription
        fields = ['recipes_limit']


    def recipes_limit_filter(self, queryset, name, value):
        user = self.request.user
        return queryset.annotate(
            nbar=Count('subscription__recipes')
        ).filter(
            nbar__gte=1
        )
