from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__NOTES_ADMINS, GROUPS__NOTES_USERS
from users.factories import UserFactory

from ..factories import MusicNotesFactory


class MusicNotesDetailViewTestCase(TestCase):
    def setUp(self) -> None:
        admins_group = Group.objects.get(name=GROUPS__NOTES_ADMINS)
        users_group = Group.objects.get(name=GROUPS__NOTES_USERS)
        self.admin = UserFactory(groups=admins_group)
        self.user = UserFactory(groups=users_group)

        self.music_notes = MusicNotesFactory(author=self.admin)

    def test_music_notes_detail_view_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("music-note-detail", kwargs={"pk": self.music_notes.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.music_notes)
        self.assertTemplateUsed(response, "music_notes/note.html")

    def test_music_notes_detail_view_when_note_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("music-note-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_music_notes_detail_view_if_user_not_author(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("music-note-detail", kwargs={"pk": self.music_notes.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.music_notes)
        self.assertTemplateUsed(response, "music_notes/note.html")
