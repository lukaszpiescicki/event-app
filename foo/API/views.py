from rest_framework.viewsets import generics
from .serializers import ArticleSerializer
from blog.models import Article


class GetAllArticles(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class GetArticle(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article
