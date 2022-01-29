from django.db import models


class Status(models.TextChoices):
    PUBLISHED = ('p', 'published')
    BLOCKED = ('b', 'blocked')


class ScoreChoices(models.IntegerChoices):
    ONE = (1, '1')
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
