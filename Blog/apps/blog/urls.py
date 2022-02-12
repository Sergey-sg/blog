from django.urls import path, include

from . import views
from ..accounts.views import UserCreateView, CustomLoginView, MyPasswordChangeView, UserChangeView, PersonalArea, \
    ConfirmRegistrationView, ActivateAccount, LogOut
from ..interaction.views import AddScore, UpdateScore, FavoriteAdd, FavoriteDelete, CommentCreate, CommentUpdate, \
    CommentDelete

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('article/', include([
        path('create/', views.ArticleCreate.as_view(), name='article_create'),
        path('<slug:slug>/', include([
            path('update/', views.ArticleUpdate.as_view(), name='article_update'),
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
    ])),
    path('subscription/', include([
        path('<int:pk>/', include([
            path('add/', views.AddSubscription.as_view(), name='subscription_add'),
            path('delete/', views.SubscriptionDelete.as_view(), name='subscription_delete'),
        ])),
    ])),
    path('accounts/', include([
        path('login/', CustomLoginView.as_view(), name='login'),
        path('logout/', LogOut.as_view(), name='logout'),
        path('create/', UserCreateView.as_view(), name='create_user'),
        path('profile/', PersonalArea.as_view(), name='personal-area'),
        path('change/', UserChangeView.as_view(), name='user-change'),
        path('password/', MyPasswordChangeView.as_view(), name='password-change'),
        path('confirmregistration/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
        path('activate/<str:uid>/<str:token>/', ActivateAccount.as_view(), name='user_activate')
        ]),),
    path('text-pages/', include([
        path('', views.TextPageList.as_view(), name='text_page_list'),
        path('<slug:slug>/', views.TextPageDetail.as_view(), name='text_page_detail'),
    ]))
]
