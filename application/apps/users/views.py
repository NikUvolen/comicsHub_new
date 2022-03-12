import random
import threading

from django import views
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from comics.models import Comics
from .forms import CustomUserCreationForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from .utils import generate_token


User = get_user_model()
error_css_class = 'is-valid'


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, you can login!')
        return redirect(reverse('user_authentication'))

    return render(request, 'users/activation-failed.html', {'user': user})


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


class UserRegistration(views.View):

    @staticmethod
    def generate_code():
        random.seed()
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_activation_email(request, user):
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        email_body = render_to_string('users/activate.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email = EmailMessage(
            subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user.email]
        )
        EmailThread(email).start()

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
            new_user.save()
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()

            self.send_activation_email(request, new_user)

            messages.add_message(request, messages.SUCCESS, 'To enter, you have to confirm your email. Check your email')

            return render(request, 'users/verificate_email.html')

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

            if not user.is_verified:
                messages.add_message(request, messages.ERROR, 'Email is not verified, please check your email')
                return render(request, 'users/authentication.html', context=self.context(user_form))

            if user:
                if not Profile.objects.filter(user=user).exists():
                    Profile.objects.create(user=user)

                login(request, user)
                return redirect('main_page')

        return render(request, 'users/authentication.html', context=self.context(user_form))


class EditProfile(views.View):

    @staticmethod
    def context(user_form, profile_form):
        return {'user_form': user_form, 'profile_form': profile_form}

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=Profile.objects.get(user=request.user))
        return render(request, 'users/user_edit_profile.html', context=self.context(user_form, profile_form))

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=Profile.objects.get(user=request.user))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', pk=request.user.pk)

        return render(request, 'users/user_edit_profile.html', context=self.context(user_form, profile_form))


class UserProfile(views.View):

    @staticmethod
    def count_all_views(comics):
        comics_views = 0
        for comic_book in comics:
            comics_views += comic_book.unique_views.count()
        return comics_views

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user_profile = Profile.objects.get(user=user)

        comics = Comics.objects.prefetch_related('unique_views').filter(author=user)

        if not comics.exists():
            comics = None
            comics_count = 0
            comics_views = 0
        else:
            comics_count = comics.count()
            comics_views = self.count_all_views(comics)

        context = {
            'user': user,
            'user_profile': user_profile,
            'comics': comics,
            'comics_count': comics_count,
            'comics_views': comics_views
        }
        return render(request, 'users/user_profile.html', context=context)

