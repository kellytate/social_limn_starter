from django import template

register = template.Library()

@register.filter
def tuple_to_array(tuple):
    return list(tuple)