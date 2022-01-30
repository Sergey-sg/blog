import django_filters
from .models import Article, Category


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ArticleFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(fields=(('title', 'по заголовку'), ('created', 'по дате создания'), ),)
    search = django_filters.CharFilter(field_name='title', lookup_expr='icontains',)
    filter_category = NumberInFilter(field_name='category', lookup_expr='in')

    class Meta:
        model = Article
        fields = ('title', 'created', 'category')
