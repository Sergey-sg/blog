from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password',)


# class CustomLoginForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = ('email', 'password',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'photo', 'img_alt')


class CustomRegistrationForm(UserCreationForm):
    is_active = False

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'is_active')
