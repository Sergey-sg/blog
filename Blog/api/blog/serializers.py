from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.blog.models import Article, Category, ImageArticle, TextPage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        # read_only_fields = ['email']
        fields = ('url', 'email', 'first_name', 'last_name', 'phone_number', 'photo', 'img_alt')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'name', 'slug')


class ImageArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageArticle
        fields = ('url', 'article', 'image_article', 'img_alt')


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('url', 'title', 'slug', 'article_preview', 'img_alt', 'author', 'category', 'short_description',
                  'content', 'recommended', 'average_rating', 'number_of_likes')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TextPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPage
        fields = ('url', 'title', 'slug', 'content', 'published',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
