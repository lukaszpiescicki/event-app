from django.urls import path
from .views import GetArticle, GetAllArticles

urlpatterns = [
    path('articles/', GetAllArticles.as_view(), name='get_articles'), # api/v1/articles/
    path('articles/<int:pk>/', GetArticle.as_view(), name='get_article') # api/v1/articles/1/
]
