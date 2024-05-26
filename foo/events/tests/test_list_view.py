from core.consts import GROUPS__EVENT_ADMINS, GROUPS__EVENT_PARTICIPANTS
from django.contrib.auth.models import Group
from django.test import TestCase, tag
from django.urls import reverse
from users.factories import UserFactory

from ..factories import EventFactory


@tag("el")
class EventListViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__EVENT_ADMINS)
        participants_group = Group.objects.get(name=GROUPS__EVENT_PARTICIPANTS)

        self.admin = UserFactory(groups=admins_group)
        self.participant = UserFactory(groups=participants_group)

        self.event = EventFactory(author=self.admin)

        self.event1 = EventFactory(author=self.participant)

        self.event2 = EventFactory(author=self.admin)

    @tag("el1")
    def test_event_list_view_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("events-home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.event, response.context["events"])
        self.assertIn(self.event1, response.context["events"])
        self.assertIn(self.event2, response.context["events"])
        self.assertTemplateUsed(response, "events/events.html")
        self.assertEqual(len(response.context["events"]), 3)
