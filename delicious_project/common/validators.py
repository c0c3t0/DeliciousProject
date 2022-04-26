from django.core.exceptions import ValidationError


def contain_only_letters_validator(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Name must contain only letters!')