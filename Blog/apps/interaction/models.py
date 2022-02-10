from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import Status, ScoreChoices
from ..blog.models import Article
from shared.mixins.model_utils import CreatedUpdateMixins, ScoreMixins


class CommentArticle(CreatedUpdateMixins):
    """
    CommentArticle model
    attributes:
        author (class User): communication with the User model
        article (class Article): communication with the Article model
        message (str): content of the comment
        created (datetime): data of create comment
        updated (datetime): data of update comment
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        help_text=_('author of comment'))
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_('article'),
        help_text=_('commented article')
    )
    score = models.ForeignKey(
        'Score',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('score'),
        help_text=_('assessment of the author of the commented article')
    )
    message = RichTextField(
        verbose_name=_('message'),
        validators=[MinLengthValidator(3)],
        help_text=_('message (comment) of article')
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        verbose_name=_('status'),
        help_text=_('status of comment'),
        default=Status.PUBLISHED
    )

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('Comments')
        ordering = ['article', '-created']

    def __str__(self) -> str:
        """class method returns the comment in string representation"""
        return f'{self.article}--{self.author}--{self.created}'


class Score(CreatedUpdateMixins, ScoreMixins):
    """
    Score model of article
    attributes:
        author (class User): communication with the User model
        article (class Article): communication with the Article model
        score (int): choice of grades from one to five
        created (datetime): data of create score
        updated (datetime): data of update score
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        help_text=_('author of score')
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_('article'),
        help_text=_('author of score')
    )
    score = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        choices=ScoreChoices.choices,
        default=ScoreChoices.ONE,
        verbose_name=_('score'),
        help_text=_('assessment of the author of the article')
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        verbose_name=_('status'),
        help_text=_('status of comment'),
        default=Status.PUBLISHED
    )

    class Meta:
        verbose_name = _('score')
        verbose_name_plural = _('Scores')
        ordering = ['article', '-created']

    def __str__(self) -> str:
        """class method returns the score in string representation"""
        return f'{self.article}--{self.author}--score'

    def save(self, *args, **kwargs) -> None:
        """save Score and adds rating to article"""
        super(Score, self).save(*args, **kwargs)
        score = Score.objects.filter(article=self.article, status=Status.PUBLISHED).only('score')
        self.add_rating_to_article(article=self.article, score=score)

    def delete(self, using=None, keep_parents=False, *args, **kwargs) -> None:
        """delete Score and update rating to article"""
        super(Score, self).delete(*args, **kwargs)
        score = Score.objects.filter(article=self.article, status=Status.PUBLISHED).only('score')
        self.add_rating_to_article(article=self.article, score=score)


class FavoritesArticle(CreatedUpdateMixins):
    """
    FavoritesArticle model
    attributes:
        subscriber (class User): communication with the User model
        article (class Article): communication with the Article model
        created (datetime): data of create score
        updated (datetime): data of update score
    """
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('Favorites')
        ordering = ['article', 'subscriber', '-created']

    def __str__(self) -> str:
        """class method returns the favorite article in string representation"""
        return f'Favorites article: {self.article}'
