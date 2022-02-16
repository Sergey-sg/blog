from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .forms import ImageArticleInlineFormset
from .models import Category, Article, ImageArticle, TextPage


class CategoryAdmin(TreeAdmin, TranslationAdmin):
    list_display = ['name', 'slug', 'created']
    search_fields = ('name', )
    exclude = ('path', 'depth', 'numchild', '_position')
    form = movenodeform_factory(Category)
    ordering = ('path', 'depth', 'numchild', 'name', 'created', )


admin.site.register(Category, CategoryAdmin)


class ImageArticleAdmin(SortableInlineAdminMixin, TranslationTabularInline):
    model = ImageArticle
    formset = ImageArticleInlineFormset
    exclude = ('dd_order',)
    can_delete = True


@admin.register(Article)
class ArticleAdmin(SortableAdminMixin, TranslationAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'average_rating', 'created',)
    exclude = ('dd_order',)
    search_fields = ('name',)
    list_filter = ['author']
    inlines = [
        ImageArticleAdmin,
    ]


@admin.register(TextPage)
class TextPageAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ('title', 'published', 'created',)
    search_fields = ('title',)
