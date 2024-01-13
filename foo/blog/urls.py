from django.urls import path
from . import views
from .views import ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'), # articles/<int:pk>
    path('article/new/', ArticleCreateView.as_view(), name='article-create'), # articles/new
    path('article/update/<int:pk>', ArticleUpdateView.as_view(), name='article-update'), # articles/<int:pk>/update
    path('article/delete/<int:pk>', ArticleDeleteView.as_view(), name='article-delete'), # articles/<int:pk>/delete
]
