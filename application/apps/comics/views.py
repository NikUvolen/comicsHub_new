from django import views
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Comics, Images, IP
from users_profiles.models import User


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ComicsViewPage(views.View):

    def get(self, request, *args, **kwargs):
        comics = Comics.objects.prefetch_related('unique_views').all()
        context = {
            'comics': comics
        }
        return render(request, 'comics/comics_view_page.html', context=context)


class DetailComicsView(views.View):

    def get(self, request, slug, *args, **kwargs):
        comics_values = ('title', 'description', 'preview_image', 'tags')
        author_values = ('username', 'avatar')
        comics = get_object_or_404(Comics, slug=slug)
        author = comics.author
        images = Images.objects.filter(comics_id=comics.pk)

        ip = get_client_ip(self.request)
        if not IP.objects.filter(ip=ip).exists():
            IP.objects.create(ip=ip)
        comics.unique_views.add(IP.objects.get(ip=ip))

        context = {
            "detail_comics": comics,
            "author": author,
            'images': images
        }
        return render(request, 'comics/detail_comics_view.html', context=context)

