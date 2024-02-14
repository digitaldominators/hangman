import datetime
from string import ascii_letters
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import GameMap
from category.models import Category
import re
from . import signals


class GameModelSerializerPlayerMixin:
    """
    A bunch of convenience methods for the GameMap object
    -> get_status(instance)
    -> get_player(instance)
    -> get_game(instance)
    -> get_word_mask(instance)
    """

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

        if player in instance.turns:
            return 'your turn'
        else:
            return 'not your turn'

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
        word_mask = ["_" if letter in ascii_letters else letter for letter in word]
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
    level = serializers.IntegerField(default=1, required=False, min_value=0, max_value=3)
    category = serializers.ChoiceField(allow_blank=True, choices=[], required=False)
    category_text = serializers.CharField(required=False)

    def validate(self, data):
        if data['multiplayer']:
            if not data.get('category_text'):
                raise serializers.ValidationError({"category_text": "This field is required."})
            if not data.get('word'):
                raise serializers.ValidationError({"word": "This field is required."})
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = serializers.ChoiceField(allow_blank=True,
                                                          choices=Category.objects.filter(active=True),
                                                          required=False)


class JoinGameSerializer(serializers.Serializer):
    game_slug = serializers.SlugField()


class GameWordSerializer(serializers.Serializer):
    word = serializers.CharField()


class GameSerializer(GameModelSerializerPlayerMixin, serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    player_name = serializers.SerializerMethodField()
    correct_guesses = serializers.SerializerMethodField()
    incorrect_guesses = serializers.SerializerMethodField()
    word = serializers.SerializerMethodField()
    game_score = serializers.SerializerMethodField()
    other_player_game_score = serializers.SerializerMethodField()
    other_player_name = serializers.SerializerMethodField()

    class Meta:
        model = GameMap
        fields = ['game_slug', 'is_multiplayer', 'full', 'timer', 'level', 'status', 'player', 'correct_guesses',
                  'incorrect_guesses', 'word', 'category', 'game_score', 'other_player_game_score', 'player_name',
                  'other_player_name', 'next_turn_time']

    def get_game_score(self, instance):
        player = self.get_player(instance)
        if player == 1:
            if instance.game_1:
                return instance.game_1.score
        else:
            if instance.game_2:
                return instance.game_2.score
        return None

    def get_player_name(self, instance):
        print("hi")
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user.username
        else:
            return None

    def get_other_player_name(self, instance):
        player = self.get_player(instance)
        if player == 1:
            if instance.player_2:
                return instance.player_2.username
        elif player == 2:
            if instance.player_1:
                return instance.player_1.username
        return None

    def get_other_player_game_score(self, instance):
        player = self.get_player(instance)
        if player == 1:
            if instance.game_2:
                return instance.game_2.score
        else:
            if instance.game_1:
                return instance.game_1.score
        return None

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

    def validate_guess(self, data):
        status = self.get_status(self.instance)
        if status != 'your turn':
            raise serializers.ValidationError("Not your turn")
        return data

    def update(self, instance, validated_data):
        if validated_data.get('timer') is not None:
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
                    signals.game_over.send(sender=self.__class__, game_map=instance)
                else:  # incorrect guess
                    game.add_incorrect_guess(guess)
            else:  # guess is a letter
                if guess in game.word:
                    game.add_correct_guess(guess)

                    if self.get_word_mask(instance) == game.word:
                        instance.winner = player
                        instance.save()
                        signals.game_over.send(sender=self.__class__, game_map=instance)
                else:
                    game.add_incorrect_guess(guess)

            if instance.is_multiplayer:
                instance.turns = [turn for turn in instance.turns if player != turn]
                if len(instance.turns) == 0:
                    instance.next_turn_time = instance.get_future_next_turn_time()
                    instance.turns = [1, 2]
                instance.save()
        return instance


class DefaultGameSettingsSerializer(serializers.Serializer):
    timer = serializers.IntegerField(default=0, required=False, min_value=0)
    level = serializers.IntegerField(default=0, required=False, min_value=0, max_value=3)
