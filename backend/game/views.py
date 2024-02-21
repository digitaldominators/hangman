from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from .models import GameMap, Game
from accounts.models import UserProfile
from game.serializers import NewGameSerializer
from rest_framework.response import Response

from generate_random_word import get_word_and_category

from .serializers import (
    JoinGameSerializer,
    GameSerializer,
    UpdateGameSerializer,
    GameWordSerializer,
    DefaultGameSettingsSerializer,
)


def set_default_game_setting(request, setting, value):
    """
    Set the default preferences for the user.
    If the user is logged in, then it updates the DefaultGameSettings object.
    If the user is not logged in, then is sets the users session.
    """
    if request.user.is_authenticated:
        game_settings, created = UserProfile.objects.get_or_create(user=request.user)
        if setting == "level":
            game_settings.level = value
        elif setting == "timer":
            game_settings.timer = value
        game_settings.save()
    else:
        # set the setting in sessions
        request.session[setting] = value


def get_user_default_settings(request):
    if request.user.is_authenticated:
        game_settings, created = UserProfile.objects.get_or_create(user=request.user)
        return {"level": game_settings.level, "timer": game_settings.timer,'private':game_settings.private}
    else:
        return {
            "level": request.session.get(f"level", 1),
            "timer": request.session.get("timer", 0),
        }


