from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shared.validators.validators import URL_REGEX
from .constants import Target, Position
from shared.mixins.model_utils import DragDropMixins


class Menu(DragDropMixins):
    """
        Menu model
        attributes:
             title (str): title (name) of url item;
             item_url (str): url address
             target (str): target for link (self or blank)
             position (str): position in menu (header or footer)
             show_item (bool): show or hidden item of menu
             created (datetime): date of created item
             updated (datetime): date of last update item
             dd_order (int): used to drag and drop items in the admin
    """

    title = models.CharField(max_length=100, unique=True, verbose_name=_('title'))
    item_url = models.CharField(
        validators=[URL_REGEX],
        unique=True, max_length=2048,
        help_text=_('Enter link address'),
        verbose_name=_('url address')
    )
    target = models.CharField(
        max_length=6,
        choices=Target.choices,
        default=Target.SELF,
        help_text=_('Target url'),
        verbose_name=_('target')
    )
    position = models.CharField(
        max_length=1,
        choices=Position.choices,
        help_text=_('Position object (header or footer)'),
        verbose_name=_('position')
    )
    show_item = models.BooleanField(
        verbose_name=_('show'),
        help_text=_('show or hidden url address'),
        default=False
    )

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')
        ordering = ['dd_order', 'created']

    def __str__(self) -> str:
        """class method returns the menu item in string representation"""
        return self.title

    def save(self, *args, **kwargs) -> None:
        """class method checks if there is a domain in the internal link,
           if the domain is missing then adds it
        """
        if self.target == Target.SELF:
            domain = Site.objects.get_current().domain
            if domain not in self.item_url:
                self.item_url = f'{domain}/{self.item_url}'
        super(Menu, self).save(*args, **kwargs)
