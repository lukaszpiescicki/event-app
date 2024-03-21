from django.urls import path
from .views import ArticleDetail, ArticleList

urlpatterns = [
    path('articles/', ArticleList.as_view(), name='get_articles'), # api/v1/articles/
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='get_article') # api/v1/articles/1/
]
