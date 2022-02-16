from django.db.models import QuerySet, Manager

from apps.blog.constants import Published


class TextPageQuerySet(QuerySet):
    """Added published method for TextPage Queryset"""
    def published(self) -> QuerySet:
        """return only published pages"""
        return self.filter(published=Published.PUBLISHED)


class TextPageManager(Manager):
    """TextPage manager with published method for filtered objects"""
    def get_queryset(self) -> TextPageQuerySet:
        """return TextPageQuerySet"""
        return TextPageQuerySet(self.model, using=self._db)

    def published(self) -> QuerySet:
        """returns only published pages"""
        return self.get_queryset().published()
