# Generated by Django 5.0.1 on 2024-02-07 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_options_phrase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='phrase',
            unique_together={('category', 'phrase')},
        ),
    ]
