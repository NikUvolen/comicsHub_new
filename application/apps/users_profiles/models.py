from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.safestring import mark_safe

from utils import upload_user_avatars_func


class Profile(models.Model):
    """Profile user model"""

    SEX_USER_CHOICES = [
        (0, 'Male'),
        (1, 'Female')
    ]

    status = models.CharField(max_length=140, null=True, blank=True)
    sex = models.BooleanField(choices=SEX_USER_CHOICES, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    user_id = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.user_id.username}'

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'Users profiles'


class User(AbstractUser):
    """Custom user model"""

    avatar = models.ImageField(upload_to=upload_user_avatars_func,
                               null=True,
                               blank=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])],
                               default=None)

    def __str__(self):
        return self.username

    def avatar_url(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" width="auto" height="120">')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
