from modeltranslation.translator import translator, TranslationOptions
from .models import Menu


class MenuTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Menu, MenuTranslationOptions)
