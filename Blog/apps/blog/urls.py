from django.urls import path, include

from . import views
from ..accounts.views import UserCreateView, CustomLoginView, MyPasswordChangeView, UserChangeView, PersonalArea
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
    path('subscription/', include([
        path('<int:pk>/', include([
            path('add/', views.AddSubscription.as_view(), name='subscription_add'),
            path('delete/', views.SubscriptionDelete.as_view(), name='subscription_delete'),
        ])),
    ])),
    path('accounts/', include([
        path('login/', CustomLoginView.as_view(), name='login'),
        path('create/', UserCreateView.as_view(), name='create_user'),
        path('profile/', PersonalArea.as_view(), name='personal-area'),
        path('change/', UserChangeView.as_view(), name='user-change'),
        path('password/', MyPasswordChangeView.as_view(), name='password-change'),
        ]),)
]
