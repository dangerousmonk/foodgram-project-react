"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework_simplejwt import views as jwtviews

from foodgram.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    re_path(r'api/auth/token/login/?', jwtviews.TokenObtainPairView.as_view(), name='jwt-create'),
    re_path(r'api/auth/token/logout/?', views.TokenRefreshView.as_view(), name='jwt-refresh'),
]
