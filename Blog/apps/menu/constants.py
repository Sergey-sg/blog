from django.db import models


class Target(models.TextChoices):
    _blank = ('b', '_blank')
    _self = ('s', '_self')


class Position(models.TextChoices):
    header = ('h', 'header')
    footer = ('f', 'footer')
