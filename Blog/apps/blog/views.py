from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .filters import ArticleFilter
from .models import Article, Category


class ArticleListView(ListView):
    """
    Generates a list of article with ordering
    """
    template_name = 'blog/home.jinja2'
    paginate_by = 16
    filterset_class = ArticleFilter
    model = Article

    def get_queryset(self):
        """Return the filtered queryset"""
        queryset = self.model.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        try:
            categories = Category.objects.get(pk=self.request.GET['filter_category']).get_descendants()
            queryset = self.model.objects.filter(category=self.request.GET['filter_category'])
            if categories:
                for category in categories:
                    queryset1 = self.model.objects.filter(category=category)
                    queryset = queryset | queryset1
                return queryset
        except Exception:
            pass
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        """Add to context filter as "filterset" """
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['category'] = Category.get_annotated_list()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail_article.jinja2"
