from core.consts import GROUPS__NOTES_ADMINS, GROUPS__NOTES_USERS
from django.contrib.auth.models import Group
from django.test import TestCase, tag
from django.urls import reverse
from music_notes.models import MusicNotes
from rest_framework import status
from users.factories import UserFactory

from ..factories import MusicNotesFactory


class MusicNotesDeleteViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__NOTES_ADMINS)
        users_group = Group.objects.get(name=GROUPS__NOTES_USERS)
        self.admin = UserFactory(groups=admins_group)
        self.user = UserFactory(groups=users_group)

        self.music_notes = MusicNotesFactory(author=self.admin)

    def test_delete_music_notes_when_user_is_author(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-delete", kwargs={"pk": self.music_notes.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MusicNotes.objects.count(), 0)

    def test_delete_music_notes_which_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("music-note-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_music_notes_When_user_is_not_author(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("music-note-delete", kwargs={"pk": self.music_notes.pk}),
            follow=False,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MusicNotes.objects.count(), 1)

    @tag("x")
    def test_delete_music_notes_when_user_not_logged_in(self):
        response = self.client.post(
            reverse("music-note-delete", kwargs={"pk": self.music_notes.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("music-note-delete", kwargs={"pk": self.music_notes.pk}),
        )
        self.assertEqual(MusicNotes.objects.count(), 1)
