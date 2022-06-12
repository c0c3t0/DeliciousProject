from django.contrib import admin

from delicious_project.delicious.models import Recipe, CookedRecipe, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')


@admin.register(CookedRecipe)
class CookedRecipeAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name')
    pass
