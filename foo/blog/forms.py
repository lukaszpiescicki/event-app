from django import forms

from .models import Comment


class CommentCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]
