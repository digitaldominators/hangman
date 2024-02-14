# Generated by Django 5.0.1 on 2024-02-06 20:19

import django.db.models.expressions
import django.db.models.functions.comparison
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_userprofile_accounts_us_avg_sco_24f300_idx_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="avg_score",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.expressions.CombinedExpression(
                    models.F("score"),
                    "/",
                    django.db.models.functions.comparison.NullIf(
                        models.F("games_played"), 0
                    ),
                ),
                output_field=models.PositiveIntegerField(),
            ),
        ),
        migrations.AddIndex(
            model_name="userprofile",
            index=models.Index(
                fields=["avg_score"], name="accounts_us_avg_sco_24f300_idx"
            ),
        ),
    ]
