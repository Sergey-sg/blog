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


# class ScoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Score
#         fields = ['url', 'author', 'article', 'score', 'status']
#
#     # def update(self, instance, validated_data):
#     #     raise ValueError('there in')
#     #     score = instance # Score.objects.get(pk=self.data['pk'])
#     #     if (validated_data.get('score'),) == score.score:
#     #         score.delete()
#     #     else:
#     #         score.score = validated_data.get('score')
#     #         score.save()
#     #     return instance


class AuthorSubscriptionSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='email')

    class Meta:
        model = get_user_model()
        fields = ['pk', 'user_email', 'subscription']

    def update(self, instance, validated_data):
        user = instance
        for subscription in validated_data.get('subscription'):
            if subscription in user.subscription.all():
                user.subscription.remove(subscription)
            else:
                user.subscription.add(subscription)
        user.save()
        return instance
