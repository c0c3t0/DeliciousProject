from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from delicious_project.accounts.models import Profile

UserModel = get_user_model()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')

@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = UserModel

    list_display = ('email', 'is_staff', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('is_superuser', 'is_staff')