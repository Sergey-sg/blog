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

    def get_current_image_name(self, model):
        if self.pk is not None:    # if the article already exists then it is checked for a change in the preview image
            orig = model.objects.get(pk=self.pk)
            if orig.article_preview.name != self.article_preview.name:
                if self.article_preview:
                    name = self.get_image_name(name=self.title, filename=self.article_preview.name)
                    return {'image_name': name, 'new': True}
            else:
                return {'new': False}
        else:
            name = self.get_image_name(name=self.title, filename=self.article_preview.name)
            return {'image_name': name, 'new': True}

    class Meta:
        abstract = True


class ScoreMixins:
    @staticmethod
    def add_rating_to_article(article, score):
        article.number_of_likes = score.count()
        rating = score.aggregate(Avg('score'))['score__avg'] or 0
        article.average_rating = rating
        article.save()

