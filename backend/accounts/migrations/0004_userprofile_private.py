# Generated by Django 5.0.1 on 2024-02-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_userprofile_avg_score_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="private",
            field=models.BooleanField(default=False),
        ),
    ]
