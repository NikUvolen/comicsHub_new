import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.filter(email=email).first()
        print(user.check_password(password))
        if (not user) or (not user.check_password(password)):
            raise forms.ValidationError('Email or password is wrong')

        return self.cleaned_data


class BaseUpdateForm(forms.ModelForm):

    def is_valid(self, *args, **kwargs):
        result = super().is_valid()
        for x in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' ' + 'is-invalid'})
        return result


class UserUpdateForm(BaseUpdateForm):

    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            raise forms.ValidationError('The user name cannot be empty')

        match = re.match('^[a-zA-Z0-9_]+$', username)

        if match is None:
            error_string = 'The username contains invalid characters. Only "a-z, A-Z, 0-9, _" is available.'
            raise forms.ValidationError(error_string)

        return username

    class Meta:
        model = User
        fields = ['username', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'textinput textInput form-control'})
        }


class ProfileUpdateForm(BaseUpdateForm):
    status = forms.Textarea()

    class Meta:
        model = Profile
        fields = ['status', 'sex', 'birthday', 'first_name', 'last_name']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'sex': forms.Select(attrs={'class': 'select form-control'}),
            'birthday': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'textinput textInput form-control'}),
        }
