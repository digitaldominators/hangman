from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from game.models import GameMap

from .models import UserProfile


def get_player(game_map, player_number):
    if player_number == 1:
        return game_map.player_1
    elif player_number == 2:
        return game_map.player_2
    else:
        return None


def set_player(game_map, player_number, user):
    # if the player is already set then return False
    if get_player(game_map, player_number):
        return False
    elif player_number == 1:
        # if the user player is this player then return False
        if get_player(game_map, 2) == user:
            return False
    elif player_number == 2:
        # if the user player is this player then return False
        if get_player(game_map, 1) == user:
            return False

    # set the player
    if player_number == 1:
        game_map.player_1 = user
    elif player_number == 2:
        game_map.player_2 = user
    game_map.save()
    return True


def get_game(game_map, player_number):
    if player_number == 1:
        return game_map.game_1
    elif player_number == 2:
        return game_map.game_2
    else:
        return None


@receiver(user_logged_in)
def associate_requests_anonymous_games_with_user(sender, request, user, **kwargs):
    """
    associate the anonymous users games with the now logged-in user then remove the session info for the game
    if the game is over then add the score to the users leaderboard
    """
    # get a list of all the users session keys
    games = request.session.keys()
    # filter list of all the session keys to be just the sessions for games (all session keys that start with `game__`
    games = [game for game in games if game.startswith("game__")]

    # associate game with user, delete session keys
    for game in games:
        game_id = game[6:]
        # get if the user is the first player or second player
        game_player_number = request.session[game]
        game_map = GameMap.objects.get(game_slug=game_id)

        # set the player for the game to the current user if the player is not already set and the user is not the
        # other player
        player_got_set = set_player(game_map, game_player_number, user)
        if player_got_set:
            if game_map.winner:
                # add the score to the users leaderboard
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                if player_game := get_game(game_map, game_player_number):
                    user_profile.score += player_game.score
                    user_profile.games_played += 1
                    user_profile.save()
            del request.session[game]
