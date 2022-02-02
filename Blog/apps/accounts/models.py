from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from shared.mixins.model_utils import ImageNameMixins


class User(AbstractUser, ImageNameMixins):
    username = None
    email = models.EmailField(_('email адрес'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+380\d{9}',
        message=_('Номер телефона должен быть в формате: "+380999999999". Начинается из "+380" и 9 цифр.')
    )
    phone_number = models.CharField(validators=[phone_regex], unique=True, max_length=13, null=True, blank=True,
                                    help_text=_('Номер телефона должен быть в формате: "+380999999999"'))
    photo = models.ImageField(upload_to='user_photo/%Y/%m/%d', null=True, blank=True, help_text=_("Фото профиля"))
    img_alt = models.CharField(max_length=200, null=True, blank=True,
                               help_text=_('текст, который будет загружен в случае потери изображения'))
    # subscription = models.ManyToManyField('self', symmetrical=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['email']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
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
