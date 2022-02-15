from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Model form for create user"""
    class Meta:
        model = User
        fields = ('email', 'password',)


class CustomUserChangeForm(UserChangeForm):
    """Model form for update user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'photo', 'img_alt')


class CustomRegistrationForm(UserCreationForm):
    """Model form for create user"""
    is_active = False

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'is_active')


class UserPhotoChangeForm(UserChangeForm):
    """Model form for update user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'photo', 'img_alt')
        exclude = ('password',)

        widgets = {
                'first_name': forms.HiddenInput(),
                'last_name': forms.HiddenInput(),
                'phone_number': forms.HiddenInput(),
                'img_alt': forms.HiddenInput(),
        }
