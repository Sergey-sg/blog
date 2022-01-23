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
