from django import template

register = template.Library()

@register.filter(name='to_plus')
def to_plus(value):
    """Removes all values of arg from the given string"""
    return value.replace(" ", "+")
