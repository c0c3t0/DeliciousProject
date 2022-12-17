from django import template

register = template.Library()


@register.filter()
def get_name(value):
    result = ''
    for char in value:
        if char != '@':
            result += char
        else:
            break

    return result
