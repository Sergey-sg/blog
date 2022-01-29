from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    """
    Generates a list of article with ordering
    """
    # permission_required = 'MiniCRM.can_see_companies'
    template_name = 'home.jinja'
    paginate_by = 2
    # filterset_class = CompanyFilter
    model = Article
