from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from delicious_project.accounts.managers import DeliciousAppUserManager
from delicious_project.common.validators import contain_only_letters_validator


class DeliciousAppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_email_verified = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,  # auto_now_add ne promenq stoinostta si
    )

    last_login = models.DateTimeField(
        auto_now=True,  # promenq stoinostta si
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = DeliciousAppUserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 3
    LAST_NAME_MAX_LENGTH = 30

    DO_NOT_SHOW = 'Do not show'
    MALE = 'Male'
    FEMALE = 'Female'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            contain_only_letters_validator,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            contain_only_letters_validator,
        )
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
    )

    picture = models.URLField(
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        DeliciousAppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ('first_name', 'last_name',)
