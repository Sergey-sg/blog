from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from shared.mixins.views_mixins import ScoreCommentMixin, CommentScoreMixin
from .forms import ScoreForm, CommentArticleForm
from .models import Score, FavoritesArticle, CommentArticle
from ..blog.models import Article


class AddScore(LoginRequiredMixin, CommentScoreMixin, CreateView):
    model = Score
    form_class = ScoreForm

    def form_valid(self, form, *args, **kwargs):
        object_form = form.save(commit=False)
        author = self.request.user
        article = Article.objects.get(slug=self.kwargs['slug'])
        object_form.author = author
        object_form.article = article
        object_form.save()
        comments = self.get_comments_for_score(article=article, author=author)
        if comments[0]:
            comments[1].update(score=object_form)
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateScore(LoginRequiredMixin, CommentScoreMixin, UpdateView):
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
            comments = self.get_comments_for_score(article=article, author=author)
            if comments[0]:
                comments[1].update(score=object_form)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteAdd(LoginRequiredMixin, CreateView):
    model = FavoritesArticle

    def post(self, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs['slug'])
        self.model.objects.create(subscriber=self.request.user, article=article)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteDelete(LoginRequiredMixin, DeleteView):
    model = FavoritesArticle

    def post(self, *args, **kwargs):
        article = Article.objects.get(slug=self.kwargs['slug'])
        try:
            favorite = self.model.objects.get(subscriber=self.request.user, article=article)
            favorite.delete()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class CommentCreate(LoginRequiredMixin, ScoreCommentMixin, CreateView):
    """
    Implementation of the creation of a new comment for article
    """
    model = CommentArticle
    form_class = CommentArticleForm
    template_name = 'interaction/comment.jinja2'

    def form_valid(self, form, **kwargs):
        object_form = form.save(commit=False)
        article = Article.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        object_form.author = author
        object_form.article = article
        score = self.get_score_for_comment(author=author, article=article)
        if score[0]:
            object_form.score = score[1]
        object_form.save()
        return redirect('article_detail', self.kwargs['slug'])


class CommentDelete(LoginRequiredMixin, View):
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


class CommentUpdate(LoginRequiredMixin, ScoreCommentMixin, UpdateView):
    """
    Implementation of changes in information about the comment of article.
    """
    form_class = CommentArticleForm
    template_name = 'interaction/comment.jinja2'

    def get_object(self, queryset=None, *args, **kwargs):
        return CommentArticle.objects.get(author=self.request.user, pk=self.kwargs['pk'])

    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        score = self.get_score_for_comment(author=obj.author, article=obj.article)
        if score[0]:
            obj.score = score[1]
        obj.save()
        return redirect('article_detail', obj.article.slug)
