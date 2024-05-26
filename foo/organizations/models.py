from django.conf import settings
from django.db import models
from django.urls import reverse


class Organization(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="member_organizations"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_organizations",
    )

    def get_absolute_url(self) -> str:
        return reverse("organization-detail", kwargs={"pk": self.pk})
