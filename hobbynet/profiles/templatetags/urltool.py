from django import template

register = template.Library()

@register.filter
def query_string(value, arg):
    return f"{value}&{arg}"

@register.simple_tag(takes_context=True)
def add_query_param(context, url, key, value):
    query_params = context['request'].GET.copy()
    query_params[key] = value
    query_string = query_params.urlencode()
    return f"{url}?{query_string}"
