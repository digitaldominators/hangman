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
from django.http import Http404
from django.template.exceptions import TemplateDoesNotExist
from django.urls import path, include
from django.shortcuts import render
from rest_framework import routers

from game.views import GameViewSet
from game.views import DefaultSettingsViewSet
from scoreboard.views import ScoreboardViewSet
from category.views import CategoryViewSet

# from accounts.views import AccountViewSet

router = routers.DefaultRouter()
router.register(r'game', GameViewSet, basename='game')
router.register(r'settings', DefaultSettingsViewSet, basename='settings')
router.register(r'scoreboard', ScoreboardViewSet, basename='scoreboard')
router.register(r'categories', CategoryViewSet, basename='categories')

# router.register(r'accounts', AccountViewSet, basename='account')

def game_view(request, slug=None):
    template_name = 'index.html'
    if slug:
        template_name = slug + ".html"
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', game_view),
    path("<slug:slug>/", game_view),
]

if settings.DEBUG:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
