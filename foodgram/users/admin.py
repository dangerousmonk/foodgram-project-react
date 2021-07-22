from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import User, UserSubscription

admin.site.register(UserSubscription)


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined'
    )
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email', 'first_name',)
    ordering = ('date_joined',)
    empty_value_display = '-'
    readonly_fields = ('date_joined', 'last_login')
