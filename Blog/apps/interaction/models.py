from ckeditor.fields import RichTextField
from django.db import models

import Blog
from .constants import Status, ScoreChoices
from ..blog.models import Article
from shared.mixins.model_utils import CreatedUpdateMixins


class Comment(CreatedUpdateMixins):
    """
    Comment model
    attributes:
        author (class User): communication with the User model
        article (class Article): communication with the Article model
        message (str): content of the comment
        created (datetime): data of create comment
        updated (datetime): data of update comment
    """
    author = models.ForeignKey(Blog.settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = RichTextField()
    status = models.CharField(max_length=1, choices=Status.choices, help_text='status of comment', default='p')

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'
        ordering = ['article', '-created']

    def __str__(self):
        return f'{self.article}--{self.author}--{self.created}'


class Score(CreatedUpdateMixins):
    """
    Score model of article
    attributes:
        author (class User): communication with the User model
        article (class Article): communication with the Article model
        score (int): choice of grades from one to five
        created (datetime): data of create score
        updated (datetime): data of update score
    """
    author = models.ForeignKey(Blog.settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=1, decimal_places=0, choices=ScoreChoices.choices)
    status = models.CharField(max_length=1, choices=Status.choices, help_text='status of comment', default='p')

    class Meta:
        verbose_name = 'score'
        verbose_name_plural = 'Scores'
        ordering = ['article', '-created']

    def __str__(self):
        return f'{self.article}--{self.author}--{self.created}'
