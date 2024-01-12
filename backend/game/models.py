import string
from django.contrib.auth.models import User
from django.db.models.functions import Length
from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.lookups import GreaterThan


# Create your models here.
class Game(models.Model):
    # longest english word is 45 letters so max_length should be big enough
    word = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def correct_guess(self):
        return self.guesses.filter(correct=True)

    @property
    def incorrect_guess(self):
        return self.guesses.filter(correct=False)

    def __str__(self):
        return f'{self.word} - {self.created}'

    def add_correct_guess(self, guess):
        return Guess.objects.create(guess=guess, game=self, correct=True)

    def add_incorrect_guess(self, guess):
        return Guess.objects.create(guess=guess, game=self, correct=False)


class Guess(models.Model):
    # longest english word is 45 letters so max_length should be big enough
    guess = models.CharField(max_length=50)
    correct = models.BooleanField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="guesses")
    is_word = models.GeneratedField(expression=GreaterThan(Length('guess'), 1), output_field=models.BooleanField(),
                                    db_persist=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.guess


class GameMap(models.Model):
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    game_1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='+')
    game_2 = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    game_slug = models.SlugField(unique=True, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.game_slug = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
        super().save(*args, **kwargs)
