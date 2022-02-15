from django.conf.urls import include
from django.urls import path

from api.interaction import views


urlpatterns = [
    path('comment/', include([
       path('list/', views.CommentListView.as_view(), name='api_comment_list'),
       path('<int:pk>/', views.CommentDetailView.as_view(), name='commentarticle-detail'),
    ])),
    path('favorite/', include([
       path('list/', views.FavoritesArticleListView.as_view(), name='api_favorite_list'),
       path('<int:pk>/', views.FavoritesArticleDetailView.as_view(), name='favoritesarticle-detail'),
    ])),
    # path('score/', include([
    #     path('list/', views.ScoreListView.as_view(), name='api_score_list'),
    #     path('<int:pk>/', views.ScoreDetailView.as_view(), name='score-detail'),
    # ])),
    path('subscription/', include([
        path('list/', views.AuthorSubscriptionListView.as_view(), name='api_subscription_list'),
        path('<int:pk>/', views.AuthorSubscriptionDetailView.as_view(), name='authorsubscription-detail'),
    ])),
]
