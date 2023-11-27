from django import template
from django.contrib.auth.models import Permission, User, Group

register = template.Library()


@register.simple_tag
def group_has_permission(group_name, codename):
    if Permission.objects.filter(group__name=group_name, codename=codename).exists():
        return "checked"
    else:
        return ""
