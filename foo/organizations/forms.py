from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Organization


class OrganizationCreateUpdateForm(UserCreationForm):
    class Meta:
        model = Organization
        fields = ["name", "city", "email", "phone_number"]
