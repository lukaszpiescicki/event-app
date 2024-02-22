from django.urls import path

from . import views
from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    CommentCreateView,
    LikeView,
)

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("contact/", views.contact, name="blog-contact"),
    path('article/', ArticleListView.as_view(), name='article-list'),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("article/new/", ArticleCreateView.as_view(), name="article-create"),
    path("article/update/<int:pk>", ArticleUpdateView.as_view(), name="article-update"),
    path("article/delete/<int:pk>", ArticleDeleteView.as_view(), name="article-delete"),
    path(
        "article/<int:pk>/comment/", CommentCreateView.as_view(), name="article-comment"
    ),
    path("article/<int:pk>/like/", LikeView, name="article-like"),
]
