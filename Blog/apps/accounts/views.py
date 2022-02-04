from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.views.generic import UpdateView, CreateView, ListView
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm


class UserChangeView(UpdateView):
    """
    Custom user change for users
    """
    template_name = 'accounts/change_user.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        user = self.request.user.pk
        return get_user_model().objects.get(pk=user)

    def get_success_url(self):
        return '/accounts/profile/'


class MyPasswordChangeView(PasswordChangeView):
    """
    Custom password change for users
    """
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None):
        user = self.request.user.pk
        return get_user_model().objects.get(pk=user)

    def get_success_url(self):
        return '/accounts/profile/'


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context['create_user_form'] = CustomUserCreationForm()
        return context


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = 'accounts/create_user.html'
    form_class = CustomUserCreationForm
    success_url = '/accounts/login/'


class PersonalArea(ListView):
    """
    Send to 'profile.html' companies, messages, projects which are user-created
    """
    template_name = 'accounts/profile.html'
    paginate_by = 2

    # def get_queryset(self):
    #     try:
    #         personal_object = self.request.GET['personal_object']
    #         if personal_object == 'companies':
    #             companies = Company.objects.filter(user=self.request.user.pk).order_by('-date_created')
    #             return companies
    #         elif personal_object == 'projects':
    #             projects = ProjectCompany.objects.filter(user=self.request.user.pk).order_by('-created')
    #             return projects
    #         elif personal_object == 'comments':
    #             comments = Message.objects.filter(manager=self.request.user.pk).order_by('-created')
    #             return comments
    #     except Exception:
    #         return Company.objects.filter(user=self.request.user.pk).order_by('-date_created')

