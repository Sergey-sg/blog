from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.menu'
    verbose_name = _('Menu')
