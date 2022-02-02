from django.contrib import admin

from ..interaction.models import Comment, Score, FavoritesArticle


@admin.register(Comment)
class TextPageAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'status', 'created',)
    list_filter = ['article', 'author', 'status']


@admin.register(Score)
class TextPageAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'score', 'status', 'created',)
    list_filter = ['article', 'author', 'status', 'score']


@admin.register(FavoritesArticle)
class FavoritesArticleAdmin(admin.ModelAdmin):
    list_display = ('article', 'subscriber', 'created',)
    list_filter = ['article', 'subscriber']

