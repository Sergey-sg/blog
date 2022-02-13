from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api.blog import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('', include(router.urls), name='api_router'),
            path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            path('article/', include([
                path('list/', views.ArticleListView.as_view(), name='api_article_list'),
                path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
                path('images/', include([
                    path('', views.ImageArticleListView.as_view(), name='article-images'),
                    path('<int:pk>', views.ImageArticleDetailView.as_view(), name='imagearticle-detail'),
                ])),
            ])),
            path('text-page/', include([
                path('list/', views.TextPageListView.as_view(), name='api_text_page_list'),
                path('<int:pk>/', views.TextPageDetailView.as_view(), name='textpage-detail'),
            ])),
            path()
        ])),
    ])),
]
