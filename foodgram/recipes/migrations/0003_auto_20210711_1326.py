# Generated by Django 3.2.5 on 2021-07-11 10:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_tag_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='time',
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(default=15, validators=[django.core.validators.MinValueValidator(1)], verbose_name='cooking time'),
            preserve_default=False,
        ),
    ]
