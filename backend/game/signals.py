import django.dispatch
from django.dispatch import receiver

won_game = django.dispatch.Signal()
lost_game = django.dispatch.Signal()
correct_guess = django.dispatch.Signal()
incorrect_guess = django.dispatch.Signal()
game_over = django.dispatch.Signal()


@receiver(game_over)
def on_game_over(sender, game_map, **kwargs):
    if game_map.is_multiplayer:
        if game_map.winner == 1:
            won_game.send(
                sender=game_map,
                game=game_map.game_1,
                player=game_map.player_1,
                game_map=game_map,
            )
            lost_game.send(
                sender=game_map,
                game=game_map.game_2,
                player=game_map.player_2,
                game_map=game_map,
            )
        elif game_map.winner == 2:
            won_game.send(
                sender=game_map,
                game=game_map.game_2,
                player=game_map.player_2,
                game_map=game_map,
            )
            lost_game.send(
                sender=game_map,
                game=game_map.game_1,
                player=game_map.player_1,
                game_map=game_map,
            )
    else:  # single player
        if game_map.winner == 1:
            won_game.send(
                sender=game_map,
                game=game_map.game_1,
                player=game_map.player_1,
                game_map=game_map,
            )
