from django import views
from django.shortcuts import render
from django.http import HttpResponse

from .models import Comics

#
# class BaseView(views.View):
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'base.html', {})


class ComicsViewPage(views.View):

    def get(self, request, *args, **kwargs):
        comics = Comics.objects.prefetch_related('unique_views').all()
        context = {
            'comics': comics
        }
        return render(request, 'comics/comics_view_page.html', context=context)
