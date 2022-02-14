from rest_framework import generics
from rest_framework import filters

from .filters import CommentFilter, FavoritesArticleFilter, ScoreFilter
from .serializers import CommentSerializer, FavoritesArticleSerializer, ScoreSerializer
from apps.interaction.models import CommentArticle, FavoritesArticle, Score


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


class ScoreListView(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    filterset_class = ScoreFilter


class ScoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


# class AddSubscription():
#     """
#     Adding an author subscription
#     """
#     def post(self, *args, **kwargs):
#         """Adding an author subscription"""
#         user = self.request.user
#         try:
#             author = get_user_model().objects.get(pk=self.kwargs['pk'])
#             user.subscription.add(author)
#             user.save()
#         except Exception:
#             pass
#         return redirect(self.request.META.get('HTTP_REFERER'))
#
#
# class SubscriptionDelete():
#     """
#     Deleting an author's subscription
#     """
#     def post(self, *args, **kwargs):
#         """Deleting an author's subscription"""
#         user = self.request.user
#         try:
#             author = get_user_model().objects.get(pk=self.kwargs['pk'])
#             user.subscription.remove(author)
#             user.save()
#         except Exception:
#             pass
#         return redirect(self.request.META.get('HTTP_REFERER'))
