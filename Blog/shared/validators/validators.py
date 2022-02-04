from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

URL_REGEX = RegexValidator(
        regex=r'^((http(s)?:\/\/)?([\w-]+\.?)+[\w-]+[.com]+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)',
        message='If the link is internal it should look like this: "blog/article/", for external links it should look'
                ' like this: "https://site.com/"')

PHONE_REGEX = RegexValidator(
        regex=r'^\+380\d{9}',
        message=_('Номер телефона должен быть в формате: "+380999999999". Начинается из "+380" и 9 цифр.')
    )
