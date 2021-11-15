from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile

USER = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_login', 'avatar_url')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'username')
    fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'last_login', 'date_joined')
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(USER, UserAdmin)
admin.site.register(Profile)
