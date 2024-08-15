from django.urls import path
from rest_framework.routers import SimpleRouter

from .api.views import EventModelViewSet
from .views import (
    EventRegisterView,
    EventsCreateView,
    EventsDeleteView,
    EventsDetailView,
    EventsListView,
    EventsUpdateView,
)

router = SimpleRouter()
router.register(r"api-events", EventModelViewSet, basename="api-events")

urlpatterns = [
    path("events/", EventsListView.as_view(), name="events-home"),
    path("events/<int:pk>/", EventsDetailView.as_view(), name="event-detail"),
    path("events/new/", EventsCreateView.as_view(), name="event-create"),
    path("events/<int:pk>/update/", EventsUpdateView.as_view(), name="event-update"),
    path("events/<int:pk>/delete/", EventsDeleteView.as_view(), name="event-delete"),
    path(
        "events/<int:pk>/participate/",
        EventRegisterView.as_view(),
        name="event-register",
    ),
]

urlpatterns += router.urls
