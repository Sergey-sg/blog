from typing import Any, Union

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import get_user_model
from django_filters.views import FilterView

from .filters import ArticleFilter
from .forms import ArticleForm, ImageArticleInlineFormset
from .models import Article, Category, TextPage
from ..interaction.forms import ScoreForm, CommentArticleForm
from ..interaction.models import CommentArticle


class ArticleListView(FilterView):
    """
    Generates a list of article with filter
    """
    template_name = 'blog/home.jinja2'
    paginate_by = 16
    filterset_class = ArticleFilter
    model = Article

    def get_queryset(self) -> QuerySet:
        """return queryset with filter"""
        qs = super(ArticleListView, self).get_queryset()
        if 'filter_category' in self.request.GET and self.request.GET['filter_category']:
            qs = qs.filter(category_id=self.request.GET['filter_category'])
        return qs

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add to context filter as "filterset" """
        context = super(ArticleListView, self).get_context_data()
        context['filterset'] = self.filterset
        context['category'] = Category.get_annotated_list()
        return context


class ArticleDetailView(DetailView, MultipleObjectMixin):
    """
    Generates a detail of article with
    """
    model = Article
    template_name = "blog/detail_article.jinja2"
    paginate_by = 8
    object_list = None

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add to context ScoreForm, CommentArticleForm and AuthenticationForm and create object_list of comments"""
        self.object_list = CommentArticle.objects.filter(article__slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['score'] = ScoreForm()
        context['new_comment'] = CommentArticleForm()
        context['login'] = AuthenticationForm()
        return context


class AddSubscription(LoginRequiredMixin, View):
    """
    Adding an author subscription
    """
    def post(self, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Adding an author subscription"""
        user = self.request.user
        try:
            author = get_user_model().objects.get(pk=self.kwargs['pk'])
            user.subscription.add(author)
            user.save()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class SubscriptionDelete(LoginRequiredMixin, View):
    """
    Deleting an author's subscription
    """
    def post(self, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Deleting an author's subscription"""
        user = self.request.user
        try:
            author = get_user_model().objects.get(pk=self.kwargs['pk'])
            user.subscription.remove(author)
            user.save()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class ArticleCreate(LoginRequiredMixin, CreateView):
    """
    Creates new Article with ImageArticle
    """
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_create.jinja2'

    def get(self, *args: Any, **kwargs: dict[str, Any]) -> TemplateResponse:
        """send context to response"""
        self.object = None
        imagearticle_form = ImageArticleInlineFormset()
        return self.render_to_response(self.get_context_data(imagearticle_form=imagearticle_form))

    def post(self, request, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponseRedirect, TemplateResponse]:
        """checks valid of filling out the class form and imagearticle form"""
        self.object = None
        form = self.get_form()
        imagearticle_form = ImageArticleInlineFormset(request.POST, request.FILES)
        if form.is_valid() and imagearticle_form.is_valid():
            return self.form_valid(form, imagearticle_form)
        else:
            return self.form_invalid(form, imagearticle_form)

    def form_valid(self, form: ArticleForm, *args: Any) -> HttpResponseRedirect:
        """save class form and imagearticle form"""
        object_form = form.save(commit=False)
        object_form.author = self.request.user
        object_form.save()
        for inlineforms in args:
            for inlineform in inlineforms:
                try:
                    inlineform_object = inlineform.save(commit=False)
                    if inlineform_object.image_article:
                        inlineform_object.article = object_form
                        inlineform_object.save()
                except Exception:
                    pass
        return redirect('article_detail', object_form.slug)

    def form_invalid(self, form: ArticleForm, *args: Any) -> TemplateResponse:
        """returns a form for correcting errors"""
        return self.render_to_response(self.get_context_data(form=form, imagearticle_form=args[0]))


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    """
    Displays a form for editing information about article.
    """
    form_class = ArticleForm
    template_name = 'blog/article_update.jinja2'

    def get_object(self, queryset=None) -> Article:
        """get object of Article if user is the author"""
        return get_object_or_404(Article, author=self.request.user, slug=self.kwargs['slug'])

    def get(self, *args: Any, **kwargs: dict[str, Any]) -> TemplateResponse:
        """send context to response"""
        self.object = self.get_object()
        imagearticle_form = ImageArticleInlineFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(imagearticle_form=imagearticle_form))

    def post(self, request, *args: Any, **kwargs: dict[str, Any]) -> Union[HttpResponseRedirect, TemplateResponse]:
        """checks valid of filling out the class form and imagearticle form"""
        self.object = self.get_object()
        form = self.get_form()
        imagearticle_form = ImageArticleInlineFormset(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and imagearticle_form.is_valid():
            return self.form_valid(form, imagearticle_form)
        else:
            return self.form_invalid(form, imagearticle_form)

    def form_valid(self, form, *args) -> HttpResponseRedirect:
        """save class form and imagearticle form"""
        obj_form = form.save()
        inlineform_object = args[0]
        inlineform_object.article = obj_form
        inlineform_object.save()
        return redirect('article_detail', obj_form.slug)

    def form_invalid(self, form: ArticleForm, *args: Any) -> TemplateResponse:
        """returns a form for correcting errors"""
        return self.render_to_response(self.get_context_data(form=form, imagearticle_form=args[0]))


class TextPageList(ListView):
    """Displays a list of text pages"""
    template_name = 'blog/text_page_list.jinja2'
    paginate_by = 8

    def get_queryset(self) -> QuerySet[TextPage]:
        """returns only published pages"""
        return TextPage.objects.published()


class TextPageDetail(DetailView):
    """Displays a detail for text page"""
    model = TextPage
    template_name = 'blog/text_page_detail.jinja2'

    def get_queryset(self) -> TextPage:
        """returns only published page"""
        queryset = super(TextPageDetail, self).get_queryset()
        return queryset.published()
