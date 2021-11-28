from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from taggit.models import CommonGenericTaggedItemBase

from .models import Comics, Images, LikesDislikes
from .forms import AtLeastOneFormSet


class ImagesInLine(admin.TabularInline):

    model = Images
    readonly_fields = ('image_url',)
    formset = AtLeastOneFormSet


class ComicsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'is_complete', 'total_unique_views', 'get_preview_image')
    list_display_links = ('id', 'title', 'get_preview_image')
    search_fields = ('id', 'title')
    list_editable = ('is_complete',)
    list_filter = ('is_complete',)
    fields = (
        'title', 'description', 'is_complete', 'get_preview_image', 'preview_image',
        'tags', 'created_at', 'updated_at', 'author'
    )
    readonly_fields = ('get_preview_image', 'created_at', 'updated_at')

    inlines = [ImagesInLine]


admin.site.register(Comics, ComicsAdmin)
admin.site.register(LikesDislikes)
