from rest_framework.viewsets import generics
from rest_framework import mixins
from blog.models import Article
from .serializers import ArticleSerializer


class ArticleList(
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView
                ):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleDetail(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article
