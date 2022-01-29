import django_filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('date_created', 'created'),
        ),
    )

    class Meta:
        model = Article
        fields = ('title',)
