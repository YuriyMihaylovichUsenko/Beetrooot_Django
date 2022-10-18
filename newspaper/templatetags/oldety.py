from django import template
import datetime

register = template.Library()


@register.simple_tag
def oldety_func(value):
    return datetime.datetime.now() - value

@register.filter
def my_upper(value: str):
    return value.upper()
