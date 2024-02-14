from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import AccountRegistrationSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@api_view(
    [
        "POST",
    ]
)
def user_registration_view(request):
    if request.method == "POST":
        serializer = AccountRegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Account has been created"
            data["username"] = account.username
            data["email"] = account.email

            token = Token.objects.get(user=account).key
            data["token"] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(
    [
        "POST",
    ]
)
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                {"Message": "You have logged in"}, status=status.HTTP_200_OK
            )
            # return redirect('home')
        else:
            return Response(
                {"Message": "Login attempt failed"}, status=status.HTTP_401_UNAUTHORIZED
            )
            # messages.success(request, ('Login attempt failed'))
            # return redirect('login')
    # else:
    # return render(request, 'authenticate/login.html', {})


@api_view(
    [
        "POST",
    ]
)
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return Response({"Message": "You have logged out"}, status=status.HTTP_200_OK)
        # messages.success(request, ('You were logged out'))
        # return redirect('home')
