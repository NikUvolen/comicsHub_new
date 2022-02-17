from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import views
from django.shortcuts import get_object_or_404
from .models import User, Profile
from comics.models import Comics, LikesDislikes

from .forms import UserUpdateForm, ProfileUpdateForm


class UserProfile(views.View):

    def get(self, request, username, *args, **kwargs):
        user_profile = get_object_or_404(User, username=username)
        user_comics = Comics.objects.prefetch_related('unique_views', 'like_dislikes').filter(author=user_profile)
        comics_quantity = user_comics.count()

        context = {
            'user_profile': user_profile,
            'user_comics': user_comics,
            'comics_col': comics_quantity,
        }
        return render(request, 'users/profile.html', context=context)


@login_required
def profile(request):
    user_profile = get_object_or_404(Profile, user_id=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    print(user_profile)
    print(user_form)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    context = {
        'user_avatar_url': request.user.avatar,
        'username': request.user.username
    }

    print(context['user_avatar_url'])

    return render(request, 'users/update_users_data.html', context=context)
