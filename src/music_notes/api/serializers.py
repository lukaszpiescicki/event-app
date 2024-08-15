from music_notes.models import MusicNotes
from rest_framework import serializers


class MusicNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicNotes
        fields = "__all__"
