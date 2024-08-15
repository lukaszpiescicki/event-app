from datetime import datetime

import factory

from music_notes.factories import MusicNotesFactory
from users.factories import UserFactory

from .models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    author = factory.SubFactory(UserFactory)
    name = factory.Faker("sentence", nb_words=6)
    date = factory.LazyFunction(datetime.today)
    time = factory.LazyFunction(datetime.now)
    place = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("paragraph", nb_sentences=5)
    repertoire = factory.SubFactory(MusicNotesFactory)
    date_posted = factory.LazyFunction(datetime.now)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

    @factory.post_generation
    def repertoire(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for music_note in extracted:
                self.repertoire.add(music_note)
