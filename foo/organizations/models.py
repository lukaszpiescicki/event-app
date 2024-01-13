from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, null=True, blank=True)



