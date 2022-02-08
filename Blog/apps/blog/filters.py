from typing import Union

import django_filters
from django.contrib.auth import get_user_model

from .models import Article, Category


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ArticleFilter(django_filters.FilterSet):

    authors = set(Article.objects.all().values_list('author', flat=True))
    user = get_user_model()

    ordering = django_filters.OrderingFilter(fields=(('title', 'по заголовку'), ('average_rating', 'по рейтингу'), ),)
    search = django_filters.CharFilter(field_name='title', lookup_expr='icontains',)
    filter_category = NumberInFilter(field_name='category', lookup_expr='in', method='filter_categories')
    filter_author = django_filters.ModelChoiceFilter(
        queryset=user.objects.filter(pk__in=authors),
        field_name='author'
    )

    class Meta:
        model = Article
        fields = ('title', 'average_rating', 'category', 'author')

    @staticmethod
    def filter_categories(queryset, name, value):
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
