from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from django.views.generic import UpdateView, CreateView, ListView, TemplateView, FormView
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomRegistrationForm
from .tokens import account_activation_token
from ..blog.forms import ArticleForm
from ..blog.models import Article


class UserChangeView(UpdateView):
    """
    Custom user change for users
    """
    template_name = 'registration/change_user.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('personal-area')


class MyPasswordChangeView(PasswordChangeView):
    """
    Custom password change for users
    """
    template_name = 'registration/password_change.html'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None):
        user = self.request.user.pk
        return get_user_model().objects.get(pk=user)

    def get_success_url(self):
        return reverse_lazy('personal-area')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context['create_user_form'] = CustomUserCreationForm()
        return context


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = 'registration/create_user.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('confirm_registration')

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        user.save()
        to_email = user.email
        current_site = get_current_site(self.request)
        mail_subject = _('Активация вашего аккаунта')
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
            message=_('ссылка для подтверждения почты и завершения регистрации'),
            recipient_list=[to_email],
            html_message=message,
        )
        return super(UserCreateView, self).form_valid(form)


class ActivateAccount(FormView):

    def dispatch(self, request, *args, **kwargs):
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
    template_name = 'registration/confirm_email_message_done.html'


class PersonalArea(ListView):
    """
    Personal area for current user
    """
    template_name = 'registration/profile.html'
    paginate_by = 8

    def get_queryset(self):
        articles = Article.objects.filter(author=self.request.user).only(
            'slug', 'title', 'short_description', 'average_rating')
        return articles
