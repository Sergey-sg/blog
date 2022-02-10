from django.db import models
from django.utils.translation import ugettext_lazy as _


class Published(models.TextChoices):
    """CHOICES:
            PUBLISHED, DRAFT
        """
    DRAFT = ('d', _('draft'))
    PUBLISHED = ('p', _('published'))
