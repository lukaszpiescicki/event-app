from django import forms

from .models import Event


class EventCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "date", "time", "place", "description"]
