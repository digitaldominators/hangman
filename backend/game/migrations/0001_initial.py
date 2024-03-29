# Generated by Django 5.0.1 on 2024-01-31 21:33

import django.db.models.deletion
import django.db.models.functions.text
import django.db.models.lookups
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='GameMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_slug', models.SlugField(blank=True, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_multiplayer', models.BooleanField(default=False)),
                ('full', models.BooleanField(default=False)),
                ('winner', models.SmallIntegerField(blank=True, null=True)),
                ('level', models.PositiveSmallIntegerField(default=1)),
                ('timer', models.PositiveSmallIntegerField(default=0)),
                ('game_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.game')),
                ('game_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.game')),
                ('player_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('player_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guess', models.CharField(max_length=50)),
                ('correct', models.BooleanField()),
                ('is_word', models.GeneratedField(db_persist=True, expression=django.db.models.lookups.GreaterThan(django.db.models.functions.text.Length('guess'), 1), output_field=models.BooleanField())),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guesses', to='game.game')),
            ],
            options={
                'verbose_name_plural': 'guesses',
                'ordering': ['game', 'created'],
            },
        ),
    ]
