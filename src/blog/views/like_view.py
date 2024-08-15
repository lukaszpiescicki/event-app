from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from ..models import Article


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=request.POST.get("article_id"))
        article.likes.add(request.user)
        return redirect("article-detail", pk=kwargs["pk"])
