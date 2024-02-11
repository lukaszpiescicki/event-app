from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import MusicNotes


class MusicNotesListView(ListView):
    model = MusicNotes
    template_name = "music_notes/music_notes.html"
    context_object_name = "music_notes"
    ordering = ["-date_posted"]


class MusicNotesDetailView(DetailView):
    model = MusicNotes
    template_name = "music_notes/note.html"


class MusicNotesCreateView(LoginRequiredMixin, CreateView):
    model = MusicNotes
    template_name = "music_notes/notes_form.html"
    fields = ["title", "duration", "url", "notes", "in_use"]

    def form_valid(self, form):
        form.author = self.request.user
        return super().form_valid(form)


# TODO jak to przekierować do detailView edytowanego ?
class MusicNotesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MusicNotes
    template_name = "music_notes/notes_form.html"
    fields = ["title", "duration", "url", "notes", "in_use"]

    def test_func(self):
        music_note = self.get_object()
        return self.request.user == music_note.author

    def get_success_url(self):
        return reverse("music-note-detail", args=[self.object.pk])


class MusicNotesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MusicNotes
    template_name = "music_notes/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        music_note = self.get_object()
        return self.request.user == music_note.author
