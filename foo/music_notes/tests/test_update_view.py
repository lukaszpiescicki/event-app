from core.consts import GROUPS__NOTES_ADMINS, GROUPS__NOTES_USERS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from music_notes.models import MusicNotes
from rest_framework import status
from users.factories import UserFactory

from ..factories import MusicNotesFactory


class MusicNotesUpdateViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__NOTES_ADMINS)
        users_group = Group.objects.get(name=GROUPS__NOTES_USERS)
        self.admin = UserFactory(groups=admins_group)
        self.user = UserFactory(groups=users_group)

        self.music_notes = MusicNotesFactory(author=self.admin)

    def test_update_music_notes_if_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
            {
                "title": "Test",
                "date_posted": "2023-02-02",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.music_notes.refresh_from_db()
        note = MusicNotes.objects.get(pk=self.music_notes.pk)
        self.assertEqual(self.music_notes.title, note.title)

    def test_update_music_notes_if_one_value_passed(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
            {"title": "Test"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.music_notes.refresh_from_db()
        note = MusicNotes.objects.get(pk=self.music_notes.pk)
        self.assertEqual(self.music_notes.title, note.title)

    def test_update_music_notes_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
            {"title": "Test"},
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.music_notes.refresh_from_db()
        note = MusicNotes.objects.get(pk=self.music_notes.pk)
        self.assertEqual(self.music_notes.title, note.title)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
        )

    def test_update_music_notes_if_user_is_not_author(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
            {"title": "Test"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.music_notes.refresh_from_db()
        note = MusicNotes.objects.get(pk=self.music_notes.pk)
        self.assertEqual(self.music_notes.title, note.title)

    def test_update_music_notes_if_object_does_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": 100}),
            {"title": "title"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_music_notes_with_incorrect_input_data(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-update", kwargs={"pk": self.music_notes.pk}),
            {"title": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = MusicNotes.objects.get(pk=self.music_notes.pk)
        self.assertEqual(self.music_notes.title, note.title)
