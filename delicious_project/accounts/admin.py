from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from delicious_project.accounts.models import Profile, DeliciousAppUser

UserModel = get_user_model()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    model = DeliciousAppUser
    list_display = ('email', 'is_staff',)
    list_filter = ('email', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)