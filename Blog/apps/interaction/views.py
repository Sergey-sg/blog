from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import ScoreForm
from .models import Score, FavoritesArticle
from ..blog.models import Article


class AddScore(CreateView):
    model = Score
    form_class = ScoreForm

    def form_valid(self, form, *args, **kwargs):
        object_form = form.save(commit=False)
        object_form.author = self.request.user
        object_form.article = Article.objects.get(slug=self.kwargs['slug'])
        object_form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateScore(UpdateView):
    form_class = ScoreForm

    def get_object(self, queryset=None, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        obj = Score.objects.get(article=article, author=author)
        return obj

    def form_valid(self, form, *args, **kwargs):
        object_form = form.save(commit=False)
        author = self.request.user
        article = Article.objects.get(slug=self.kwargs['slug'])
        score = Score.objects.get(author=author, article=article)
        if object_form.score == score.score:
            score.delete()
        else:
            object_form.author = author
            object_form.article = article
            object_form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteAdd(CreateView):
    model = FavoritesArticle

    def post(self, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs['slug'])
        self.model.objects.create(subscriber=self.request.user, article=article)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteDelete(DeleteView):
    model = FavoritesArticle

    def post(self, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs['slug'])
        try:
            favorite = self.model.objects.get(subscriber=self.request.user, article=article)
            favorite.delete()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))
