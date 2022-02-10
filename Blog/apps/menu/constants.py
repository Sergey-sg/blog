from django.db import models
from django.utils.translation import ugettext_lazy as _


class Target(models.TextChoices):
    BLANK = ('_blank', _('blank'))
    SELF = ('_self', _('self'))


class Position(models.TextChoices):
    HEADER = ('h', _('header'))
    FOOTER = ('f', _('footer'))
