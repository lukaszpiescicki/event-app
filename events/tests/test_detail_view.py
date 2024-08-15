from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__EVENT_ADMINS, GROUPS__EVENT_PARTICIPANTS
from users.factories import UserFactory

from ..factories import EventFactory


class EventDetailViewTest(TestCase):
    def setUp(self) -> None:
        admins_group = Group.objects.get(name=GROUPS__EVENT_ADMINS)
        participants_group = Group.objects.get(name=GROUPS__EVENT_PARTICIPANTS)
        self.admin = UserFactory(groups=admins_group)

        self.participant = UserFactory(groups=participants_group)

        self.event = EventFactory(author=self.admin)

    def test_event_detail_view_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("event-detail", kwargs={"pk": self.event.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.event)
        self.assertTemplateUsed(response, "events/event.html")

    def test_event_detail_view_when_event_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("event-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_detail_view_if_user_is_not_author(self):
        self.client.force_login(self.participant)
        response = self.client.get(
            reverse("event-detail", kwargs={"pk": self.event.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.event)
        self.assertTemplateUsed(response, "events/event.html")
