from django.conf import settings
from django.db import models
from django.utils import timezone


class MusicNotes(models.Model):
    title = models.CharField(max_length=50)
    duration = models.DurationField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    notes = models.FileField(upload_to="pdf", null=True, blank=True)
    in_use = models.BooleanField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_posted = models.DateTimeField(default=timezone.now)
