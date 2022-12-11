from datetime import date, timedelta

from django.core.exceptions import ValidationError


def contain_only_letters_validator(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Name must contain only letters!')

def yesterday():
    result = date.today() - timedelta(days=1)
    return result

def a_hundred_years_ago():
    result = date.today() - timedelta(days=100 * 365)
    return result