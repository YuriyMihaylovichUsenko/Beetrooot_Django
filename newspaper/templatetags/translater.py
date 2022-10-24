from django import template
import datetime

register = template.Library()


# @register.simple_tag
# def transleter(obj, lan):
#     if lan.startswith('en'):
#         return obj.name_en
#     else:
#         return obj.name


@register.filter
def transleter_names(obj, lan):
    if lan.startswith('en'):
        return obj.name_en
    else:
        return obj.name


@register.filter
def transleter_title(obj, lan):
    if lan.startswith('en'):
        return obj.title_en
    else:
        return obj.title


@register.filter
def transleter_description(obj, lan):
    if lan.startswith('en'):
        return obj.description_en
    else:
        return obj.description


@register.filter
def transleter_text(obj, lan):
    if lan.startswith('en'):
        return obj.text_en
    else:
        return obj.text


