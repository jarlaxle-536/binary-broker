# coding=utf-8
from django.template import Library

register = Library()

@register.filter
def get_from_dict(dictionary, key):
    return dictionary.get(key)
