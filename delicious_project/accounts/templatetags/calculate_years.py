from django import template
import datetime

register = template.Library()


@register.filter()
def calculate_years(value):
    year_of_birth = value.year
    today = datetime.date.today()
    age = today.year - year_of_birth
    return age
