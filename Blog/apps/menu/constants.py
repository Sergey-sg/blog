from django.db import models


class Target(models.TextChoices):
    BLANK = ('b', '_blank')
    SELF = ('s', '_self')


class Position(models.TextChoices):
    HEADER = ('h', 'header')
    FOOTER = ('f', 'footer')
