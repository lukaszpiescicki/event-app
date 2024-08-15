from core.consts import GROUPS__EVENT_ADMINS, GROUPS__EVENT_PARTICIPANTS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from events.models import Event
from rest_framework import status
from users.factories import UserFactory

from ..factories import EventFactory


class EventUpdateViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__EVENT_ADMINS)
        participants_group = Group.objects.get(name=GROUPS__EVENT_PARTICIPANTS)
        self.admin = UserFactory(groups=admins_group)
        self.participant = UserFactory(groups=participants_group)

        self.event = EventFactory(author=self.admin)

    def test_update_if_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {
                "name": "test-event",
                "date": "2023-02-02",
                "time": "11:00",
                "place": "Poznan",
                "description": "test",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.event.refresh_from_db()

        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.name, event.name)

    def test_update_if_one_value_passed(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "test-event"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.name, event.name)

    def test_update_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "test"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.event.refresh_from_db()
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.name, event.name)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("event-update", kwargs={"pk": self.event.pk}),
        )

    def test_update_if_user_is_not_author(self):
        self.client.force_login(self.participant)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "name"},
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        self.event.refresh_from_db()
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.name, event.name)

    def test_update_if_object_does_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": 100}), {"name": "name"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_incorrect_input_data(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(self.event.name, event.name)
