from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics

from api.blog.serializers import ArticleSerializer, UserSerializer, CategorySerializer, ImageArticleSerializer, \
    TextPageSerializer
from apps.blog.models import Article, Category, ImageArticle, TextPage


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleListView(generics.ListCreateAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # parser_classes = (FormParser, MultiPartParser, JSONParser)


class ImageArticleListView(generics.ListCreateAPIView):
    queryset = ImageArticle.objects.all()
    serializer_class = ImageArticleSerializer


class ImageArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImageArticle.objects.all()
    serializer_class = ImageArticleSerializer


class TextPageListView(generics.ListCreateAPIView):
    queryset = TextPage.objects.all()
    serializer_class = TextPageSerializer


class TextPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TextPage.objects.all()
    serializer_class = TextPageSerializer
