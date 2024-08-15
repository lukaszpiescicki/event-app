from django.conf import settings
from django.db import models
from django.urls import reverse

from music_notes.models import MusicNotes


class Event(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="created_events",
    )
    name = models.CharField(max_length=100)
    date = models.DateField(help_text="date of the event")
    time = models.TimeField(null=True, blank=True, help_text="time of the event")
    place = models.CharField(max_length=500)
    description = models.CharField(max_length=500, null=True, blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="attended_events"
    )
    repertoire = models.ManyToManyField(
        MusicNotes,
        blank=True,
        null=True,
        help_text="music_notes required for the " "event",
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self) -> str:
        return reverse("event-detail", kwargs={"pk": self.pk})
