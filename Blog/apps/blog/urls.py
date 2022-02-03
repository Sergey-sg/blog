from django.urls import path, include

from . import views
from ..interaction.views import AddScore, UpdateScore, FavoriteAdd, FavoriteDelete, CommentCreate, CommentUpdate, \
    CommentDelete

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('<slug:slug>/', include([
        path('detail/', views.ArticleDetailView.as_view(), name='article_detail'),
        path('score/', include([
                    path('add/', AddScore.as_view(), name='add_score'),
                    path('update/', UpdateScore.as_view(), name='update_score'),
        ])),
        path('favorites/', include([
            path('add/', FavoriteAdd.as_view(), name='favorite_add'),
            path('delete/', FavoriteDelete.as_view(), name='favorite_delete'),
        ])),
        path('comment/', include([
            path('add/', CommentCreate.as_view(), name='comment_add'),
            path('<int:pk>/', include([
                path('change/', CommentUpdate.as_view(), name='comment_change'),
                path('delete/', CommentDelete.as_view(), name='comment_delete'),
            ])),
        ])),
    ])),
]
