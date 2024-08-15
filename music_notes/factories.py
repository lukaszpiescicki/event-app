import io
from datetime import datetime

import factory
from django.core.files.base import ContentFile
from factory.fuzzy import FuzzyInteger
from reportlab.pdfgen import canvas

from music_notes.models import MusicNotes
from users.factories import UserFactory


def generate_pdf():
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Example PDF for Music Notes")
    p.showPage()
    p.save()
    buffer.seek(0)

    return ContentFile(buffer.read(), "note.pdf")


class MusicNotesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MusicNotes

    title = factory.Faker("sentence", nb_words=3)
    duration = factory.Faker("time")
    url = factory.Faker("url")
    notes = factory.LazyFunction(generate_pdf)
    in_use = True
    author = factory.SubFactory(UserFactory)
    date_posted = factory.LazyFunction(datetime.now)
    voice = FuzzyInteger(1, 3)
