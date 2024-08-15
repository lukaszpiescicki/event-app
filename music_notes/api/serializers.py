from rest_framework import serializers

from music_notes.models import MusicNotes


class MusicNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicNotes
        fields = "__all__"
