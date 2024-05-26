from core.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, UpdateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import EventCreateUpdateForm
from .models import Event


class EventRegisterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs["pk"])
        event.participants.add(request.user)
        return redirect("event-detail", pk=event.id)


class EventMailingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs["pk"])
        emails = [user.email for user in event.participants]
        send_mail(
            event.name,
            f"Hello, new event ${event.name} was created",
            DEFAULT_FROM_EMAIL,
            emails,
        )


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
    form_class = EventCreateUpdateForm
    permission_required = "events.add_event"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventsUpdateView(
    PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Event
    template_name = "events/events_form.html"
    form_class = EventCreateUpdateForm
    permission_required = "events.change_event"

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author


class EventsDeleteView(
    PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    permission_required = "events.delete_event"
    model = Event
    template_name = "events/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author
