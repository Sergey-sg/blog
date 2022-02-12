from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import inlineformset_factory

from .models import Article, ImageArticle


class ArticleForm(forms.ModelForm):
    """model form of Article"""

    class Meta:
        model = Article
        fields = (
            'title',
            'slug',
            'article_preview',
            'img_alt',
            'category',
            'short_description',
            'content',
            'recommended',
        )
        widgets = {
            'recommended': forms.CheckboxSelectMultiple(),
            'short_description': forms.Textarea(),
            'content': CKEditorWidget()
        }


# inlineformset for adding images to an article
ImageArticleInlineFormset = inlineformset_factory(
    Article,
    ImageArticle,
    fields=('image_article', 'img_alt',),
    extra=5,
    can_delete_extra=False,
    can_delete=True
)
