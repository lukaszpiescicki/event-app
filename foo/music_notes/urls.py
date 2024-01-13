from django.urls import path
from . import views
from .views import MusicNotesDetailView, MusicNotesCreateView, MusicNotesListView, MusicNotesDeleteView, MusicNotesUpdateView

urlpatterns = [
    path('musicnote', MusicNotesListView.as_view(), name='music_note-home'),
    path('musicnote/<int:pk>/', MusicNotesDetailView.as_view(), name='music_note-detail'),
    path('musicnote/new/', MusicNotesCreateView.as_view(), name='music_note-create'),
    path('musicnote/update/<int:pk>/', MusicNotesUpdateView.as_view(), name='music_note-update'),
    path('musicnote/delete/<int:pk>/', MusicNotesDeleteView.as_view(), name='music_note-delete'),
]
