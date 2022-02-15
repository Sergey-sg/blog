from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from apps.interaction.models import CommentArticle, FavoritesArticle, Score


class CommentFilter(filters.FilterSet):
    """filter for Comments"""

    class Meta:
        model = CommentArticle
        fields = ('article', 'author')


class FavoritesArticleFilter(filters.FilterSet):
    """filter for Article"""

    class Meta:
        model = FavoritesArticle
        fields = ('article', 'subscriber')


# class ScoreFilter(filters.FilterSet):
#     """filter for Comments"""
#
#     class Meta:
#         model = Score
#         fields = ('article', 'author')


class SubscriptionFilter(filters.FilterSet):
    """filter for Comments"""

    class Meta:
        model = get_user_model()
        fields = ('email',)
