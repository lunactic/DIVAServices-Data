from django import template

register = template.Library()

@register.filter(is_safe=True)
def index(sequence, position):
    return sequence[position]