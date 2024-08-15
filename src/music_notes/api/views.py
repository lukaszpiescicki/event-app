from music_notes.models import MusicNotes
from rest_framework.viewsets import ModelViewSet

from .serializers import MusicNotesSerializer


class MusicNotesViewSet(ModelViewSet):
    serializer_class = MusicNotesSerializer
    queryset = MusicNotes.objects.all()
