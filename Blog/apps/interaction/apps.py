from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InteractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interaction'
    verbose_name = _('Interaction')
