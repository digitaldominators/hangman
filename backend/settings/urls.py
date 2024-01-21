"""
URL configuration for hangman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from game.views import GameViewSet
from accounts import views

router = routers.DefaultRouter()
router.register(r'game', GameViewSet, basename='game')
#router.register(r'accounts', AccountViewSet, basename='account')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', views.user_registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]