# Generated by Django 4.0.4 on 2022-04-25 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delicious', '0006_alter_recipe_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(max_length=10000, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]