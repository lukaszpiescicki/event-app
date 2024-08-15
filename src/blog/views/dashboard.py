from django.views.generic import TemplateView
from django.views.generic.list import ListView

from ..models import Article


class HomeView(ListView):
    model = Article
    template_name = "blog/blog.html"
    context_object_name = "articles"


class ContactView(TemplateView):
    template_name = "contact.html"
