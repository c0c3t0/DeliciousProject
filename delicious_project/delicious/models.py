from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

UserModel = get_user_model()


class Category(models.Model):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    DESSERTS = 'Dessert'
    APPETIZERS = 'Appetizers'
    DRINKS = 'Drinks'
    UNCATEGORIZED = 'Uncategorized'

    TYPES = [(x, x) for x in (BREAKFAST, LUNCH, DINNER, DESSERTS, APPETIZERS, DRINKS, UNCATEGORIZED)]

    title = models.CharField(
        max_length=max(len(x) for x, _ in TYPES),
        choices=TYPES,
        default=UNCATEGORIZED,
    )

    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("category slug", kwargs={"slug": self.slug})


class Recipe(models.Model):
    TITLE_MAX_LEN = 100
    INGREDIENT_MAX_LEN = 3000
    DESCRIPTION_MAX_LEN = 10000

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        unique=True,
    )

    ingredients = models.TextField(
        max_length=INGREDIENT_MAX_LEN,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LEN,
    )

    picture = models.URLField(
        null=True,
        blank=True,
    )

    preparation_time = models.PositiveIntegerField()

    cooking_time = models.PositiveIntegerField()

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    cooked = models.ManyToManyField(
        UserModel,
        blank=True,
        related_name='cooked',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-publication_date',)

    def __str__(self):
        return self.title

    @property
    def total_cooking_time(self):
        return self.preparation_time + self.cooking_time

    @property
    def cooked_counter(self):
        return self.cooked.all().count()



class Comment(models.Model):
    text = models.TextField()

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    published_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-published_on',)
