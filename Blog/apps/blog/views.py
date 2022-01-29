from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from .filters import ArticleFilter
from .models import Article


class ArticleListView(ListView):
    """
    Generates a list of article with ordering
    """
    # permission_required = 'MiniCRM.can_see_companies'
    template_name = 'blog/home.jinja2'
    paginate_by = 16
    filterset_class = ArticleFilter
    model = Article
