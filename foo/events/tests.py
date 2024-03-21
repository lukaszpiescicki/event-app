from datetime import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from events.models import Event
from rest_framework import status
from users.models import CustomUser


class EventCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        content_type = ContentType.objects.get_for_model(Event)
        permission = Permission.objects.get(
            codename="add_event", content_type=content_type
        )
        self.user.user_permissions.add(permission)
        self.user.save()
        self.client.force_login(self.user)

    def test_get_all_events_when_db_is_empty(self):
        response = self.client.get(reverse("events-home"))
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context["events"]), 0)
        self.assertTemplateUsed(response, "events/events.html")

    def test_create_event_redirect_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=/events/new/")

    def test_create_event_render_page_and_return_200_when_user_logged_in(self):
        response = self.client.get(reverse("event-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "events/events_form.html")

    def test_create_event_correct_object_created(self):
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
        self.assertEqual(event.author, self.user)

    def test_create_event_with_incorrect_input_data(self):
        self.client.force_login(self.user)
        self.assertEqual(Event.objects.count(), 0)
        response = self.client.post(
            reverse("event-create"),
            {"name": "", "date": "2024-10-12", "time": "12:00", "place": "Sroda"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)


class EventUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.event = Event.objects.create(
            author=self.user,
            name="event-name",
            date="2023-01-02",
            time="12:00",
            place="Sroda",
        )

    def test_update_if_user_logged_in(self):
        self.client.force_login(self.user)
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

        self.assertEqual(self.event.name, "test-event")

    def test_update_if_one_value_passed(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "test-event"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "event-name")

    def test_update_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "test"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "event-name")
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("event-update", kwargs={"pk": self.event.pk}),
        )

    def test_update_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": "name"},
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "event-name")

    def test_update_if_object_does_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": 100}), {"name": "name"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_incorrect_input_data(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("event-update", kwargs={"pk": self.event.pk}),
            {"name": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "event-name")


class EventDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.event = Event.objects.create(
            author=self.user,
            name="event-name",
            date="2023-01-02",
            time="12:00",
            place="Sroda",
        )

    def test_delete_event_when_user_is_author(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": self.event.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_event_which_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_event_when_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("event-delete", kwargs={"pk": self.event.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Event.objects.count(), 1)

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


class EventListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.event = Event.objects.create(
            author=self.user,
            name="event-name",
            date="2023-01-01",
            time="12:00",
            place="Sroda",
        )

        self.event1 = Event.objects.create(
            author=self.user1,
            name="event1",
            date="2023-02-02",
            time="22:22",
            place="Turek",
        )

        self.event2 = Event.objects.create(
            author=self.user,
            name="event2",
            date="2023-03-03",
            time="13:33",
            place="Poznan",
        )

    def test_event_list_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("events-home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.event, response.context["events"])
        self.assertIn(self.event1, response.context["events"])
        self.assertIn(self.event2, response.context["events"])
        self.assertTemplateUsed(response, "events/events.html")
        self.assertEqual(len(response.context["events"]), 3)


class EventDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.event = Event.objects.create(
            author=self.user,
            name="event-name",
            date="2023-01-01",
            time="12:00",
            place="Sroda",
        )

    def test_event_detail_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("event-detail", kwargs={"pk": self.event.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.event)
        self.assertTemplateUsed(response, "events/event.html")

    def test_event_detail_view_when_event_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("event-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_detail_view_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse("event-detail", kwargs={"pk": self.event.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.event)
        self.assertTemplateUsed(response, "events/event.html")
