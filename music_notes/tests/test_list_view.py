from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from core.consts import GROUPS__NOTES_ADMINS, GROUPS__NOTES_USERS
from users.factories import UserFactory

from ..factories import MusicNotesFactory


class MusicNotesListViewTestCase(TestCase):
    def setUp(self) -> None:
        admins_group = Group.objects.get(name=GROUPS__NOTES_ADMINS)
        users_group = Group.objects.get(name=GROUPS__NOTES_USERS)

        self.admin = UserFactory(groups=admins_group)
        self.user = UserFactory(groups=users_group)

        self.note = MusicNotesFactory(author=self.admin)
        self.note1 = MusicNotesFactory(author=self.user)
        self.note2 = MusicNotesFactory(author=self.admin)

    def test_music_notes_list_view_when_user_logged_in(self) -> None:
        self.client.force_login(self.admin)
        response = self.client.get(reverse("music-notes-home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note, response.context["music_notes"])
        self.assertIn(self.note1, response.context["music_notes"])
        self.assertIn(self.note2, response.context["music_notes"])
        self.assertTemplateUsed(response, "music_notes/music_notes.html")
        self.assertEqual(len(response.context["music_notes"]), 3)
