from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(help_text="date of the event")
    time = models.DateTimeField(null=True, blank=True)
    place = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
