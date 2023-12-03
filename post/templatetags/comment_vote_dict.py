from django import template

register = template.Library()

@register.filter
def from_dict(d, k):
    return d[k]