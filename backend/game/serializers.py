from rest_framework import serializers


class NewGameSerializer(serializers.Serializer):
    multiplayer = serializers.BooleanField()