from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountRegistrationSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, logout


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
            serializer.save()
            data["message"] = "Account has been created"

            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)
            login(request, user)

        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def login_user(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "You have logged in"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Login attempt failed"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(
    [
        "POST",
    ]
)
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return Response({"message": "You have logged out"}, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def change_password(request):
    if request.user.is_authenticated:
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        data = {}
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login(request, user)
        data["message"] = "Password has been changed"

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "You are not logged in"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(
    [
        "GET",
    ]
)
def user_authenticated(request):
    if request.user.is_authenticated:

        data = {}

        data["authenticated"] = True
        data["username"] = request.user.username
        if request.user.userprofile:
            data['total_score'] = request.user.userprofile.score
            data['average_score'] = request.user.userprofile.avg_score
            data['total_games'] = request.user.userprofile.games_played
            data['show_leaderboard'] = not request.user.userprofile.private
        else:
            data['highest_score'] = 0
            data['average_score'] = 0
            data['total_games'] = 0
            data['show_leaderboard'] = True
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"authenticated": False}, status=status.HTTP_200_OK)
