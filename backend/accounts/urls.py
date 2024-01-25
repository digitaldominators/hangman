from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration_view, name='register'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
]