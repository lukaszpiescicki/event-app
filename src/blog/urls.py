from blog.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    CommentCreateView,
    ContactView,
    HomeView,
    LikeView,
    PDFView,
)
from django.urls import path
from rest_framework.routers import SimpleRouter

from .api.views import ArticleModelViewSet

router = SimpleRouter()
router.register(r"articles", ArticleModelViewSet, basename="api-articles")

urlpatterns = [
    path("", HomeView.as_view(), name="blog-home"),
    path("contact/", ContactView.as_view(), name="blog-contact"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/new/", ArticleCreateView.as_view(), name="article-create"),
    path(
        "articles/<int:pk>/update", ArticleUpdateView.as_view(), name="article-update"
    ),
    path(
        "articles/<int:pk>/delete", ArticleDeleteView.as_view(), name="article-delete"
    ),
    path(
        "articles/<int:pk>/comment/",
        CommentCreateView.as_view(),
        name="article-comment",
    ),
    path("articles/<int:pk>/like/", LikeView.as_view(), name="article-like"),
    path("articles/<int:pk>/download/", PDFView.as_view(), name="article-download"),
]

urlpatterns += router.urls
