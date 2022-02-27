# Generated by Django 4.0.2 on 2022-02-25 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comics',
            name='description',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='comics',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Title'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('is_anonym', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=512)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name="Comment' date")),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('from_comics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comics.comics')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]