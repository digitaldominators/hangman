from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import password_validation


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, max_length=128, write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ["username", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})

        if User.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({"error": "Username already exists"})

        account = User(username=self.validated_data["username"])
        account.set_password(password)
        account.save()

        return account


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        # style={"input_type": "password"}, max_length=128, write_only=True, required=True
    )
    password2 = serializers.CharField(
        max_length=128,
        write_only=True,
        required=True,
        # style={"input_type": "password"}, max_length=128, write_only=True, required=True
    )

    # def validate_old_password(self, value):
    # user = self.context['request'].user
    # if not user.check_password(value):
    # raise serializers.ValidationError({'error': 'Current password is incorrect'})
    # return value

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"error": "Passwords do not match"})
        password_validation.validate_password(
            data.get("password"), self.context["request"].user
        )
        if not data.get("password"):
            raise serializers.ValidationError({"error": "password is required"})
        return data

    def save(self, **kwargs):
        password = self.validated_data["password"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user
