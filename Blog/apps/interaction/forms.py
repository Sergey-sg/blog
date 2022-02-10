from django import forms

from .models import Score, CommentArticle


class ScoreForm(forms.ModelForm):
    """model form of scores"""

    class Meta:
        model = Score
        fields = ('score',)


class CommentArticleForm(forms.ModelForm):
    """model form of comment of article"""

    class Meta:
        model = CommentArticle
        fields = ('message',)
