from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from users_profiles.models import User


register = template.Library()


@register.simple_tag
def get_avatar_or_default(user_avatar):
    if user_avatar:
        return user_avatar.url
    else:
        return static('users_profiles/no-avatar.jpg')
