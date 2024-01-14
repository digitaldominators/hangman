from rest_framework import serializers

from .models import GameMap


class NewGameSerializer(serializers.Serializer):
    multiplayer = serializers.BooleanField()
    word = serializers.CharField(required=False)

    def validate(self, data):
        if data['multiplayer']:
            if not data.get('word'):
                raise serializers.ValidationError({"word": "This field is required."})
        return data


class JoinGameSerializer(serializers.Serializer):
    game_slug = serializers.SlugField()
    word = serializers.CharField()


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMap
        fields = ['game_slug', 'is_multiplayer', 'full']
