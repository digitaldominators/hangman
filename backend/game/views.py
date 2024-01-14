from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from .models import GameMap, Game
from game.serializers import NewGameSerializer
from rest_framework.response import Response

from generate_random_word import generate_random_word

from .serializers import JoinGameSerializer, GameSerializer


# Create your views here.
class GameViewSet(viewsets.GenericViewSet):
    queryset = GameMap.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return NewGameSerializer
        elif self.action == 'join_game':
            return JoinGameSerializer

        return GameSerializer

    def get_current_game(self, request, slug):
        game_map = GameMap.objects.get(slug=slug)
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
        serializer = self.get_serializer_class()(data=request.data)
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

        game_serializer = GameSerializer(game_map)
        # add if user is logged in or not
        data = game_serializer.data
        data['is_logged_in'] = request.user.is_authenticated
        return Response(data,
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def join_game(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_map = get_object_or_404(GameMap, game_slug=serializer.validated_data['game_slug'])
        if game_map.full:
            return Response({"message": "Game full"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_authenticated:
            game_map.player_2 = request.user
        else:
            request.session[f'game__{game_map.game_slug}'] = 2

        # create game for player 1 with word set to players word
        game = Game.objects.create(word=serializer.validated_data['word'])
        game_map.game_1 = game
        game_map.full = True
        game_map.save()

        game_serializer = GameSerializer(game_map)
        # add if user is logged in or not
        data = game_serializer.data
        data['is_logged_in'] = request.user.is_authenticated
        return Response(data, status=status.HTTP_201_CREATED)


    def list(self, request):
        if request.user.is_authenticated:
            games = GameMap.objects.filter(Q(player_1=request.user) | Q(player_2=request.user))
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        else:
            games = request.session.keys()
            # filter list of all the session keys to be just the sessions for games
            games = [game for game in games if game.startswith("game__")]
            # remove the game__ prefix from each string
            games = [game[6:] for game in games]

            # get game objects from database
            games = GameMap.objects.filter(game_slug__in=games)
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
