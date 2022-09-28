from django import template

register = template.Library()


@register.filter
def get_class_name(instance):
    """Return the class name of an instance"""
    return instance.__class__.__name__
