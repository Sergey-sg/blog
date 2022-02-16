from datetime import datetime

from django.db import models
from django.db.models import Avg


class CreatedUpdateMixins(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DragDropMixins(CreatedUpdateMixins):
    dd_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        abstract = True


class ImageNameMixins:
    @staticmethod
    def get_image_name(name, filename):
        extension = filename.split('.')[-1]
        return f'{name}-{datetime.now()}.{extension}'

    class Meta:
        abstract = True


class ScoreMixins:
    @staticmethod
    def add_rating_to_article(article, score):
        article.number_of_likes = score.count()
        rating = score.aggregate(Avg('score'))['score__avg'] or 0
        article.average_rating = rating
        article.save()
