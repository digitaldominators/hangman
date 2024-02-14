# Generated by Django 5.0.1 on 2024-01-31 21:33

import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("level", models.PositiveSmallIntegerField(default=1)),
                ("timer", models.PositiveSmallIntegerField(default=0)),
                ("score", models.PositiveIntegerField(default=0)),
                ("games_played", models.PositiveIntegerField(default=0)),
                (
                    "avg_score",
                    models.GeneratedField(
                        db_persist=True,
                        expression=django.db.models.expressions.CombinedExpression(
                            models.F("score"), "/", models.F("games_played")
                        ),
                        output_field=models.PositiveIntegerField(),
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=models.Model, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["score"], name="accounts_us_score_1a0b3d_idx"),
                    models.Index(
                        fields=["avg_score"], name="accounts_us_avg_sco_24f300_idx"
                    ),
                ],
            },
        ),
    ]
