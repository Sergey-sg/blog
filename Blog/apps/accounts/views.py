from typing import Any, Union

from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _

from django.views.generic import UpdateView, CreateView, ListView, TemplateView, FormView
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomRegistrationForm, UserPhotoChangeForm
from .tokens import account_activation_token
from ..blog.models import Article


class UserChangeView(LoginRequiredMixin, UpdateView):
    """
    Displays and processes the change user page
    """
    template_name = 'registration/change_user.jinja2'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None) -> object:
        """return object of User for the current user"""
        return get_user_model().objects.get(pk=self.request.user.pk)

    def get_success_url(self) -> str:
        """return url address for personal area"""
        return reverse_lazy('personal-area')


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Custom password change for users
    """
    template_name = 'registration/password_change.jinja2'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None) -> object:
        """return object of User for the current user"""
        user = self.request.user.pk
        return get_user_model().objects.get(pk=user)

    def get_success_url(self):
        """return url address for personal area"""
        return reverse_lazy('personal-area')


class CustomLoginView(LoginView):
    """Login view with form for create new user"""
    template_name = 'registration/login.jinja2'

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """return form for login and create new user"""
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context['create_user_form'] = CustomUserCreationForm()
        return context


class UserCreateView(CreateView):
    """Displays and processes the new user page"""
    model = get_user_model()
    template_name = 'registration/create_user.jinja2'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('confirm_registration')

    def form_valid(self, form: CustomRegistrationForm, *args: Any, **kwargs: dict[str, Any]) -> HttpResponseRedirect:
        """saves the user with the inactive status and sends an email message to confirm the identity"""
        user = form.save(commit=False)
        user.save()
        to_email = user.email
        current_site = get_current_site(self.request)
        mail_subject = _('Activating your account')
        message = render_to_string(
            'registration/msg.html',
            {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        send_mail(
            mail_subject,
            from_email=settings.EMAIL_HOST_USER,
            message=_('link to confirm email and complete registration'),
            recipient_list=[to_email],
            html_message=message,
        )
        return super(UserCreateView, self).form_valid(form)


class ActivateAccount(FormView):
    """Checks uidb64 and token for activate user"""

    def dispatch(self, request, *args, **kwargs) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse]:
        """Checks uidb64 and token for authenticity and, if successful, activates the user"""
        uidb64 = kwargs['uid']
        token = kwargs['token']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except Exception:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')


class ConfirmRegistrationView(TemplateView):
    """Displays a successful registration page"""
    template_name = 'registration/confirm_email_message_done.jinja2'


class PersonalArea(LoginRequiredMixin, ListView):
    """
    Personal area for current user
    """
    template_name = 'registration/profile.jinja2'
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Article]:
        articles = Article.objects.filter(author=self.request.user).only(
            'slug', 'title', 'short_description', 'average_rating')
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PersonalArea, self).get_context_data(**kwargs)
        context['user_photo_form'] = UserPhotoChangeForm(instance=self.request.user)
        return context
