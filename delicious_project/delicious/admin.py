from django.contrib import admin

from delicious_project.delicious.models import Recipe, CookedRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(CookedRecipe)
class CookedRecipeAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name')
    pass
