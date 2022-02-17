from django import forms
from django.contrib.auth.models import User

from .models import User, Profile


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'avatar']


class ProfileUpdateForm(forms.ModelForm):
    status = forms.Textarea()

    class Meta:
        model = Profile
        fields = ['status', 'sex', 'birthday', 'first_name', 'last_name']
