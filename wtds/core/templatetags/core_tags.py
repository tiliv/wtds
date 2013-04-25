from operator import add, attrgetter

from django import template

register = template.Library()

@register.simple_tag
def combine_forms_media(*forms):
    media_list = map(attrgetter('media'), filter(bool, forms))
    if media_list:
        return reduce(add, media_list)
    return ""
