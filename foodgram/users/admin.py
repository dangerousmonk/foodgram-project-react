from django.contrib import admin
from .models import User, UserSubscription

admin.site.register(User)
admin.site.register(UserSubscription)
