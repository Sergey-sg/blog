from django.db import models


class Target(models.TextChoices):
    BLANK = ('_blank', 'blank')
    SELF = ('_self', 'self')


class Position(models.TextChoices):
    HEADER = ('h', 'header')
    FOOTER = ('f', 'footer')
