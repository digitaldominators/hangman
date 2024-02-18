from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import AccountRegistrationSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

@api_view(['POST',])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = AccountRegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid(raise_exception=True):
            account = serializer.save()

            data['message'] = 'Account has been created'
            data['username'] = account.username

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)
    
@api_view(['POST',])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'You have logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login attempt failed'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST',])
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'You have logged out'}, status=status.HTTP_200_OK)
    
@api_view(['POST',])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        data = {}

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()
            token = Token.objects.get(user=user).key

            data['message'] = 'Password has been changed'
            data['token'] = token
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST',])
def user_authenticated(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return Response({'username': request.user})