# Generated by Django 5.0.1 on 2024-02-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemap',
            name='category',
            field=models.CharField(default='no category', max_length=50),
            preserve_default=False,
        ),
    ]
