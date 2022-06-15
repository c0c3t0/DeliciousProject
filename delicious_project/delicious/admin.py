from django.contrib import admin

from delicious_project.delicious.models import Recipe, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'cooked_counter')

