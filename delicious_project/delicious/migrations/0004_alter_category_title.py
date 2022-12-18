# Generated by Django 4.0.4 on 2022-12-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delicious', '0003_remove_recipe_is_cooked_alter_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Dessert', 'Dessert'), ('Appetizers', 'Appetizers'), ('Drinks', 'Drinks'), ('Uncategorized', 'Uncategorized')], default='Uncategorized', max_length=13),
        ),
    ]