# Generated by Django 3.2.5 on 2021-07-10 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(editable=False, max_length=255, verbose_name='slug'),
        ),
    ]
