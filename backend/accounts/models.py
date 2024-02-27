from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Max
from django.db.models.functions import NullIf
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


def get_default_level():
    return settings.DEFAULT_LEVEL


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.Model)

    # game settings
    # difficulty level number 1-3
    level = models.PositiveSmallIntegerField(default=get_default_level)
    # number of seconds before turn is skipped.
    timer = models.PositiveSmallIntegerField(default=0)

    # total score
    score = models.PositiveIntegerField(default=0)
    # number of games played
    games_played = models.PositiveIntegerField(default=0)
    # average score
    avg_score = models.GeneratedField(
        expression=F("score") / NullIf(F("games_played"), 0),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
    )

    # set to true if user wants to remove scores from leaderboard
    private = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["score"]), models.Index(fields=["avg_score"])]

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
