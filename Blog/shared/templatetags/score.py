from django_jinja import library

from apps.interaction.models import Score, FavoritesArticle


@library.global_function
def in_scores(request, article):
    try:
        score = Score.objects.get(author=request.user, article=article)
    except Exception:
        return False
    if score:
        return True


@library.global_function
def in_favorite(request, article):
    try:
        favorite = FavoritesArticle.objects.get(subscriber=request.user, article=article)
    except Exception:
        return False
    if favorite:
        return True


@library.global_function
def in_subscription(request, author):
    try:
        subscription = request.user.subscription.all()
    except Exception:
        return False
    if author in subscription:
        return True
