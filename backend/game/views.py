from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, NotAuthenticated

from .models import GameMap, Game
from game.serializers import NewGameSerializer
from rest_framework.response import Response

from generate_random_word import generate_random_word

from .serializers import JoinGameSerializer, GameSerializer, UpdateGameSerializer, GameWordSerializer


# Create your views here.
class GameViewSet(viewsets.GenericViewSet):
    lookup_field = 'game_slug'
    queryset = GameMap.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return NewGameSerializer
        elif self.action == 'join_game':
            return JoinGameSerializer
        elif self.action == 'update':
            return UpdateGameSerializer
        elif self.action == 'choose_word':
            return GameWordSerializer
        return GameSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_current_player(self, gameMap):
        if self.request.user.is_authenticated:
            if gameMap.player_1 == self.request.user:
                return 1
            if gameMap.player_2 == self.request.user:
                return 2
        else:
            return self.request.session.get(f'game__{gameMap.slug}')

        raise NotFound("current player not found")

    def get_game_map(self, request, slug):
        if request.user.is_authenticated:
            return get_object_or_404(GameMap, Q(player_1=request.user) | Q(player_2=request.user), game_slug=slug)
        else:
            game_number = request.session.get(f'game__{slug}')
            if game_number:
                return get_object_or_404(GameMap, game_slug=slug)
        raise NotFound()

    def get_current_game(self, request, slug):
        game_map = GameMap.objects.get(game_slug=slug)
        if request.user.is_authenticated:
            if game_map.player_1 == self.request.user:
                return game_map.game_1
            elif game_map.player_2 == self.request.user:
                return game_map.game_2
        else:
            game_number = request.session.get(f'game__{slug}')
            if game_number:
                if game_number == 1:
                    return game_map.game_1
                elif game_number == 2:
                    return game_map.game_2
        raise NotFound(detail=f'Game not found')

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        # if multiplayer game
        if serializer.validated_data.get('multiplayer'):
            if request.user.is_authenticated:
                game_map = GameMap.objects.create(player_1=request.user, is_multiplayer=True)
            else:
                game_map = GameMap.objects.create(is_multiplayer=True)
                request.session[f'game__{game_map.game_slug}'] = 1

            second_player_game = Game.objects.create(word=serializer.validated_data.get('word'))
            game_map.game_2 = second_player_game
            game_map.save()
        else:  # single player game
            game = Game.objects.create(word=generate_random_word())
            if request.user.is_authenticated:
                game_map = GameMap.objects.create(player_1=request.user, game_1=game, is_multiplayer=False, full=True)
            else:
                game_map = GameMap.objects.create(game_1=game, is_multiplayer=False, full=True)
                request.session[f'game__{game_map.game_slug}'] = 1

        game_serializer = GameSerializer(game_map,context=self.get_serializer_context())
        # add if user is logged in or not
        data = game_serializer.data
        data['is_logged_in'] = request.user.is_authenticated
        return Response(data,
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def join_game(self, request):
        serializer = self.get_serializer_class()(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        game_map = get_object_or_404(GameMap, game_slug=serializer.validated_data['game_slug'])
        if game_map.full:
            return Response({"message": "Game full"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_authenticated:
            game_map.player_2 = request.user
        else:
            request.session[f'game__{game_map.game_slug}'] = 2

        game_map.full = True
        game_map.save()

        game_serializer = GameSerializer(game_map, context=self.get_serializer_context())
        # add if user is logged in or not
        data = game_serializer.data
        data['is_logged_in'] = request.user.is_authenticated
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def choose_word(self, request, game_slug):
        serializer = self.get_serializer_class()(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        game_map = self.get_game_map(request, game_slug)

        if game_map.game_1:
            return Response({"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED)

        # at this point only player 1 or 2 can reach this point. If the user is not player 2 or the game is not 2
        # then the user is player 1 and the word from player one was already set.
        if request.user.is_authenticated:
            if game_map.player_2 != request.user:
                return Response({"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.session[f'game__{game_map.game_slug}'] != 2:
                return Response({"message": "Word already set"}, status=status.HTTP_401_UNAUTHORIZED)

        # create game for player 1 with word set to players word
        game = Game.objects.create(word=serializer.validated_data['word'])
        game_map.game_1 = game
        game_map.full = True
        game_map.save()

        game_serializer = GameSerializer(game_map, context=self.get_serializer_context())
        # add if user is logged in or not
        data = game_serializer.data
        data['is_logged_in'] = request.user.is_authenticated
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request):
        if request.user.is_authenticated:
            games = GameMap.objects.filter(Q(player_1=request.user) | Q(player_2=request.user))
            serializer = GameSerializer(games, many=True, context=self.get_serializer_context())
            return Response(serializer.data)
        else:
            games = request.session.keys()
            # filter list of all the session keys to be just the sessions for games
            games = [game for game in games if game.startswith("game__")]
            # remove the game__ prefix from each string
            games = [game[6:] for game in games]

            # get game objects from database
            games = GameMap.objects.filter(game_slug__in=games)
            serializer = GameSerializer(games, many=True,context=self.get_serializer_context())
            return Response(serializer.data)

    def retrieve(self, request, game_slug):
        game_map = self.get_game_map(request, game_slug)
        return Response(GameSerializer(game_map,context=self.get_serializer_context()).data)

    def update(self, request, game_slug):
        """
        update the game map
        """
        game_map = self.get_game_map(request, game_slug)
        serializer = self.get_serializer_class()(game_map, data=request.data,context=self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            data = GameSerializer(game_map,context=self.get_serializer_context()).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
