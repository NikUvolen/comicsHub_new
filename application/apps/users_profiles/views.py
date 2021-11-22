from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django import views
from django.shortcuts import get_object_or_404
from .models import User
from comics.models import Comics


class UserProfile(views.View):

    def get(self, request, username, *args, **kwargs):
        user_profile = get_object_or_404(User, username=username)
        user_comics = Comics.objects.prefetch_related('unique_views').filter(author=user_profile)
        comics_col = user_comics.count()
        context = {
            'user_profile': user_profile,
            'user_comics': user_comics,
            'comics_col': comics_col
        }
        return render(request, 'profile.html', context=context)
