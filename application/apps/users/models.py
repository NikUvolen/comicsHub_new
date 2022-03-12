from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

from utils import upload_user_avatars_func
from .managers import CustomUserManager


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=20, unique=False, null=False, blank=True)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, null=False)
    avatar = models.ImageField(upload_to=upload_user_avatars_func,
                               null=True,
                               blank=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
                               default=None)

    is_verified = models.BooleanField('Verified', default=False)
    last_online = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @staticmethod
    def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

            img = self.crop_center(img, 120, 120)
            img.save(self.avatar.path)

    def avatar_url(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" width="auto" height="120">')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    """Profile user model"""

    SEX_USER_CHOICES = [
        (0, 'Male'),
        (1, 'Female')
    ]

    status = models.CharField(max_length=50, null=True, blank=True)
    sex = models.BooleanField(choices=SEX_USER_CHOICES, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.user}'

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'Users profiles'


class UserTokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
