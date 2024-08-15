from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import MusicNotesViewSet
from .views import (
    MusicNotesCreateView,
    MusicNotesDeleteView,
    MusicNotesDetailView,
    MusicNotesListView,
    MusicNotesUpdateView,
)

router = SimpleRouter()
router.register(r"music-notes", MusicNotesViewSet, basename="music-notes-api")

urlpatterns = [
    path("music-notes/", MusicNotesListView.as_view(), name="music-notes-home"),
    path(
        "music-notes/<int:pk>/",
        MusicNotesDetailView.as_view(),
        name="music-note-detail",
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
    path("api/v1/", include(router.urls)),
]
