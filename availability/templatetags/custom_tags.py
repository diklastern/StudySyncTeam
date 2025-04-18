from django import template

register = template.Library()

@register.filter
def to(start, end):
    return range(start, end)

@register.filter
def format_hour(value):
    return f"{int(value):02d}:00"
