import json

from django import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import AddComicsForm
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
        comics = Comics.objects.prefetch_related('unique_views').all().only(
            'title', 'description', 'preview_image', 'slug'
        )
        context = {
            'comics': comics
        }
        return render(request, 'comics/comics_view_page.html', context=context)


class DetailComicsView(views.View):

    @staticmethod
    def _get_comics_or_404(slug):
        try:
            comics = Comics.objects.prefetch_related(
                Prefetch('author', queryset=User.objects.all().only('username', 'avatar')),
                # 'comics__images',
                # Prefetch('comics__images', queryset=Images.objects.all())
            ).only('title', 'description', 'tags').get(slug=slug)
        except Comics.DoesNotExist:
            return HttpResponseNotFound("404. Page not found")
        return comics

    def get(self, request, slug, *args, **kwargs):
        comics_values = ('title', 'description', 'preview_image', 'tags')
        author_values = ('username', 'avatar')
        comics = self._get_comics_or_404(slug)
        images = Images.objects.filter(comics_id=comics.pk).only('image')

        likes_dislikes = comics.like_dislikes
        likes = likes_dislikes.likes().count()
        dislikes = likes_dislikes.dislikes().count()

        ip = get_client_ip(self.request)
        if not IP.objects.filter(ip=ip).exists():
            IP.objects.create(ip=ip)
        comics.unique_views.add(IP.objects.get(ip=ip))

        context = {
            "detail_comics": comics,
            'images': images,
            'likes': likes,
            'dislikes': dislikes,
        }
        return render(request, 'comics/detail_comics_view.html', context=context)


class VoteView(views.View):

    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)

        # TODO: решить проблему "лайкодрочерства" и фризе кнопки лайкоов

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


# class AddComicsView(views.View):
#
#     ImageFormSet = modelformset_factory(Images, form=AddComicsImages)
#
#     def get(self, request, *args, **kwargs):
#         comicsForm = AddComicsForm()
#         formset = self.ImageFormSet(queryset=Images.objects.none())
#
#         context = {
#             'comicsForm': comicsForm,
#             'formset': formset
#         }
#         return render(request, 'comics/add_comics_view_page.html', context=context)
#
#     def post(self, request, *args, **kwargs):
#         # comics_formset = inlineformset_factory(Comics, Images, fields=('image',))
#         # creator = User.objects.get(username=request.user.username)
#         # formset = comics_formset(instance=creator)
#         comicsForm = AddComicsForm(request.POST)
#         formset = self.ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
#
#         if comicsForm.is_valid() and formset.is_valid():
#             comics_form = comicsForm.save(commit=False)
#             comics_form.author = request.user
#             comics_form.save()
#
#             for form in formset.cleaned_data:
#                 if form:
#                     image = form['image']
#                     photo = Images(comics_id=comics_form, image=image)
#                     photo.save()
#
#             messages.success(request, "Yeeew, check it out on the home page!")
#             return redirect('detail_comics_view', comics_form.slug)


@login_required(redirect_field_name='login')
def add_comics(request):
    if request.method == 'POST':
        comicsForm = AddComicsForm(request.POST, request.FILES)

        if comicsForm.is_valid():
            images = request.FILES.getlist('images')

            if len(images) < 1:
                raise ValidationError('Image count < 1')

            comics_form = comicsForm.save(commit=False)
            comics_form.author = request.user
            comics_form.save()

            for image in images:
                Images.objects.create(
                    comics_id=comics_form,
                    image=image
                )

            messages.success(request, "Yeeew, check it out on the home page!")
            return redirect('detail_comics_view', comics_form.slug)
        else:
            errors = ''
            for err in comicsForm.errors:
                errors += f'\n {comicsForm.errors[err]}'

            return HttpResponse(errors)
    else:
        comicsForm = AddComicsForm()

        context = {
            'comicsForm': comicsForm,
        }
        return render(request, 'comics/add_comics_view_page.html', context=context)
