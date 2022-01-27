from datetime import datetime

from django.db import models


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
    def get_image_name(self, name, filename):
        extension = filename.split('.')[-1]
        return f'{name}-{datetime.now()}.{extension}'

    class Meta:
        abstract = True

