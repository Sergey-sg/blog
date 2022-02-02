from django import forms

from .models import Score


class ScoreCreateForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('score',)
