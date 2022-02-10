from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

URL_REGEX = RegexValidator(
        regex=r'^((http(s)?:\/\/)?([\w-]+\.?)+[\w-]+[.com]*([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)',
        message=_('If the link is internal it should look like this: "blog/article/", for external links it should look'
                  ' like this: "https://www.site.com/"')
)

PHONE_REGEX = RegexValidator(
        regex=r'^\+380\d{9}',
        message=_('The phone number must be in the format: "+380999999999". Starts with "+380" and 9 digits.')
)
