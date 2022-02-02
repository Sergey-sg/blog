from django import template
from ..models import Score

register = template.Library()


@register.simple_tag(takes_context=True)
def in_scores(context, article):
    request = context['request']
    try:
        score = Score.objects.get(author=request.user, article=article)
    except Exception:
        return False
    if score:
        return True
