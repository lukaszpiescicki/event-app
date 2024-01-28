from django.urls import path

from .views import (
    MusicNotesCreateView,
    MusicNotesDeleteView,
    MusicNotesDetailView,
    MusicNotesListView,
    MusicNotesUpdateView,
)

urlpatterns = [
    path("music-notes/", MusicNotesListView.as_view(), name="music-notes-home"),
    path(
        "music-notes/<int:pk>/",
        MusicNotesDetailView.as_view(),
        name="music_note-detail",
    ),
    path("music-notes/new/", MusicNotesCreateView.as_view(), name="music-note-create"),
    path(
        "music-notes/<int:pk>/update/",
        MusicNotesUpdateView.as_view(),
        name="music-note-update",
    ),
    path(
        "music-notes/<int:pk>/delete/",
        MusicNotesDeleteView.as_view(),
        name="music-note-delete",
    ),
]
