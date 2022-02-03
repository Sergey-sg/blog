from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Score, CommentArticle


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('score',)


class CommentArticleForm(forms.ModelForm):

    class Meta:
        model = CommentArticle
        fields = ('message',)