# Create your views here.
class DefaultSettingsViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to get or update default game settings.

     post data:
     -> level: difficulty level, int 1-3
     -> timer: positive number of seconds between turns, if 0 game is not timed
    """

    serializer_class = DefaultGameSettingsSerializer

    def create(self, request):
        """
        update the users default settings
        post data:
            level: difficulty level, int 1-3
            timer: positive number of seconds between turns, if 0 game is not timed
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("level"):
            set_default_game_setting(
                request, "level", serializer.validated_data.get("level")
            )
        if serializer.validated_data.get("timer") is not None:
            set_default_game_setting(
                request, "timer", serializer.validated_data.get("timer")
            )
        if serializer.validated_data.get("private") is not None:
            if request.user.is_authenticated:
                game_settings, created = UserProfile.objects.get_or_create(
                    user=request.user
                )
                game_settings.private = serializer.validated_data.get("private")
                game_settings.save()
            else:
                return Response(
                    {"message": "You must be logged in to change scoreboard privacy"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # display the settings
        return self.list(request)

    def list(self, request):
        """display the users settings"""
        return Response(get_user_default_settings(self.request))


class GameViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows games to be viewed, created, or updated.

    * game_slug - code used to join the game and is used as the game id to run any action on the game.
    * is_multiplayer - boolean if game is a multiplayer game.
    * full - boolean if the game has all the players needed to start the game.
    * timer - int - number of seconds between turns - 0 means timer is off. (this value is not currently used by the backend it is just saved for the frontend to use.)
    * level - int 1 to 3 - game difficulty level
    * status - next action that must be taken by player (won/loss/choose word/wait for other player to join/your turn/other players turn)
    * player - int 1 if this player is the first player 2 if second player (1st player created the game)
    * correct_guesses - list of letters/words - correct guesses
    * incorrect_guesses - list of letters/words - incorrect guesses
    * word - string - outline of the word each letter except spaces replaces with `_` unless user guesses the letter. If the word is `heads up` and the user guessed `e` `s` and `u` it would return `_e__s u_`.
    * game_score - int - current score in game
    * other_player_game_score - int - current score of the other players game
    """

    lookup_field = "game_slug"
    queryset = GameMap.objects.all()

    def get_serializer_class(self):
        """
        Returns the appropriate serializer for the given action.
        """
        if self.action == "create":
            return NewGameSerializer
        elif self.action == "join_game":
            return JoinGameSerializer
        elif self.action == "update":
            return UpdateGameSerializer
        elif self.action == "partial_update":
            return UpdateGameSerializer
        elif self.action == "choose_word":
            return GameWordSerializer
        return GameSerializer

    def get_serializer_context(self):
        """add the request to the serializer context"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_current_player(self, gameMap):
        """
        Get the current player playing the game.
        This works for authenticated and non-authenticated users.
        If the user is player 1 then it will return int 1.
        If the user is player 2 then it will return int 2.
        Otherwise, it will return 404 error current player not found.
        """
        if self.request.user.is_authenticated:
            if gameMap.player_1 == self.request.user:
                return 1
            if gameMap.player_2 == self.request.user:
                return 2
        else:
            return self.request.session.get(f"game__{gameMap.slug}")

        raise NotFound("current player not found")

    def get_game_map(self, request, slug):
        """
        Returns the GameMap object for the given request player with the given slug.
        If the current user is not playing a game with that slug, it will return 404 error.
        If the game with that slug no longer exists, it will return a 404.
        """
        if request.user.is_authenticated:
            return get_object_or_404(
                GameMap,
                Q(player_1=request.user) | Q(player_2=request.user),
                game_slug=slug,
            )
        else:
            game_number = request.session.get(f"game__{slug}")
            if game_number:
                return get_object_or_404(GameMap, game_slug=slug)
        raise NotFound()

    def get_current_game(self, request, slug):
        """
        Returns the Game object for the given request player with the given slug.
        If the current user is not playing a GameMap with that slug, it will return 404 error.
        If the game with that slug no longer exists, it will return a 404.
        """
        game_map = get_object_or_404(GameMap, game_slug=slug)
        if request.user.is_authenticated:
            if game_map.player_1 == self.request.user:
                return game_map.game_1
            elif game_map.player_2 == self.request.user:
                return game_map.game_2
        else:
            game_number = request.session.get(f"game__{slug}")
            if game_number:
                if game_number == 1:
                    return game_map.game_1
                elif game_number == 2:
                    return game_map.game_2
        raise NotFound(detail=f"Game not found")

    def create(self, request):
        """
        Create a new GameMap instance.
        post data:
        -> "multiplayer": false, // required (true/false)
        -> "word": "heads up", // required if multiplayer - set other players word. - If multi player is false this doesn't do anything.
        -> "timer": null, // optional - set time between modes
        -> "level": null // optional - set difficulty level - default 1
        -> "category": string choice of one of the categories optional
        -> "category_text": string, //only for multiplayer - string of category
        """

        # show human-readable error messages for creating a multiplayer game
        if request.data.get("multiplayer") == True:
            if request.data.get("category_text", "") == "":
                return Response(
                    {"message": "Category cannot be blank"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif request.data.get("word", "") == "":
                return Response(
                    {"message": "Word cannot be blank"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # get the current users default settings
        default_settings = get_user_default_settings(request)
        # save request data to data
        # must create copy since data is immutable
        data = request.data.copy()
        # if the user sent data of the level, update the default game level.
        if data.get("level"):
            set_default_game_setting(request, "level", data["level"])
        else:  # if user did not sent level, set the level to use the game default
            data["level"] = default_settings["level"]
        # if the user sent data of the timer, update the default game timer.
        if data.get("timer"):
            set_default_game_setting(request, "timer", data["timer"])
        else:  # if user did not sent timer, set the timer to use the game default
            data["timer"] = default_settings["timer"]
        # initialize serializer object
        serializer = self.get_serializer_class()(
            data=data, context=self.get_serializer_context()
        )
        # check if the data is valid, if not raise a 400 error
        serializer.is_valid(raise_exception=True)

        # if multiplayer game
        if serializer.validated_data.get("multiplayer"):
            # if the user is logged in then set player_1 to be logged in user otherwise add the user to the session.
            if request.user.is_authenticated:
                game_map = GameMap.objects.create(
                    player_1=request.user,
                    is_multiplayer=True,
                    level=serializer.validated_data.get("level"),
                    timer=serializer.validated_data.get("timer"),
                    category=serializer.validated_data.get("category_text"),
                    turns=[1, 2],
                )
            else:
                game_map = GameMap.objects.create(
                    is_multiplayer=True,
                    level=serializer.validated_data.get("level"),
                    timer=serializer.validated_data.get("timer"),
                    category=serializer.validated_data.get("category_text"),
                    turns=[1, 2],
                )
                request.session[f"game__{game_map.game_slug}"] = 1

            # create the game for the second player with the word that the first player chose.
            second_player_game = Game.objects.create(
                word=serializer.validated_data.get("word").lower()
            )
            game_map.game_2 = second_player_game
            game_map.save()
        else:  # single player game
            # create the game with a randomly generated word.
            category, phrase = get_word_and_category(
                category=serializer.validated_data.get("category")
            )
            game = Game.objects.create(word=phrase)

            # if the user is logged in then set player_1 to be logged in user otherwise add the user to the session.
            if request.user.is_authenticated:
                game_map = GameMap.objects.create(
                    player_1=request.user,
                    game_1=game,
                    is_multiplayer=False,
                    full=True,
                    level=serializer.validated_data.get("level"),
                    timer=serializer.validated_data.get("timer"),
                    category=category,
                    turns=[1],
                )
            else:
                game_map = GameMap.objects.create(
                    game_1=game,
                    is_multiplayer=False,
                    full=True,
                    level=serializer.validated_data.get("level"),
                    timer=serializer.validated_data.get("timer"),
                    category=category,
                    turns=[1],
                )
                request.session[f"game__{game_map.game_slug}"] = 1
        # set the next turn time
        game_map.next_turn_time = game_map.get_future_next_turn_time()
        game_map.save()
        # create a serializer for the game.
        game_serializer = GameSerializer(
            game_map, context=self.get_serializer_context()
        )
        # add if user is logged in or not
        data = game_serializer.data
        data["is_logged_in"] = request.user.is_authenticated
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def join_game(self, request):
        """
        api view which lets the second player join the game in multiplayer.
        post data
        -> game_slug : join code for the game
        """
        # get join game serializer
        serializer = self.get_serializer_class()(
            data={"game_slug": request.data.get("game_slug", "").upper()},
            context=self.get_serializer_context(),
        )
        # validate users input
        serializer.is_valid(raise_exception=True)

        try:
            # get game map
            game_map = get_object_or_404(
                GameMap, game_slug=serializer.validated_data["game_slug"]
            )
        except Http404:
            return Response(
                {"message": "Invalid join code"}, status=status.HTTP_404_NOT_FOUND
            )

        # don't let user join if game is already full
        if game_map.full:
            return Response(
                {"message": "Game full"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # set player to the current user. If user is not logged in set it with a session object
        if request.user.is_authenticated:
            # don't let the user be both player 1 and 2
            if game_map.player_1 == request.user:
                return Response(
                    {"message": "You are already playing this game."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set player 2 to be current user
            game_map.player_2 = request.user
        else:
            # don't let the user be both player 1 and 2
            if request.session.get(f"game__{game_map.game_slug}"):
                return Response(
                    {"message": "You are already playing this game."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set player 2 to be current user
            request.session[f"game__{game_map.game_slug}"] = 2

        # set the game to be full
        game_map.full = True
        game_map.save()

        # return the game object data
        game_serializer = GameSerializer(
            game_map, context=self.get_serializer_context()
        )
        # add if user is logged in or not
        data = game_serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def choose_word(self, request, game_slug):
        """
        API endpoint to let the second player choose a word.
        post data:
        -> word: string, the word/ phrase to for player 1 to guess
        """
        serializer = self.get_serializer_class()(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        game_map = self.get_game_map(request, game_slug)

        # if game 1 already exists then the word was already set by player 2
        if game_map.game_1:
            return Response(
                {"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # at this point only player 1 or 2 can reach this point. If the user is not player 2 or the game is not 2
        # then the user is player 1 and the word from player one was already set.
        if request.user.is_authenticated:
            if game_map.player_2 != request.user:
                return Response(
                    {"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            if request.session[f"game__{game_map.game_slug}"] != 2:
                return Response(
                    {"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED
                )

        # create game for player 1 with word set to players word
        game = Game.objects.create(word=serializer.validated_data["word"].lower())
        game_map.game_1 = game
        # set the next turn time
        game_map.next_turn_time = game_map.get_future_next_turn_time()
        game_map.save()

        game_serializer = GameSerializer(
            game_map, context=self.get_serializer_context()
        )
        # add if user is logged in or not
        data = game_serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        get a list of all the games the current user is playing
        """
        if request.user.is_authenticated:
            games = GameMap.objects.filter(
                Q(player_1=request.user) | Q(player_2=request.user)
            )[:50]
            serializer = GameSerializer(
                games, many=True, context=self.get_serializer_context()
            )
            return Response(serializer.data)
        else:
            # get a list of all the users session keys
            games = request.session.keys()
            # filter list of all the session keys to be just the sessions for games (all session keys that start with `game__`
            games = [game for game in games if game.startswith("game__")]
            # remove the game__ prefix from each string
            games = [game[6:] for game in games]

            # get game objects from database
            games = GameMap.objects.filter(game_slug__in=games)[:50]
            serializer = GameSerializer(
                games, many=True, context=self.get_serializer_context()
            )
            return Response(serializer.data)

    def retrieve(self, request, game_slug):
        """
        Return one game object
        """
        game_map = self.get_game_map(request, game_slug)
        if game_map.timer:
            if game_map.next_turn_time is None:
                game_map.next_turn_time = game_map.get_future_next_turn_time()
                game_map.turns = [1, 2]
                game_map.save()
            elif game_map.next_turn_time < timezone.now():
                game_map.next_turn_time = game_map.get_future_next_turn_time()
                game_map.turns = [1, 2]
                game_map.save()
        else:
            if game_map.next_turn_time is not None:
                game_map.next_turn_time = None
                game_map.save()
        return Response(
            GameSerializer(game_map, context=self.get_serializer_context()).data
        )

    def update(self, request, game_slug):
        """
        update the game map
        """
        game_map = self.get_game_map(request, game_slug)
        serializer = self.get_serializer_class()(
            game_map, data=request.data, context=self.get_serializer_context()
        )
        if serializer.is_valid():
            serializer.save()
            if request.data.get("timer"):
                set_default_game_setting(request, "timer", request.data.get("timer"))
            data = GameSerializer(game_map, context=self.get_serializer_context()).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
