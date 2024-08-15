from django.conf import settings
from django.db import models
from django.urls import reverse


class MusicNotes(models.Model):
    title = models.CharField(max_length=50)
    duration = models.DurationField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    notes = models.FileField(
        upload_to="pdf", null=True, blank=True, help_text="Pdf file of music notes"
    )
    in_use = models.BooleanField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="music_notes",
    )
    date_posted = models.DateTimeField(auto_now_add=True)
    voice = models.CharField(
        max_length=20, null=True, blank=True, help_text="name of instrument and voice"
    )

    def get_absolute_url(self) -> str:
        return reverse("music-note-detail", kwargs={"pk": self.pk})
