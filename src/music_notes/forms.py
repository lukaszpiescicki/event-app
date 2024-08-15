from django import forms

from .models import MusicNotes


class MusicNotesCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MusicNotes
        fields = ["title", "duration", "url", "notes", "in_use"]
