import json

from django import views
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from users.templatetags import include_tags
from .models import Comics, Images, IP, Comments
from .forms import AddComicsForm, AddCommentForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def delete_comment(request, pk):
    pass


class MainPage(views.View):

    def get(self, request, *args, **kwargs):
        comics = Comics.objects.prefetch_related('unique_views').select_related('author').all()
        results = []
        tt = []

        for book in range(0, len(comics)):
            tt.append(comics[book])
            if len(tt) == 4:
                results.append(tt.copy())
                tt.clear()
        else:
            results.append(tt.copy())
            tt.clear()

        return render(request, 'comics/main_page.html', context={'comics': results})


# def add_comment(request, comics_slug):
#     if request.method == 'POST':
#         leave_comment_form = AddCommentForm(request.POST)
#         if leave_comment_form.is_valid():
#             comment = leave_comment_form.cleaned_data['comment_text']
#
#             Comments.add_root(
#                 from_comics=get_object_or_404(Comics, slug=comics_slug),
#                 author=request.user,
#                 comment=comment
#             )
#
#             json_response = {
#                 'username': request.user.username,
#                 'user_avatar': include_tags.get_avatar_or_default(request.user.avatar),
#                 'comment_text': comment,
#             }
#
#             return JsonResponse(json_response, safe=False)
#         return HttpResponse(str(leave_comment_form.errors))


class DetailViewComics(views.View):

    @staticmethod
    def add_unique_view_on_comics(request, comics):
        ip = get_client_ip(request)
        if not IP.objects.filter(ip=ip).exists():
            IP.objects.create(ip=ip)
        comics.unique_views.add(IP.objects.get(ip=ip))

    def get(self, request, comics_slug, *args, **kwargs):
        comics = get_object_or_404(Comics, slug=comics_slug)
        images = Images.objects.filter(comics_id=comics)
        creator = comics.author

        comments = Comments.get_root_nodes().select_related('author').filter(from_comics=comics).order_by('-pub_date')
        total_comments = Comments.count_comments(comics)

        self.add_unique_view_on_comics(self.request, comics)

        leave_comment_form = AddCommentForm()

        context = {
            'comics': comics,
            'images': images,
            'creator': creator,
            'comments': comments,
            'total_comments': total_comments,
            'leave_comment_form': leave_comment_form
        }

        return render(request, 'comics/detail_comics_view.html', context=context)

    def post(self, request, comics_slug):
        leave_comment_form = AddCommentForm(request.POST)
        if leave_comment_form.is_valid():
            comment = leave_comment_form.cleaned_data['comment_text']

            user_comment = Comments.add_root(
                from_comics=get_object_or_404(Comics, slug=comics_slug),
                author=request.user,
                comment=comment
            )

            json_response = {
                'username': request.user.username,
                'user_avatar': include_tags.get_avatar_or_default(request.user.avatar),
                'comment_text': comment,
                'pub_date': user_comment.pub_date.strftime("%d %B %Y, %H:%M")
            }

            return JsonResponse(json_response, safe=False)
        return HttpResponse(str(leave_comment_form.errors))


class UserComics(views.View):

    def get(self, request, comics_slug, *args, **kwargs):
        pass


class AddComics(views.View):

    def get(self, request, *args, **kwargs):
        add_comics_form = AddComicsForm()
        context = {
            'add_comics_form': add_comics_form
        }
        return render(request, 'comics/add_comics.html', context=context)

    def post(self, request, *args, **kwargs):
        add_comics_form = AddComicsForm(request.POST, request.FILES)

        if add_comics_form.is_valid():
            images = request.FILES.getlist('images')

            if len(images) < 1:
                add_comics_form.errors['images'] = add_comics_form.error_class(['Image count < 1'])
                raise ValidationError('Image count < 1')

            add_comics_form = add_comics_form.save(commit=False)
            add_comics_form.author = request.user
            add_comics_form.save()

            for image in images:
                Images.objects.create(
                    comics_id=add_comics_form,
                    image=image
                )

            messages.success(request, "Yeeew, check it out on the home page!")
            return redirect('view_comics', add_comics_form.slug)

        context = {
            'add_comics_form': add_comics_form
        }
        return render(request, 'comics/add_comics.html', context=context)
