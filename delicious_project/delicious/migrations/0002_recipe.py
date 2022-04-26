# Generated by Django 4.0.4 on 2022-04-25 13:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delicious', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('ingredients', models.TextField(max_length=300, validators=[django.core.validators.MinLengthValidator(10)])),
                ('description', models.TextField(max_length=1000, validators=[django.core.validators.MinLengthValidator(100)])),
                ('picture', models.URLField(blank=True, null=True)),
                ('preparation_time', models.PositiveIntegerField()),
                ('cooking_time', models.PositiveIntegerField()),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='delicious.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('title', 'user')},
            },
        ),
    ]