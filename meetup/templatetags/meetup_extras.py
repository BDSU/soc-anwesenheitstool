from django import template
from django.conf import settings
from django.urls import reverse

register = template.Library()


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


# https://stackoverflow.com/a/19024649
@register.simple_tag(takes_context=True)
def abs_url(context, view_name, *args, **kwargs):
    return context['request'].build_absolute_uri(
        reverse(view_name, args=args, kwargs=kwargs)
    )
