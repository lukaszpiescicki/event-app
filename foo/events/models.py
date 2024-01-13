from django.db import models


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    place = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
