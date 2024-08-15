from django.contrib.auth.models import Group
from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__EVENT_ADMINS, GROUPS__EVENT_PARTICIPANTS
from events.models import Event
from users.factories import UserFactory

from ..factories import EventFactory


@tag("ed")
class EventDeleteViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__EVENT_ADMINS)
        participants_group = Group.objects.get(name=GROUPS__EVENT_PARTICIPANTS)
        self.admin = UserFactory(groups=admins_group)
        self.participant = UserFactory(groups=participants_group)

        self.event = EventFactory(author=self.admin)

    @tag("ed1")
    def test_delete_event_when_user_is_author(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": self.event.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)

    @tag("ed2")
    def test_delete_event_which_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("ed3")
    def test_delete_event_when_user_is_not_author(self):
        self.client.force_login(self.participant)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": self.event.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Event.objects.count(), 1)

    @tag("ed4")
    def test_delete_event_when_user_not_logged_in(self):
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": self.event.pk}), follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("event-delete", kwargs={"pk": self.event.pk}),
        )
        self.assertEqual(Event.objects.count(), 1)
