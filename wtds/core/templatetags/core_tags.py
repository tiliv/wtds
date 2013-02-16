from operator import add, attrgetter

from django import template

register = template.Library()

@register.simple_tag
def combine_forms_media(*forms):
    return reduce(add, map(attrgetter('media'), filter(bool, forms)))
