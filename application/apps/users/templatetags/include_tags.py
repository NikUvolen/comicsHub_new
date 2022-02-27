from django import template
from django.templatetags.static import static


register = template.Library()


@register.simple_tag
def get_avatar_or_default(user_avatar):
    if user_avatar:
        return user_avatar.url
    else:
        return static('users/no-avatar.jpg')

