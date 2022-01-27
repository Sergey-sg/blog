from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator
from django.db import models

from treebeard.mp_tree import MP_Node
from slugify import slugify
from shared.mixins.model_utils import CreatedUpdateMixins, DragDropMixins, ImageNameMixins

import Blog
from .constants import Published


class Category(MP_Node, CreatedUpdateMixins):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)])
    node_order_by = ['name']
    slug = models.SlugField(unique=True, help_text='used to generate URL', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        """class method returns the category in string representation"""
        return self.name

    class Meta(object):
        verbose_name = 'category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Article(DragDropMixins, ImageNameMixins):
    title = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    slug = models.SlugField(unique=True, help_text='used to generate URL', null=True, blank=True)
    article_preview = models.FileField(upload_to='article_preview/%Y/%m/%d', help_text="article preview")
    img_alt = models.CharField(max_length=200, null=True, blank=True, help_text='текст, который будет загружен в случае потери изображения')
    author = models.ForeignKey(Blog.settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    short_description = models.TextField()
    content = RichTextField()
    # featured_articles =
    # average_rating =
    # number_of_reviews =
    # number_of_likes =

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        if self.article_preview:
            self.article_preview.name = self.get_image_name(name=self.slug, filename=self.article_preview.name)
            if not self.img_alt:
                self.img_alt = self.title
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        """class method returns the article in string representation"""
        return self.title

    class Meta(object):
        verbose_name = 'article'
        verbose_name_plural = 'Articles'
        ordering = ['dd_order', '-created']


class ImageArticle(DragDropMixins, ImageNameMixins):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    image_article = models.ImageField(upload_to='image_article/%Y/%m/%d', help_text="image article")
    img_alt = models.CharField(max_length=200, help_text='текст, который будет загружен в случае потери изображения')

    def save(self, *args, **kwargs):
        self.image_article.name = self.get_image_name(name=self.img_alt[:15], filename=self.image_article.name)
        super(ImageArticle, self).save(*args, **kwargs)

    def __str__(self):
        """class method returns the image of article in string representation"""
        return self.img_alt

    class Meta(object):
        verbose_name = 'image'
        verbose_name_plural = 'Images of article'
        ordering = ['dd_order', 'created']


class TextPage(CreatedUpdateMixins):
    title = models.CharField(max_length=150, unique=True)
    content = RichTextField()
    published = models.CharField(
        max_length=1,
        choices=Published.choices,
        help_text='Published or draft',
        default='d',
    )
    slug = models.SlugField(unique=True, help_text='used to generate URL', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        super(TextPage, self).save(*args, **kwargs)

    def __str__(self):
        """class method returns the text page in string representation"""
        return self.title

    class Meta(object):
        verbose_name = 'text page'
        verbose_name_plural = 'Text pages'
        ordering = ['-created']
