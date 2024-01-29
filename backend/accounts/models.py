from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.Model)

    # game settings
    # difficulty level number 1-3
    level = models.PositiveSmallIntegerField(default=1)
    # number of seconds before tern is skipped.
    timer = models.PositiveSmallIntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)