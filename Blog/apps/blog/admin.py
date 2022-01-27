from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from adminsortable2.admin import SortableAdminMixin

from .models import Category, Article, ImageArticle, TextPage


class MyAdmin(TreeAdmin):
    list_display = ['name', 'created']
    search_fields = ('name', )
    exclude = ('path', 'depth', 'numchild', '_position')
    form = movenodeform_factory(Category)
    ordering = ('path', 'depth', 'numchild', 'name', 'created', )

admin.site.register(Category, MyAdmin)


# @admin.register(Article)
# class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
#     list_display = ('title', 'slug', 'author', 'category', 'created',)
#     exclude = ('dd_order',)
#     search_fields = ('name',)
#     list_filter = ['author']
#
#
@admin.register(ImageArticle)
class ImageOfArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('img_alt', 'article', 'image_article', 'created',)
    exclude = ('dd_order',)
    list_filter = ['article']


class ImageArticleAdmin(admin.TabularInline):
    model = ImageArticle
    exclude = ('dd_order',)


class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'created',)
    exclude = ('dd_order',)
    search_fields = ('name',)
    list_filter = ['author']
    inlines = [
        ImageArticleAdmin,
    ]

admin.site.register(Article, ArticleAdmin)


@admin.register(TextPage)
class TextPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created',)
    search_fields = ('title',)
