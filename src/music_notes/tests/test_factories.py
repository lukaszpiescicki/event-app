from django.test import TestCase
from music_notes.factories import MusicNotesFactory
from music_notes.models import MusicNotes


class TestMusicNoteFactory(TestCase):
    def test_music_note_factory_creation_single_object(self):
        MusicNotesFactory.create()
        self.assertEqual(MusicNotes.objects.count(), 1)

    def test_music_note_factory_creation_bulk_objects(self):
        MusicNotesFactory.create_batch(5)

        self.assertEqual(MusicNotes.objects.count(), 5)
