from django.db import models
from django.utils.translation import ugettext_lazy as _


class Status(models.TextChoices):
    """CHOICES:
        PUBLISHED, BLOCKED
    """
    PUBLISHED = ('p', _('published'))
    BLOCKED = ('b', _('blocked'))


class ScoreChoices(models.IntegerChoices):
    """CHOICES:
        ONE, TWO, TREE, FOUR, FIVE
    """
    ONE = (1, '1')
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
