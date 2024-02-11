from django.conf import settings
from django.db import models
from django.utils import timezone
from music_notes.models import MusicNotes


class Event(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="created_events",
    )
    name = models.CharField(max_length=50)
    date = models.DateField(help_text="date of the event")
    time = models.TimeField(null=True, blank=True)
    place = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="attended_events"
    )
    repertoire = models.ManyToManyField(MusicNotes, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
