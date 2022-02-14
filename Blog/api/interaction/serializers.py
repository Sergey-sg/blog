from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.interaction.models import CommentArticle, FavoritesArticle, Score


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentArticle
        fields = ['url', 'author', 'article', 'message']


class FavoritesArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritesArticle
        fields = ['url', 'subscriber', 'article']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['url', 'author', 'article', 'score', 'status']


# class AuthorSubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['url', 'email', 'subscription']
#
#     def update(self, instance, validated_data):
#         if
#         instance.subscription = validated_data.get('subscription', instance.subscription)
#         instance.save()
#         return instance
