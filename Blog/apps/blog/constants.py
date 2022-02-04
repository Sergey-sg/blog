from django.db import models


class Published(models.TextChoices):
    DRAFT = ('d', 'draft')
    PUBLISHED = ('p', 'published')
