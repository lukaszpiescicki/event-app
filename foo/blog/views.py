from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article, Comment


def home(request):
    return render(request, "blog/blog.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def LikeView(request, pk):
    article = get_object_or_404(Article, id=request.POST.get("article_id"))
    article.likes.add(request.user)
    return HttpResponseRedirect(reverse("article-detail", args=[str(pk)]))


class ArticleListView(ListView):
    model = Article
    template_name = "blog/blog.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 4


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article.html"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article = get_object_or_404(Article, id=self.kwargs["pk"])
        total_likes = article.total_likes()
        context["total_likes"] = total_likes

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "blog/article_form.html"
    fields = ["title", "content"]

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
