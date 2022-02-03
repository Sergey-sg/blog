from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from .forms import ScoreForm, CommentArticleForm
from .models import Score, FavoritesArticle, CommentArticle
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


class CommentCreate(CreateView):
    """
    Implementation of the creation of a new comment for article
    """
    model = CommentArticle
    form_class = CommentArticleForm

    def form_valid(self, form, **kwargs):
        object_form = form.save(commit=False)
        object_form.author = self.request.user
        object_form.article = Article.objects.get(slug=self.kwargs['slug'])
        object_form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class CommentDelete(View):
    """
    Delete a comment of article
    """

    def post(self, *args, **kwargs):
        try:
            comment = CommentArticle.objects.get(pk=self.kwargs['pk'], author=self.request.user)
            comment.delete()
        except Exception:
            pass
        return redirect('article_detail', self.kwargs['slug'])


class CommentUpdate(UpdateView):
    """
    Implementation of changes in information about the comment of article.
    """
    form_class = CommentArticleForm
    template_name = 'interaction/change_comment.jinja2'

    def get_object(self, queryset=None, *args, **kwargs):
        return CommentArticle.objects.get(author=self.request.user, pk=self.kwargs['pk'])

    def form_valid(self, form, **kwargs):
        obj = form.save()
        return redirect('article_detail', obj.article.slug)
