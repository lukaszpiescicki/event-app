from django.urls import path

from .views import (
    EventsCreateView,
    EventsDeleteView,
    EventsDetailView,
    EventsListView,
    EventsUpdateView,
    event_register,
)

urlpatterns = [
    path("events/", EventsListView.as_view(), name="events-home"),
    path("events/<int:pk>/", EventsDetailView.as_view(), name="event-detail"),
    path("events/new/", EventsCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/update/", EventsUpdateView.as_view(), name="event-update"),
    path("events/<int:pk>/delete/", EventsDeleteView.as_view(), name="event-delete"),
    path("events/<int:pk>/participate/", event_register, name="event-register"),
]
