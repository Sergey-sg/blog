from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from ..accounts.views import UserCreateView, CustomLoginView, MyPasswordChangeView, UserChangeView, PersonalArea, \
    ConfirmRegistrationView, ActivateAccount
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
        path('logout/', LogoutView.as_view(template_name='registration/logged_out.jinja2'), name='logout'),
        path('create/', UserCreateView.as_view(), name='create_user'),
        path('activate-done/', TemplateView.as_view(
            template_name='registration/activate_done.jinja2'), name='activate_done'),
        path('profile/', PersonalArea.as_view(), name='personal-area'),
        path('change/', UserChangeView.as_view(), name='user-change'),
        path('password/', include([
            path('', MyPasswordChangeView.as_view(), name='password-change'),
            path('reset/', include([
                path('', PasswordResetView.as_view(template_name='registration/password_reset_form.jinja2'),
                     name='password_reset'),
                path('done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.jinja2'),
                     name='password_reset_done'),
                path('<uidb64>/<token>/',
                     PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.jinja2"),
                     name='password_reset_confirm'
                     ),
                path('complete/', PasswordResetCompleteView.as_view(
                    template_name='registration/password_reset_complete.jinja2'), name='password_reset_complete'),
            ])),
        ])),

        path('confirmregistration/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
        path('activate/<uid>/<token>/', ActivateAccount.as_view(), name='user_activate')
        ]),),
    path('text-pages/', include([
        path('', views.TextPageList.as_view(), name='text_page_list'),
        path('<slug:slug>/', views.TextPageDetail.as_view(), name='text_page_detail'),
    ]))
]
