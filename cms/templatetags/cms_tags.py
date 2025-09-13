from django import template

register = template.Library()

@register.filter(name='split_string')
def split_string(value, delimiter=','):
    """
    Split a string by delimiter and return a list of stripped items.
    If the value is None or empty, return an empty list.
    """
    if value is None or value == '':
        return []
    return [item.strip() for item in value.split(delimiter)]

@register.filter(name='split')
def split(value, delimiter=' '):
    """
    Split a string by delimiter and return a list of items.
    If the value is None or empty, return an empty list.
    """
    if value is None or value == '':
        return []
    return value.split(delimiter)

@register.filter(name='strip')
def strip(value):
    """
    Strip whitespace from the beginning and end of a string.
    If the value is None, return an empty string.
    """
    if value is None:
        return ''
    return value.strip()