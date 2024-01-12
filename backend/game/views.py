from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound

from .models import GameMap, Game
from game.serializers import NewGameSerializer
from rest_framework.response import Response

from generate_random_word import generate_random_word


# Create your views here.
class GameViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return NewGameSerializer

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
        else:  # single player game
            game = Game.objects.create(word=generate_random_word())
            if request.user.is_authenticated:
                game_map = GameMap.objects.create(player_1=request.user, game_1=game, is_multiplayer=False)
            else:
                game_map = GameMap.objects.create(game_1=game, is_multiplayer=False)
                request.session[f'game__{game_map.slug}'] = 1
        return Response({"game_slug"     : game_map.game_slug,
                         "is_multiplayer": game_map.is_multiplayer,
                         "is_logged_in"  : request.user.is_authenticated},
                        status=status.HTTP_201_CREATED)
