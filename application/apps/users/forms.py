from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'avatar']


class ProfileUpdateForm(forms.ModelForm):
    status = forms.Textarea()

    class Meta:
        model = Profile
        fields = ['status', 'sex', 'birthday', 'first_name', 'last_name']
