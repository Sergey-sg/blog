from django.db import models

from .constans import target_const, position_const


class Menu(models.Model):
    title = models.CharField(max_length=100, unique=True)
    item_url = models.CharField(max_length=2048)
    target = models.CharField(
        max_length=1,
        choices=target_const,
        default='s',
        help_text='Target url'
    )
    position = models.CharField(
        max_length=1,
        choices=position_const,
        help_text='Position object (header or footer)'
    )
    show_item = models.BooleanField('show', default=False)
    created = models.DateTimeField(auto_now_add=True)
