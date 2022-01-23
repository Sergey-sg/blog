from django.core.validators import RegexValidator
from django.db import models

from .constans import target_const, position_const
from shared.mixins.model_utils import DragDropMixins


class Menu(DragDropMixins):
    title = models.CharField(max_length=100, unique=True)
    url_regex = RegexValidator(
        regex=r'^((http(s)?:\/\/)?([\w-]+\.?)+[\w-]+[.com]+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)',
        message='If the link is internal it should look like this: "blog/article/", for external links it should look'
                ' like this: "https://site.com/"')
    item_url = models.CharField(validators=[url_regex], unique=True, max_length=2048, help_text='Enter link address')
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

    def __str__(self):
        """class method returns the phone number of company in string representation"""
        return self.title

    class Meta(object):
        verbose_name = 'menu item'
        verbose_name_plural = 'Menu items'
        ordering = ['dd_order', 'created']
