# Generated by Django 5.0.1 on 2024-01-22 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_gamemap_level_gamemap_timer'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemap',
            name='winner',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
