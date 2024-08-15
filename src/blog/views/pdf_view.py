from core import renderers
from django.shortcuts import get_object_or_404
from django.views.generic import View

from ..models import Article


class PDFView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs["pk"])
        return renderers.render_to_pdf(
            template_src="blog/article_content.html", context_dict={"object": article}
        )
