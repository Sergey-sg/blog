from typing import Any

from django.conf import settings
import datetime

from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from treebeard.mp_tree import MP_Node
from slugify import slugify

from shared.mixins.model_utils import CreatedUpdateMixins, DragDropMixins, ImageNameMixins
from shared.mixins.views_mixins import CurrentSlugMixin, SendSubscriptionMixin

from .constants import Published


class Category(MP_Node, CurrentSlugMixin, CreatedUpdateMixins):
    """
    Category model
        attributes:
             name (str): category name
             slug (str): used to generate URL
             created (datetime): date of created item
             updated (datetime): date of last update item
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        verbose_name=_('name'),
        help_text=_('category name')
    )
    node_order_by = ['name']
    slug = models.SlugField(
        unique=True,
        help_text=_('used to generate URL'),
        null=True,
        blank=True
    )

    class Meta(object):
        verbose_name = _('category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self) -> str:
        """class method returns the category in string representation"""
        return self.name

    def save(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """if the slug is not created then it is created from the name of the category"""
        origin = Category.objects.get(pk=self.pk)
        if origin and self.slug == origin.slug:
            pass
        else:
            self.slug = self.get_current_slug(slug=self.slug, alt=self.name, model=Category)
        self.slug = self.get_current_slug(slug=self.slug, alt=self.name, model=Category)
        super(Category, self).save(*args, **kwargs)


class Article(ImageNameMixins, CurrentSlugMixin, SendSubscriptionMixin, DragDropMixins):
    """
    Article model
        attributes:
             title (str): title of article
             slug (str): used to generate URL
             article_preview (img): article preview image
             img_alt (str): text to be loaded in case of image loss
             author (class User): author of article
             category(class Category): category of article
             short_description (str): article summary
             content (str): the content of the article
             recommended (class Article): recommended articles
             average_rating (float): average article rating
             number_of_likes (int): number of article ratings
             created (datetime): date of created item
             updated (datetime): date of last update item
             dd_order (int): used to drag and drop items in the admin
    """
    title = models.CharField(
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(3)],
        verbose_name=_('title'),
        help_text=_('title of article')
    )
    slug = models.SlugField(
        unique=True,
        help_text=_('used to generate URL'),
        null=True,
        blank=True
    )
    article_preview = models.ImageField(
        upload_to='article_preview/%Y/%m/%d',
        verbose_name=_('article preview'),
        help_text="article preview image"
    )
    img_alt = models.CharField(
        max_length=200,
        null=True, blank=True,
        verbose_name=_('image alternative'),
        help_text=_('text to be loaded in case of image loss')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('author'),
        help_text=_('author of article')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('category'),
        help_text=_('category of article')
    )
    short_description = models.CharField(
        max_length=350,
        verbose_name=_('short description'),
        help_text=_('a short description about the article')
    )
    content = RichTextField(
        verbose_name=_('content'),
        help_text=_('the content of the article')
    )
    recommended = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name=_('recommended'),
        help_text=_('recommended articles')
    )
    average_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
        verbose_name=_('average rating'),
        help_text=_('average article rating')
    )
    number_of_likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_('number of likes'),
        help_text=_('number of article ratings')
    )

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('Articles')
        ordering = ['dd_order', '-created']

    def __str__(self):
        """class method returns the article in string representation"""
        return self.title

    def save(self, *args, **kwargs) -> None:
        """if the slug is not created then it is created from the title of the article
        and rename article preview image"""
        try:
            origin = Article.objects.get(pk=self.pk)
        except Exception:
            origin = False
        if origin and self.slug == origin.slug:
            pass
        else:
            self.slug = self.get_current_slug(slug=self.slug, alt=self.title, model=Article)
        if self.pk is not None:    # if the article already exists then it is checked for a change in the preview image
            orig = Article.objects.get(pk=self.pk)
            if orig.article_preview.name != self.article_preview.name:
                if self.article_preview:
                    self.article_preview.name = self.get_image_name(name=self.slug, filename=self.article_preview.name)
                    if not self.img_alt:
                        self.img_alt = self.title
            super(Article, self).save(*args, **kwargs)
        else:
            self.article_preview.name = self.get_image_name(name=self.slug, filename=self.article_preview.name)
            if not self.img_alt:
                self.img_alt = self.title
            super(Article, self).save(*args, **kwargs)
            self.send_to_subscriptions(article=self)

    def get_absolute_url(self) -> str:
        """
        Returns the URL to access the article instance.
        """
        return reverse_lazy('article_detail', args=[self.slug])


class ImageArticle(DragDropMixins, ImageNameMixins):
    """
    ImageArticle model
        attributes:
             article (Class Article): linked Article model with image
             image_article (img): article image
             img_alt (str): text to be loaded in case of image loss
             created (datetime): date of created item
             updated (datetime): date of last update item
             dd_order (int): used to drag and drop items in the admin
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('article'),
        help_text=_('linked Article model with image')
    )
    image_article = models.ImageField(
        upload_to='image_article/%Y/%m/%d',
        verbose_name=_('image'),
        help_text="article image",
        blank=True
    )
    img_alt = models.CharField(
        max_length=200,
        verbose_name=_('image alternative'),
        help_text=_('text to be loaded in case of image loss'),
        blank=True
    )

    class Meta(object):
        verbose_name = _('image')
        verbose_name_plural = _('Images for article')
        ordering = ['dd_order', 'created']

    def __str__(self) -> str:
        """class method returns the image of article in string representation"""
        return f'Article{self.article}--{self.img_alt}'

    def save(self, *args, **kwargs) -> None:
        """if the slug is not created then it is created from the title of the article
                and rename article preview image"""
        if not self.img_alt:
            self.img_alt = f'{self.article.title}--{datetime.datetime.now()}'
        if self.pk is not None:    # if the image already exists, then it is checked for change
            orig = ImageArticle.objects.get(pk=self.pk)
            if orig.image_article.name != self.image_article.name:
                if self.image_article:
                    self.image_article.name = self.get_image_name(name=self.img_alt, filename=self.image_article.name)
        else:
            self.image_article.name = self.get_image_name(name=self.img_alt, filename=self.image_article.name)
        super(ImageArticle, self).save(*args, **kwargs)


class TextPage(CreatedUpdateMixins):
    """
    TextPage model
        attributes:
             title (img): title of text page
             content (str): the content of the text page
             published (str): publishing or hiding a page from public access
             created (datetime): date of created item
             updated (datetime): date of last update item
    """
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('title'),
        help_text=_('title of text page')
    )
    content = RichTextField(
        verbose_name=_('content'),
        help_text=_('the content of the text page')
    )
    published = models.CharField(
        max_length=1,
        choices=Published.choices,
        verbose_name=_('published'),
        help_text=_('Published or draft'),
        default=Published.PUBLISHED,
    )
    slug = models.SlugField(
        unique=True,
        help_text=_('used to generate URL'),
        null=True, blank=True
    )

    class Meta:
        verbose_name = _('text page')
        verbose_name_plural = _('Text pages')
        ordering = ['-created']

    def __str__(self) -> str:
        """class method returns the text page in string representation"""
        return self.title

    def save(self, *args, **kwargs) -> None:
        """if the slug is not entered, then it is created from the page title"""
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.slug)
        super(TextPage, self).save(*args, **kwargs)
