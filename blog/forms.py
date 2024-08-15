from django import forms

from .models import Article, Comment


class ArticleCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]


class CommentCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]
