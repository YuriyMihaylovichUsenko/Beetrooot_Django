from django import template
import datetime

register = template.Library()


@register.simple_tag
def oldety_func(value):
    oldety = (datetime.datetime.now() - value)*1000000
    if oldety.seconds > 60*60*24:
        return f'f{int(oldety.seconds/60*60*24)} days ago'
    if 60*60*24 > oldety.seconds > 60*60:
        return f'f{int(oldety.seconds/60*60)} hours ago'
    if 60 * 60 > oldety.seconds > 60:
        return f'f{int(oldety.seconds / 60)} minutes ago'
    else:
        return f'f{int(oldety.seconds)} seconds ago'


@register.filter
def my_upper(value: str):
    return value.upper()




