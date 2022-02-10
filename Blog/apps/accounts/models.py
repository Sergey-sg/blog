from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from shared.validators.validators import PHONE_REGEX
from .managers import CustomUserManager
from shared.mixins.model_utils import ImageNameMixins


class User(AbstractUser, ImageNameMixins):
    """
    User model
        attributes:
             email (str): used to log in the site
             phone_number (str): User phone number
             photo (img): article preview image
             img_alt (str): text to be loaded in case of image loss
             subscription (class User): author subscription
    """
    username = None
    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('used to login the site'),
        unique=True,
    )
    phone_number = models.CharField(
        validators=[PHONE_REGEX],
        unique=True, max_length=13,
        null=True,
        blank=True,
        verbose_name=_('phone number'),
        help_text=_('The phone number must be in the format: "+380999999999"')
    )
    photo = models.ImageField(
        upload_to='user_photo/%Y/%m/%d',
        null=True, blank=True,
        verbose_name=_('photo'),
        help_text=_("Profile photo")
    )
    img_alt = models.CharField(
        max_length=200,
        null=True, blank=True,
        verbose_name=_('image alternative'),
        help_text=_('text to be loaded in case of image loss')
    )
    subscription = models.ManyToManyField(
        'self',
        verbose_name=_('subscription'),
        help_text=_('author subscription'),
        symmetrical=False,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')
        ordering = ['email']

    def __str__(self) -> str:
        """class method returns the user in string representation"""
        return self.email

    def save(self, *args, **kwargs) -> None:
        """checks for a user photo and changes it renames the user photo"""
        if self.photo:
            if self.pk:
                orig = User.objects.get(pk=self.pk)
                if orig.photo.name != self.photo.name:
                    if self.photo:
                        self.photo.name = self.get_image_name(name=self.email, filename=self.photo.name)
                        if not self.img_alt:
                            self.img_alt = f'photo {self.email} user'
            else:
                self.photo.name = self.get_image_name(name=self.email, filename=self.photo.name)
                if not self.img_alt:
                    self.img_alt = f'photo {self.email} user'
        super(User, self).save(*args, **kwargs)
