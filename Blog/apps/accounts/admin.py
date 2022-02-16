from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserLoginForm, CustomUserChangeForm
from .models import User

from modeltranslation.admin import TranslationAdmin


class CustomUserAdmin(TranslationAdmin, UserAdmin):
    add_form = CustomUserLoginForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields':
                ('first_name', 'last_name', 'phone_number', 'photo', 'img_alt', 'subscription')
                }),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
