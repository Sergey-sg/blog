from django.urls import path, include

from . import views
from ..interaction.views import AddScore, UpdateScore

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<slug:slug>/score/', include([
            path('add/', AddScore.as_view(), name='add_score'),
            path('update/', UpdateScore.as_view(), name='update_score'),
        ]),)
]
