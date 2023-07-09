from django import template

register = template.Library()

@register.simple_tag()
def get_topic_active(topic, params: dict):
    return 'active' if topic.pk == int(params.get('topic', 1)) else ''
