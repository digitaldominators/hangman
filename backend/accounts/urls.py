from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration_view, name='register'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('user_authenticated/', views.user_authenticated, name='user_authenticated'),
    path('change_password/', views.change_password, name='change_password')
]