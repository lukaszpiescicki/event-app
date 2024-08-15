from rest_framework.viewsets import ModelViewSet

from music_notes.models import MusicNotes

from .serializers import MusicNotesSerializer


class MusicNotesViewSet(ModelViewSet):
    serializer_class = MusicNotesSerializer
    queryset = MusicNotes.objects.all()
