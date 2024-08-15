from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__NOTES_ADMINS
from music_notes.models import MusicNotes
from users.factories import UserFactory


class MusicNotestCreateViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__NOTES_ADMINS)
        self.admin = UserFactory(groups=admins_group)

    def test_get_all_music_notes_when_db_is_empty(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("music-notes-home"))
        context = response.context
        print(context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(context["music_notes"]), 0)
        self.assertTemplateUsed(response, "music_notes/music_notes.html")

    def test_create_music_notes_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse("music-note-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=/music-notes/new/")

    def test_create_music_notes_render_page_and_return_200_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("music-note-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "music_notes/notes_form.html")

    def test_create_music_notes_correct_object_created(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-create"),
            {
                "title": "Test",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(MusicNotes.objects.count(), 1)
        first_notes = MusicNotes.objects.first()
        self.assertEqual(first_notes.title, "Test")
