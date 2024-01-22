from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import GameMap
import re


class GameModelSerializerPlayerMixin:
    def get_status(self, instance):
        player = self.get_player(instance)

        # if the game is over
        if instance.winner:
            if instance.winner == player:
                return "you won"
            else:
                return "you lost"

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
            return 'your turn'

        if instance.game_2.guesses.count() == instance.game_1.guesses.count():
            return 'your turn'
        elif instance.game_2.guesses.count() > instance.game_1.guesses.count():
            if player == 2:
                return 'not your turn'
            else:
                return 'your turn'
        else:
            if player == 1:
                return 'not your turn'
            else:
                return 'your turn'

    def get_player(self, instance):
        if self.context['request'].user.is_authenticated:
            if instance.player_1 == self.context['request'].user:
                return 1
            if instance.player_2 == self.context['request'].user:
                return 2
        else:
            return self.context['request'].session.get(f'game__{instance.game_slug}')

        raise NotFound("current player not found")

    def get_game(self, instance):
        player = self.get_player(instance)
        if player == 1:
            return instance.game_1
        else:
            return instance.game_2

    def get_word_mask(self, instance):
        if not self.get_game(instance):
            return None
        correct_guesses = self.get_game(instance).guesses.filter(is_word=False, correct=True).values_list('guess',
                                                                                                          flat=True)
        word = self.get_game(instance).word
        word_mask = [" " if letter == " " else "_" for letter in word]
        for letter in correct_guesses:
            positions = [x.start() for x in re.finditer(letter, word)]

            for position in positions:
                word_mask[position] = letter

        word_mask = "".join(word_mask)
        return word_mask


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


class GameSerializer(GameModelSerializerPlayerMixin, serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    correct_guesses = serializers.SerializerMethodField()
    incorrect_guesses = serializers.SerializerMethodField()
    word = serializers.SerializerMethodField()

    class Meta:
        model = GameMap
        fields = ['game_slug', 'is_multiplayer', 'full', 'timer', 'level', 'status', 'player', 'correct_guesses',
                  'incorrect_guesses', 'word']

    def get_correct_guesses(self, instance):
        if self.get_game(instance):
            return self.get_game(instance).correct_guesses.values_list('guess', flat=True)
        return []

    def get_incorrect_guesses(self, instance):
        if self.get_game(instance):
            return self.get_game(instance).incorrect_guesses.values_list('guess', flat=True)
        return []

    def get_word(self, instance):
        return self.get_word_mask(instance)


class UpdateGameSerializer(GameModelSerializerPlayerMixin, serializers.ModelSerializer):
    timer = serializers.IntegerField(default=0, required=False, min_value=0)
    guess = serializers.CharField(required=False)

    class Meta:
        model = GameMap
        fields = ['timer', 'guess']

    def update(self, instance, validated_data):
        if validated_data.get('timer'):
            instance.timer = validated_data.get('timer')
            instance.save()
        if validated_data.get('guess'):
            player = self.get_player(instance)
            game = self.get_game(instance)
            guess = validated_data.get('guess').lower()

            # guess was already made
            if game.guesses.filter(guess=guess).exists():
                return instance

            # if guess is a word
            if len(guess) > 1:
                # correct
                if game.word == guess:
                    game.add_correct_guess(guess)
                    instance.winner = player
                    instance.save()
                else:  # incorrect guess
                    game.add_incorrect_guess(guess)
            else:  # guess is a letter
                if guess in game.word:
                    game.add_correct_guess(guess)

                    if "_" not in self.get_word_mask(instance):
                        instance.winner = player
                        instance.save()
                else:
                    game.add_incorrect_guess(guess)
        return instance
