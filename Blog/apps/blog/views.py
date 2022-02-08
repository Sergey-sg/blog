from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
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
    Generates a list of article with ordering
    """
    template_name = 'blog/home.jinja2'
    paginate_by = 2
    filterset_class = ArticleFilter
    model = Article

    def get_queryset(self):
        qs = super(ArticleListView, self).get_queryset()
        if 'filter_category' in self.request.GET:
            qs = qs.filter(category_id=self.request.GET['filter_category'])
        return qs


    # def get_queryset(self):
    #     """Return the filtered queryset"""
    #     queryset = super(ArticleListView, self).get_queryset()    # self.model.objects.all()
    #     self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
    #     try:
    #         categories = Category.objects.get(pk=self.request.GET['filter_category']).get_descendants()
    #         queryset = self.model.objects.filter(category=self.request.GET['filter_category'])
    #         if categories:
    #             for category in categories:
    #                 queryset1 = self.model.objects.filter(category=category)
    #                 queryset = queryset | queryset1
    #             return queryset
    #     except Exception:
    #         pass
    #     return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        """Add to context filter as "filterset" """
        context = super(ArticleListView, self).get_context_data()
        context['filterset'] = self.filterset
        context['category'] = Category.get_annotated_list()
        return context


class ArticleDetailView(DetailView, MultipleObjectMixin):
    model = Article
    template_name = "blog/detail_article.jinja2"
    paginate_by = 8
    object_list = None

    def get_context_data(self, **kwargs):
        """Add to context filter as "filterset" """
        self.object_list = CommentArticle.objects.filter(article__slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['score'] = ScoreForm()
        context['new_comment'] = CommentArticleForm()
        context['login'] = AuthenticationForm()
        return context


class AddSubscription(View):

    def post(self, *args, **kwargs):
        user = self.request.user
        try:
            author = get_user_model().objects.get(pk=self.kwargs['pk'])
            user.subscription.add(author)
            user.save()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class SubscriptionDelete(View):

    def post(self, *args, **kwargs):
        user = self.request.user
        try:
            author = get_user_model().objects.get(pk=self.kwargs['pk'])
            user.subscription.remove(author)
            user.save()
        except Exception:
            pass
        return redirect(self.request.META.get('HTTP_REFERER'))


class ArticleCreate(CreateView):

    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_create.jinja2'

    def get(self, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imagearticle_form = ImageArticleInlineFormset()
        return self.render_to_response(self.get_context_data(form=form, imagearticle_form=imagearticle_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imagearticle_form = ImageArticleInlineFormset(request.POST, request.FILES)
        if form.is_valid() and imagearticle_form.is_valid():
            return self.form_valid(form, imagearticle_form)
        else:
            return self.form_invalid(form, imagearticle_form)

    def form_valid(self, form, *args):
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
        return super(ArticleCreate, self).form_valid(form)

    def form_invalid(self, form, *args):
        return self.render_to_response(self.get_context_data(form=form, imagearticle_form=args[0]))


class ArticleUpdate(UpdateView):
    """
    Displays a form for editing information about a company.
    """
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update.jinja2'

    def get_queryset(self, *args, **kwargs):
        queryset = super(ArticleUpdate, self).get_queryset()
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['imagearticle_form'] = ImageArticleInlineFormset(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['imagearticle_form'] = ImageArticleInlineFormset(instance=self.object)
        return context

    def form_valid(self, form, *args):
        context = self.get_context_data()
        imagearticle_form = context['imagearticle_form']
        if form.is_valid() and imagearticle_form.is_valid():
            # self.object = form.save()
            form.save()
            imagearticle_form.save()
        else:
            return self.form_invalid(form, imagearticle_form)
        return super(ArticleUpdate, self).form_valid(form)

    def form_invalid(self, form, *args):
        return self.render_to_response(self.get_context_data(form=form, imagearticle_form=args[0]))


class TextPageList(ListView):
    template_name = 'blog/text_page_list.jinja2'
    paginate_by = 8

    def get_queryset(self):
        return TextPage.objects.filter(published='p')


class TextPageDetail(DetailView):
    model = TextPage
    template_name = 'blog/text_page_detail.jinja2'

    def get_queryset(self):
        queryset = super(TextPageDetail, self).get_queryset()
        return queryset.filter(published='p')
