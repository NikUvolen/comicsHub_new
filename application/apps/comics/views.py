import json

from django import views
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import DetailView

from .models import Comics, Images, IP, LikesDislikes
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

    @staticmethod
    def _get_comics_or_404(slug):
        try:
            # author =
            comics = Comics.objects.select_related('author').get(slug=slug)
        except Comics.DoesNotExist:
            return HttpResponseNotFound("404. Page not found")
        return comics

    def get(self, request, slug, *args, **kwargs):
        comics_values = ('title', 'description', 'preview_image', 'tags')
        author_values = ('username', 'avatar')
        comics = self._get_comics_or_404(slug)
        images = Images.objects.filter(comics_id=comics.pk)

        likes_dislikes = comics.like_dislikes
        likes = likes_dislikes.likes().count()
        dislikes = likes_dislikes.dislikes().count()

        ip = get_client_ip(self.request)
        if not IP.objects.filter(ip=ip).exists():
            IP.objects.create(ip=ip)
        comics.unique_views.add(IP.objects.get(ip=ip))

        context = {
            "detail_comics": comics,
            'likes': likes,
            'dislikes': dislikes,
            'images': images
        }
        return render(request, 'comics/detail_comics_view.html', context=context)


class VoteView(views.View):

    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)

        # TODO: решить проблему "лайкодрочерства" и фризе кнопки лайкоов
        # TODO: сделать кэширование на странице

        try:
            like_dislike = LikesDislikes.objects.get(
                content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user
            )
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                like_dislike.delete()
                result = False
        except LikesDislikes.MultipleObjectsReturned:
            print('Durak?')
            result = False
        except LikesDislikes.DoesNotExist:
            obj.like_dislikes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.like_dislikes.likes().count(),
                "dislike_count": obj.like_dislikes.dislikes().count(),
            }),
            content_type="application/json"
        )
