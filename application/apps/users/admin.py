from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile


user = get_user_model()


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'last_login', 'avatar_url')
    list_display_links = ('id', 'username')
    search_fields = ('id', 'username')
    fields = ('username', 'email', 'avatar', 'last_login', 'date_joined', 'is_verified', 'is_active', 'last_online')
    readonly_fields = ('email', 'last_login', 'date_joined')


admin.site.register(user, UserAdmin)
admin.site.register(Profile)
