from rest_framework.viewsets import ModelViewSet

from blog.models import Article

from .serializers import ArticleSerializer


class ArticleModelViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
