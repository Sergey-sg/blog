from django.contrib.auth import get_user_model
from rest_framework import generics

from .filters import CommentFilter, FavoritesArticleFilter, SubscriptionFilter
from .serializers import CommentSerializer, FavoritesArticleSerializer, AuthorSubscriptionSerializer
from apps.interaction.models import CommentArticle, FavoritesArticle


class CommentListView(generics.ListCreateAPIView):
    queryset = CommentArticle.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentArticle.objects.all()
    serializer_class = CommentSerializer


class FavoritesArticleListView(generics.ListCreateAPIView):
    queryset = FavoritesArticle.objects.all()
    serializer_class = FavoritesArticleSerializer
    filterset_class = FavoritesArticleFilter


class FavoritesArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FavoritesArticle.objects.all()
    serializer_class = FavoritesArticleSerializer


# class ScoreListView(generics.ListCreateAPIView):
#     queryset = Score.objects.all()
#     serializer_class = ScoreSerializer
#     filterset_class = ScoreFilter
#
#
# class ScoreDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Score.objects.all()
#     serializer_class = ScoreSerializer


class AuthorSubscriptionListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = AuthorSubscriptionSerializer
    filterset_class = SubscriptionFilter


class AuthorSubscriptionDetailView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = AuthorSubscriptionSerializer
