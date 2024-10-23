from django import template

register = template.Library()

@register.filter
def repeat(value, count):
    """Repeat a string 'count' times."""
    return value * count
