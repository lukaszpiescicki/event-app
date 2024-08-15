from events.models import Event
from rest_framework.viewsets import ModelViewSet

from .serializers import EventSerializer


class EventModelViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
