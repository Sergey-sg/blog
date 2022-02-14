from django.contrib.auth import get_user_model
from django.db import OperationalError
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from .models import Article, Category


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """filter to sort queryset digits(primary key)"""
    pass


class ArticleFilter(filters.FilterSet):
    """filter for Article"""
    try:
        authors = [author.author.pk for author in Article.objects.all().only('author')]
    except OperationalError:
        authors = []
    ordering = filters.OrderingFilter(fields=(('title', 'по заголовку'), ('average_rating', 'по рейтингу'), ),)
    search = filters.CharFilter(field_name='title', lookup_expr='icontains',)
    filter_category = NumberInFilter(field_name='category', lookup_expr='in', method='filter_categories', )
    filter_author = filters.ModelChoiceFilter(
        queryset=get_user_model().objects.filter(pk__in=authors),
        field_name='author'
    )

    class Meta:
        model = Article
        fields = ('title', 'average_rating', 'category', 'author')

    @staticmethod
    def filter_categories(queryset, name, value) -> QuerySet:
        """get the filter value by category and return the combined queryset from all child categories"""
        try:
            categories = Category.objects.get(pk=value[0]).get_descendants()
            if categories:
                for category in categories:
                    queryset1 = Article.objects.filter(category=category)
                    queryset = queryset | queryset1
                return queryset
        except Exception:
            pass
        return queryset
