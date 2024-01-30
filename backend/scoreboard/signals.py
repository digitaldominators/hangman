from django.dispatch import receiver
from game.models import Game, Guess, GameMap
from django.contrib.auth.models import User

from game import signals as game_signals

from accounts.models import UserProfile


@receiver(game_signals.won_game)
def won_game(sender, game: Game, player: User, game_map: GameMap, **kwargs):
    if game_map.level == 1:
        game.score += 200
    elif game_map.level == 2:
        game.score += 400
    elif game_map.level == 3:
        game.score += 600
    game.save()


    if player:
        user_profile, created = UserProfile.objects.get_or_create(user=player)
        user_profile.score += game.score
        user_profile.games_played += 1
        user_profile.save()


@receiver(game_signals.lost_game)
def lost_game(sender, game: Game, player: User, game_map: GameMap, **kwargs):
    if player:
        user_profile, created = UserProfile.objects.get_or_create(user=player)
        user_profile.score += game.score
        user_profile.games_played += 1
        user_profile.save()


@receiver(game_signals.correct_guess)
def correct_guess(sender, game: Game, guess: Guess, **kwargs):
    game.score += 100
    game.save()


@receiver(game_signals.incorrect_guess)
def incorrect_guess(sender, game: Game, guess: Guess, **kwargs):
    game.score -= 50
    if game.score < 0:
        game.score = 0

    game.save()
