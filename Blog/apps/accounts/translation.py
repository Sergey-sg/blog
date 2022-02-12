from modeltranslation.translator import translator, TranslationOptions
from .models import User


class UserTranslationOptions(TranslationOptions):
    fields = ('img_alt',)


translator.register(User, UserTranslationOptions)
