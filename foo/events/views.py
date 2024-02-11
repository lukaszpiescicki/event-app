from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Event


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, id=pk)
    event.participants.add(request.user)
    return redirect("event-detail", pk=event.id)


class EventsListView(ListView):
    model = Event
    template_name = "events/events.html"
    context_object_name = "events"
    ordering = ["-date_posted"]


class EventsDetailView(DetailView):
    model = Event
    template_name = "events/event.html"


class EventsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = "events/events_form.html"
    fields = ["name", "date", "time", "place", "description", "repertoire"]
    permission_required = "events.add_event"


class EventsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "events/events_form.html"

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author


class EventsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "events/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author
