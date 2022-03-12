from django import template
from django.templatetags.static import static
from django.utils import timezone

register = template.Library()


@register.simple_tag
def get_avatar_or_default(user_avatar):
    if user_avatar:
        return user_avatar.url
    else:
        return static('users/no-avatar.jpg')


@register.simple_tag
def get_online_status(user):
    if user.last_login:
        if (timezone.now() - user.last_login) < timezone.timedelta(seconds=35):
            return 'Online'
        return 'Offline'
    return 'Offline'

