# Generated by Django 3.2.9 on 2021-12-07 14:28

import django.core.validators
from django.db import migrations, models
import utils.uploading


class Migration(migrations.Migration):

    dependencies = [
        ('users_profiles', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=utils.uploading.upload_user_avatars_func, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])]),
        ),
    ]