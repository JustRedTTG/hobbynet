from django import template

register = template.Library()

@register.simple_tag()
def dir(formI):
    return formI
