from django.db import models


class Published(models.TextChoices):
    draft = ('d', 'draft')
    published = ('p', 'published')
