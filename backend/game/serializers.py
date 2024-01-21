from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import GameMap


class NewGameSerializer(serializers.Serializer):
    multiplayer = serializers.BooleanField()
    word = serializers.CharField(required=False)
    timer = serializers.IntegerField(default=0, required=False, min_value=0)
    level = serializers.IntegerField(default=0, required=False, min_value=0, max_value=3)

    def validate(self, data):
        if data['multiplayer']:
            if not data.get('word'):
                raise serializers.ValidationError({"word": "This field is required."})
        return data


class JoinGameSerializer(serializers.Serializer):
    game_slug = serializers.SlugField()


class GameWordSerializer(serializers.Serializer):
    word = serializers.CharField()

class GameSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    class Meta:
        model = GameMap
        fields = ['game_slug', 'is_multiplayer', 'full', 'timer', 'level', 'status','player']

    def get_status(self, instance):
        player = self.get_player(instance)
        if instance.is_multiplayer:
            if instance.full:
                if not instance.game_1:
                    if player == 1:
                        return "Waiting for player to choose word"
                    else:
                        return "choose word"
            else:
                if player == 1:
                    return "Waiting for player to join"
                else:
                    return "join game"
        else:
            return 'next turn'
        return 'started'

    def get_player(self, instance):
        if self.context['request'].user.is_authenticated:
            if instance.player_1 == self.context['request'].user:
                return 1
            if instance.player_2 == self.context['request'].user:
                return 2
        else:
            return self.context['request'].session.get(f'game__{instance.game_slug}')

        raise NotFound("current player not found")

class UpdateGameSerializer(serializers.ModelSerializer):
    timer = serializers.IntegerField(default=0, required=False, min_value=0)

    class Meta:
        model = GameMap
        fields = ['timer']
