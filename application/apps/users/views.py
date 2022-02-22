from django import views
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from comics.models import Comics
from .forms import CustomUserCreationForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


User = get_user_model()
error_css_class = 'is-valid'


class UserRegistration(views.View):

    @staticmethod
    def context(user_form):
        return {'user_form': user_form}

    def get(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm()
        return render(request, 'users/registration.html', context=self.context(user_form))

    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST or None)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['username']
            new_user.email = user_form.cleaned_data['email']
            new_user.user_profile = Profile.objects.create()
            new_user.save()
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password1'])
            login(request, user)
            return redirect('main_page')

        return render(request, 'users/registration.html', context=self.context(user_form))


class UserLogin(views.View):

    @staticmethod
    def context(user_form):
        return {'user_form': user_form}

    def get(self, request, *args, **kwargs):
        user_form = LoginForm()
        return render(request, 'users/authentication.html', context=self.context(user_form))

    def post(self, request, *args, **kwargs):
        user_form = LoginForm(request.POST or None)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('main_page')

        return render(request, 'users/authentication.html', context=self.context(user_form))


class EditProfile(views.View):

    @staticmethod
    def context(user_form, profile_form):
        return {'user_form': user_form, 'profile_form': profile_form}

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)
        return render(request, 'users/user_edit_profile.html', context=self.context(user_form, profile_form))

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', pk=request.user.pk)

        return render(request, 'users/user_edit_profile.html', context=self.context(user_form, profile_form))


class UserProfile(views.View):

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user_profile = user.user_profile

        comics = Comics.objects.prefetch_related('unique_views').filter(author=user)
        if not comics.exists():
            comics = None

        context = {
            'user': user,
            'user_profile': user_profile,
            'comics': comics
        }
        return render(request, 'users/user_profile.html', context=context)

