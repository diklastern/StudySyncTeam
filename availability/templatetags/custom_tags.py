from django import template

register = template.Library()

@register.filter
def to(value, arg):
    """Usage: {% for i in 8|to:22 %}"""
    return range(int(value), int(arg))

@register.filter
def format_hour(value):
    try:
        return f"{int(value):02d}:00"
    except:
        return value
