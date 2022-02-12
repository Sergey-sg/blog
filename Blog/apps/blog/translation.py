from modeltranslation.translator import translator, TranslationOptions
from .models import Category, TextPage, Article, ImageArticle


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class TextPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'img_alt', 'short_description', 'content',)


class ImageArticleTranslationOptions(TranslationOptions):
    fields = ('img_alt',)


translator.register(Category, CategoryTranslationOptions)
translator.register(TextPage, TextPageTranslationOptions)
translator.register(Article, ArticleTranslationOptions)
translator.register(ImageArticle, ImageArticleTranslationOptions)
