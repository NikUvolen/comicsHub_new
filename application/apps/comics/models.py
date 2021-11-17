from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe
from utils import upload_function, upload_comics_images
from django.core.validators import FileExtensionValidator

from django.db import models


class IP(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Comics(models.Model):

    title = models.CharField(max_length=150, verbose_name='Title')
    slug = AutoSlugField(populate_from='title', verbose_name='Comics url')
    description = models.TextField(max_length=512, null=True, blank=True, verbose_name='Description')
    is_complete = models.BooleanField(default=False, verbose_name='Is complete')
    unique_views = models.ManyToManyField(IP, related_name='post_views', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    preview_image = models.ImageField(
        upload_to=upload_function, verbose_name='Edit preview image',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])]
    )

    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, verbose_name='Author')

    def __str__(self):
        return f'{self.title} | from {self.author.username}'

    def total_unique_views(self):
        return self.unique_views.count()

    def get_absolute_url(self):
        return reverse('view_comics', kwargs={'comics_slug': self.slug})

    def get_preview_image(self):
        return mark_safe(f'<img src="{self.preview_image.url}" width="auto" height="130">')
    get_preview_image.short_description = 'Preview image'

    class Meta:
        verbose_name = 'Comic book'
        verbose_name_plural = 'Comics'
        ordering = ['-created_at']


class Images(models.Model):

    image = models.ImageField(
        upload_to=upload_comics_images, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])]
    )

    comics_id = models.ForeignKey(Comics, on_delete=models.CASCADE, verbose_name='Comics id')

    def __str__(self):
        return f'image | from comics {self.comics_id.slug}'

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="150">')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
