from django import views
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect

from .models import Comics, Images
from .forms import AddComicsForm


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


class DetailViewComics(views.View):

    def get(self, request, comics_slug, *args, **kwargs):
        comics = get_object_or_404(Comics, slug=comics_slug)
        images = Images.objects.filter(comics_id=comics)
        return render(request, 'comics/detail_comics_view.html', context={'comics': comics, 'images': images})


class UserComics(views.View):

    def get(self, request, pk, *args, **kwargs):
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
