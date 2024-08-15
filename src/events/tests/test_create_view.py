from datetime import datetime

from core.consts import GROUPS__EVENT_ADMINS, GROUPS__EVENT_PARTICIPANTS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from events.models import Event
from rest_framework import status
from users.factories import UserFactory


class EventCreateViewTestCase(TestCase):
    def setUp(self):
        admin_group = Group.objects.get(name=GROUPS__EVENT_ADMINS)
        participant_group = Group.objects.get(name=GROUPS__EVENT_PARTICIPANTS)
        self.admin = UserFactory(groups=admin_group)
        self.participant = UserFactory(groups=participant_group)

    def test_get_all_events_when_db_is_empty(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("events-home"))
        context = response.context
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(context["events"]), 0)
        self.assertTemplateUsed(response, "events/events.html")

    def test_create_event_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=/events/new/")

    def test_create_event_render_page_and_return_200_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "events/events_form.html")

    def test_create_event_correct_object_created(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("event-create"),
            {
                "name": "event-name",
                "date": "2024-10-12",
                "time": "12:00",
                "place": "Sroda",
                "description": "test",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.name, "event-name")
        self.assertEqual(event.date, datetime.date(datetime(2024, 10, 12)))
        self.assertEqual(event.time, datetime.time(datetime(2024, 10, 12, 12, 0)))
        self.assertEqual(event.place, "Sroda")
        self.assertEqual(event.description, "test")
        self.assertEqual(event.author, self.admin)

    def test_create_event_with_incorrect_input_data(self):
        self.client.force_login(self.admin)
        self.assertEqual(Event.objects.count(), 0)
        response = self.client.post(
            reverse("event-create"),
            {"name": "", "date": "2024-10-12", "time": "12:00", "place": "Sroda"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)
