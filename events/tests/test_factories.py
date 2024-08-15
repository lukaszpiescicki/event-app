from django.test import TestCase, tag

from events.factories import EventFactory
from events.models import Event


@tag("e")
class TestEventFactory(TestCase):
    def test_event_factory_creation_single_object(self):
        EventFactory.create()
        self.assertEqual(Event.objects.count(), 1)

    def test_event_factory_creation_bulk_objects(self):
        EventFactory.create_batch(5)

        self.assertEqual(Event.objects.count(), 5)
