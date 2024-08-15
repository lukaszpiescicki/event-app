from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..models import Article, Comment


class ArticleListView(ListView):
    model = Article
    template_name = "blog/blog.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 4


class ArticleDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "blog.view_article"
    model = Article
    template_name = "blog/article.html"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article = get_object_or_404(Article, id=self.kwargs["pk"])
        total_likes = article.total_likes()
        context["total_likes"] = total_likes

        return context


class ArticleCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "blog.add_article"
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(
    PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    permission_required = "blog.change_article"
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class ArticleDeleteView(
    PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    permission_required = "blog.delete_article"
    model = Article
    template_name = "blog/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["name", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article_id = self.kwargs["pk"]
        return super().form_valid(form)
