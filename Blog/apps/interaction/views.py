from typing import Union, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from shared.mixins.views_mixins import ScoreCommentMixin, CommentScoreMixin
from .forms import ScoreForm, CommentArticleForm
from .models import Score, FavoritesArticle, CommentArticle
from ..blog.models import Article


class AddScore(LoginRequiredMixin, CommentScoreMixin, CreateView):
    """
    If the user is authenticated add a rating (Score) to the Article
        and update the rating for the author's comments
    """
    model = Score
    form_class = ScoreForm

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """save Score for Article and update the rating for the author's comments"""
        object_form = form.save(commit=False)
        author = self.request.user
        article = Article.objects.get(slug=self.kwargs['slug'])
        object_form.author = author
        object_form.article = article
        object_form.save()
        comments = self.get_comments_for_score(article=article, author=author, model=CommentArticle)
        if comments[0]:
            comments[1].update(score=object_form)
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateScore(LoginRequiredMixin, CommentScoreMixin, UpdateView):
    """
    Update a rating (Score) of the Article
        and update the rating for the author's comments
    """
    form_class = ScoreForm

    def get_object(self, queryset=None, *args: Any, **kwargs: dict[str, Any]) -> Score:
        """return object of Score"""
        article = Article.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        obj = Score.objects.get(article=article, author=author)
        return obj

    def form_valid(self, form: ScoreForm, *args: Any, **kwargs: Any) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Save or Delete Score and update the rating for the author's comments"""
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
            comments = self.get_comments_for_score(article=article, author=author, model=CommentArticle)
            if comments[0]:
                comments[1].update(score=object_form)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteAdd(LoginRequiredMixin, CreateView):
    """Adds the author to the user's favorites"""
    model = FavoritesArticle

    def post(self, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """creates an author subscription for the user"""
        article = Article.objects.get(slug=self.kwargs['slug'])
        self.model.objects.create(subscriber=self.request.user, article=article)
        return redirect(self.request.META.get('HTTP_REFERER'))


class FavoriteDelete(LoginRequiredMixin, DeleteView):
    """Removes the author from the user's subscriptions"""
    model = FavoritesArticle

    def post(self, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
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

    def form_valid(self, form: CommentArticleForm, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """saves the form and adds the author's score"""
        object_form = form.save(commit=False)
        article = Article.objects.get(slug=self.kwargs['slug'])
        author = self.request.user
        object_form.author = author
        object_form.article = article
        score = self.get_score_for_comment(author=author, article=article, model=Score)
        if score[0]:
            object_form.score = score[1]
        object_form.save()
        return redirect('article_detail', self.kwargs['slug'])


class CommentDelete(LoginRequiredMixin, View):
    """
    Delete a comment of article
    """

    def post(self, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """checks if the user has a personal comment and deletes it"""
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

    def get_object(self, queryset=None, *args: Any, **kwargs: dict[str, Any]) -> CommentArticle:
        """return object of CommentArticle"""
        return CommentArticle.objects.get(author=self.request.user, pk=self.kwargs['pk'])

    def form_valid(self, form: CommentArticleForm, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """saves the form and adds the author's score"""
        obj = form.save(commit=False)
        score = self.get_score_for_comment(author=obj.author, article=obj.article, model=Score)
        if score[0]:
            obj.score = score[1]
        obj.save()
        return redirect('article_detail', obj.article.slug)
